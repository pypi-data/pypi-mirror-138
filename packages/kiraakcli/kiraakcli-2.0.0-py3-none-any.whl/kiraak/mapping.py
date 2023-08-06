import logging
import sys
import typing as t

from kiraak.difflib import get_close_matches
from kiraak.catalog import Product, Catalog

from kiraak.order import OrderList

from rich.table import Table
from click import confirm
from kiraak import console
from kiraak.catalog import Catalog, Product

logger = logging.getLogger(__name__)


class Mapping:
    def __init__(self, orderlist: OrderList, catalog: Catalog) -> None:
        self.map: t.Dict[str, Product] = {}
        self.orders = orderlist
        self.catalog = catalog

    def match(self, prod, conf=True):
        """Gets the closest match to a product"""
        close_matches = get_close_matches(prod, self.catalog, len(self.catalog), 0)
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
                return res
            if inp == "s":
                return None
            if inp == "name":
                return self.match(input("Enter name of product: "))
            logger.error("Skipping...")

    def initialize_mapping(self) -> None:
        for oproduct in self.orders.unique_names:
            self.map[oproduct] = self.match(oproduct, conf=False)

    def confirm(self) -> None:
        while True:
            tbl = Table("Number", "Order Product", "Catalog Product", "Catalog Description", "Catalog Size")
            for i, map_ in enumerate(self.map.items()):
                order_prod, catalog_prod = map_
                tbl.add_row(
                    str(i),
                    order_prod,
                    catalog_prod.name,
                    catalog_prod.desc,
                    catalog_prod.quantity
)

            console.print(tbl)
            if confirm("Edit mapping?", default=True):
                while True:
                    num = int(input("Enter number of product to edit: "))
                    product = list(self.map.keys())[num]
                    self.map[product] = self.match(product)
                    if not confirm("Continue editing?", default=True):
                        break
            else:
                break

    def __getitem__(self, key) -> Product:
        return self.map[key]