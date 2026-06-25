from dataclasses import dataclass


@dataclass
class Product:
    product_id:int
    product_name:str
    brand_id:int
    category_id:int
    model_year:int
    list_price:str

    def __hash__(self):
        return hash(self.product_id)

    def __str__(self):
        return f"{self.product_name}"