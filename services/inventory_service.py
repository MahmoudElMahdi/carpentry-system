from db.storage import Storage
from models.material import Material
from models.product import Product

class InventoryService:
    def __init__(self, storage: Storage):
        self.storage = storage

    def add_material(self, name: str, unit: str, cost: float) -> Material:
        material = Material(name=name, unit=unit, cost_per_unit=cost)
        self.storage.append('materials', material.to_dict())
        print(f"Material added: {name}")
        return material

    def add_product(self, name: str, price: float) -> Product:
        product = Product(name=name, sale_price=price)
        self.storage.append('products', product.to_dict())
        print(f"Product added: {name}")
        return product

    def list_materials(self):
        return [Material.from_dict(m) for m in self.storage.load('materials')]

    def list_products(self):
        return [Product.from_dict(p) for p in self.storage.load('products')]
