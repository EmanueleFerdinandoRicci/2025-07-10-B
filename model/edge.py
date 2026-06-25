from dataclasses import dataclass

from model.product import Product


@dataclass
class Edge:
    p1: Product
    p2: Product
    peso1: int
    peso2: int