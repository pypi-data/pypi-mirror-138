"""Processing of json file and adding orders"""
import json
import logging

from rich.table import Table

from kiraak import console
from kiraak.add_orders import add_orders
from kiraak.api import get_catalog, login
from kiraak.config import Config
from kiraak.catalog import Catalog
from kiraak.order import OrderList

logger = logging.getLogger(__name__)


# TODO: Finish this OOP approach for the program

def main(file: str) -> None:
    """Process files, adds orders"""

    # Login
    logger.info(f"Logging in as {Config.MOBILE}")
    partner_info = login(Config.MOBILE, Config.PASSWORD)
    logger.info(
        f"Logged in as {partner_info['partnerName']} @ {partner_info['partnerBrand']}"
    )

    # Get and print catalog
    logger.info("Fetching catalog...")
    catalog = Catalog(get_catalog())
    logger.info(f"Recieved catalog (id {catalog.id})")
    tbl = Table(
        "Product Name",
        "Description",
        "Price",
        "Base quantity",
        "In Stock?",
    )
    for product in catalog:
        tbl.add_row(
            product.name,
            product.desc,
            f"₹ {product.price}",
            product.quantity,
            str(product.stock),
        )
    console.print(tbl)

    # Process json file
    logger.info(f"Processing {file}")
    with open(file, "r") as file_obj:
        orders = OrderList(json.load(file_obj))
    logger.info(f"Processed {len(orders)} orders")

    logger.info(f"Adding {len(orders)} orders...")
    add_orders(orders, catalog)
    logger.info(
        f"Added {len(orders)} orders!\n[bold]All done![/]", extra={"markup": True}
    )
