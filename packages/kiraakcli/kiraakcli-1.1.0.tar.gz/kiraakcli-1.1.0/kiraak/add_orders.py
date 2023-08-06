"""Handles adding orders to kiraak"""
import difflib
import logging
import re
import sys
import typing as t

from click import confirm
from rich.table import Table

from kiraak import console
from kiraak.api import add_order
from kiraak.config import Config

logger = logging.getLogger(__name__)

# Check whether  product exists in catalog
def match(prod, catalog, conf=True):
    """Gets the closest match to a product"""
    close_matches = difflib.get_close_matches(prod, catalog, len(catalog), 0)
    if not conf:
        return close_matches[0]
    if not close_matches:
        logger.error(f"Product {prod} not found in catalog!")
        sys.exit(1)
    for res in close_matches:
        logger.info(
            f"Matching [bold]{prod}[/] -> [bold]{res}[/]",
            extra={"markup": True},
        )
        if (
            inp := input("Continue? ([Y]es/[n]o/[q]uit/[s]kip/[name]) ").lower()
        ) == "n":
            continue
        if inp in ["y", ""]:
            return res.split("|")[0]
        if inp == "s":
            return None
        if inp == "name":
            return match(input("Enter name of product: "), catalog)
        logger.error("Quitting...")
        sys.exit(1)


def get_mapping(prods, catalog):
    """Gets a mapping of the products in the to the products in the catalog"""
    mapping = {}

    for product in prods:
        if mapping.get(product):
            continue  # product mapping exists, but this product is just a diff weight

        mapping[product] = match(product, catalog, conf=False)

    while True:
        tbl = Table("Number", "Excel Product", "Catalog Product")
        for i, map_ in enumerate(mapping.items()):
            val, catalog_val = map_
            tbl.add_row(str(i), val, catalog_val)

        console.print(tbl)
        if confirm("Edit mapping?", default=True):
            while True:
                num = int(input("Enter number of product to edit: "))
                product = list(mapping.keys())[num]
                mapping[product] = match(product, catalog)
                if not confirm("Continue editing?", default=True):
                    break
        else:
            break

    return mapping


def add_orders(orders: t.List[t.Dict], price_id, catalog):
    """Adds the provided orders"""
    prods = list({x["name"] for o in orders for x in o["products"]})
    cat_prods = list(
        map(lambda x: x["productId"]["productName"], catalog["productList"])
    )
    mapping = get_mapping(prods, cat_prods)
    for order in orders:
        res = re.match(Config.FLAT_RE, order["billing_address"])
        if not res:
            logger.error(
                f"Could not parse billing address {order['billing_address']}, skipping order"
            )
            continue
        name = f'{order["billing_first_name"]} {order.get("billing_last_name")}'
        flat = f'{res.group("block")}-{res.group("flat")}'
        logger.info(f"Adding order of {name} @ {flat}:")
        tbl = Table("Product", "Quantity", "Catalog Name")
        for prod in order["products"]:
            tbl.add_row(
                prod["name"],
                prod["qty"],
                mapping[prod["name"]],
            )
        console.print(tbl)
        if confirm(f"Confirm order of {name} @ {flat}?"):
            final_order = {
                "name": name,
                "flat": flat,
                "total": order["order_subtotal"],
                "products": [
                    {
                        "cat": next(
                            (
                                x
                                for x in catalog["productList"]
                                if x["productId"]["productName"] == mapping[p["name"]]
                            )
                        ),
                        "amt": int(p["qty"]),
                        "price": p["item_price"],
                    }
                    for p in order["products"]
                ],
            }
            add_order(final_order, price_id)
        else:
            logger.error("Order not added!")

    return orders
