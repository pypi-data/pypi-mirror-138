"""Processing of json file and adding orders"""
import logging

from openpyxl import Workbook

from kiraak.api import get_catalog, login
from kiraak.config import Config

logger = logging.getLogger(__name__)

# Login
logger.info(f"Logging in as {Config.MOBILE}")
partner_info = login(Config.MOBILE, Config.PASSWORD)
logger.info(
    f"Logged in as {partner_info['partnerName']} @ {partner_info['partnerBrand']}"
)

# Get and print catalog
logger.info("Fetching catalog...")
catalog = get_catalog()
logger.info(f"Recieved catalog (id {catalog['_id']})")

wb = Workbook()
ws = wb.active
ws.title = "catalog"
ws.append(
    ["Product ID", "Product Name", "Description", "Price", "Base quantity", "In Stock?"]
)
for product in catalog["productList"]:
    prodId = product["productId"]
    ws.append(
        [
            product["_id"],
            prodId["productName"],
            prodId["productDescription"],
            "₹" + product["productPrice"],
            product["productBaseQuantity"],
            str(product["productAvailability"] == "instock"),
        ]
    )

wb.save("catalog.xlsx")
