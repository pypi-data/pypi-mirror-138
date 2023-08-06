"""Module for main API requests"""
import functools
import json
import logging
import sys
import typing as t
from datetime import datetime

from click import confirm
from kiraak.mapping import Mapping

from kiraak.config import API, session

logger = logging.getLogger(__name__)


def authorized(wrapped_fn: t.Callable) -> t.Callable:
    """Decorator for ensuring that the headers contain the token"""

    @functools.wraps(wrapped_fn)
    def _wrapper(*args, **kwargs):
        if not (
            session.headers.get("Authorization")
            and session.headers.get("Authorization").startswith("Bearer ")
        ):
            logger.error("Not logged in!")
            sys.exit(1)
        return wrapped_fn(*args, **kwargs)

    return _wrapper


def login(mobile: str, password: str) -> dict:
    """Logs into kiraak using the login route and returns the token"""
    if API.TOKEN_FILE.exists() and len(API.TOKEN_FILE.read_text()) > 0:
        with open(API.TOKEN_FILE, "r") as file:
            data = json.load(file)
            session.headers.update({"Authorization": "Bearer " + data["token"]})
            return data["partnerInfo"]
    res = session.post(API.LOGIN, json={"mobile": mobile, "password": password}).json()
    if not res["isAuthenticated"]:
        logger.error(
            f"Failed to login: {res['message']}",
        )
        sys.exit(1)
    with open(API.TOKEN_FILE, "w+") as file:
        json.dump(
            {
                "token": res["token"],
                "time": str(datetime.now()),
                "partnerInfo": res["partnerInfo"],
            },
            file,
        )
    session.headers.update({"Authorization": "Bearer " + res["token"]})
    return res["partnerInfo"]


@authorized
def get_catalog() -> dict:
    """Gets the catalog of products"""
    res = session.get(API.CATALOG).json()
    if not res["activePrice"]:
        logger.error(f"Failed to get catalog: {res['message']}")
        sys.exit(1)
    return res["priceList"]


@authorized
def get_customer(flat) -> dict:
    """Get a customer from their flat no."""
    customers = session.get(API.CUSTOMERS).json()
    if customers["message"] != "customers found by partner":
        logger.error(f"Failed to get customers: {customers['message']}")
    try:
        return next(
            (
                x
                for x in customers["viewAllCustomers"]
                if x["customerCommunityInfo"]["customerHouseNo"] == flat
            )
        )
    except StopIteration:
        logger.error(f"User @ {flat} not found!")
        sys.exit(1)


@authorized
def get_current_order(customer):
    """TODO: Get the current order of a customer"""
    orders = session.get(API.ACTIVE_ORDERS.format(id=customer[id])).json()


@authorized
def add_order(order: t.Dict[str, str], mapping: Mapping, price_id) -> None:
    """Adds the given order using the kiraak API"""
    customer = get_customer(order["flat"])
    data = {
        "orderType": "regular",
        "priceId": price_id,
        "customerId": customer["_id"],
        "orderSource": "whatsApp",
        "orderNote": "",
        "orderBillAmount": order["total"],
        "cartList": [],
    }
    for prod in order["products"]:
        data["cartList"].append(
            {
                "productId": prod["cat"].product_id,
                "orderQuantity": prod["amt"],
                "productTotalBill": prod["amt"] * prod["price"],
                "productBaseQuantity": prod["cat"].quantity,
            }
        )
    res = session.post(API.ADD_ORDER, json=data).json()
    if res["message"] == (
        "Failed to add order: there is an active order, "
        "please process the active order to place a new order"
    ):
        logger.error(f"Failed to add order: {res['message']}")
        sys.exit(1)
        # TODO: Complete
        if confirm(
            f"An order already exists for {order['name']} @ {order['flat']}"
            ", do you want to replace it?"
        ):
            current = get_current_order(customer)
            res = session.put(API.UPDATE_ORDER.format(id=current[""]), json=data).json()
    elif res["message"] != "order created successfully":
        logger.error(f"Failed to add order: {res['message']}")
        sys.exit(1)
    else:
        logger.info("Added order!")
