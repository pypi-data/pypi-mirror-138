"""Processing of json file and adding orders"""
import json
import logging

from rich.table import Table

from kiraak import console
from kiraak.add_orders import add_orders
from kiraak.api import get_catalog, login
from kiraak.config import Config

data = {}
logger = logging.getLogger(__name__)


def main(file: str) -> None:
    """Process files, adds orders"""

    # Login
    logger.info(f"Logging in as {Config.MOBILE}")
    partner_info = data["partner_info"] = login(Config.MOBILE, Config.PASSWORD)
    logger.info(
        f"Logged in as {partner_info['partnerName']} @ {partner_info['partnerBrand']}"
    )

    # Get and print catalog
    logger.info("Fetching catalog...")
    catalog = data["catalog"] = get_catalog()
    price_id = catalog["_id"]
    logger.info(f"Recieved catalog (id {catalog['_id']})")
    tbl = Table(
        "Product Name",
        "Price",
        "Base quantity",
        "In Stock?",
    )
    for product in catalog["productList"]:
        prod_id = product["productId"]
        tbl.add_row(
            prod_id["productName"],
            "₹" + product["productPrice"],
            product["productBaseQuantity"],
            str(product["productAvailability"] == "instock"),
        )
    console.print(tbl)

    # Process json file
    logger.info(f"Processing {file}")
    with open(file, "r") as file_obj:
        orders = json.load(file_obj)
    logger.info(f"Processed {len(orders)} orders")

    logger.info(f"Adding {len(orders)} orders...")
    add_orders(orders, price_id, catalog)
    logger.info(
        f"Added {len(orders)} orders!\n[bold]All done![/]", extra={"markup": True}
    )
