import sqlite3
from typing import Optional, List
from src.domain.models import Supplier, Product, Order, OrderItem


class Repository:
    def __init__(self, db_path: str = "logistics.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS suppliers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT NOT NULL
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sku TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                quantity INTEGER DEFAULT 0,
                price REAL DEFAULT 0.0
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id TEXT NOT NULL,
                status TEXT DEFAULT 'pending',
                total REAL DEFAULT 0.0
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS order_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                sku TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                price REAL NOT NULL,
                FOREIGN KEY (order_id) REFERENCES orders(id)
            )
        """)
        
        conn.commit()
        conn.close()

    # Supplier operations
    def add_supplier(self, supplier: Supplier) -> int:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO suppliers (name, email, phone) VALUES (?, ?, ?)",
            (supplier.name, supplier.email, supplier.phone)
        )
        supplier_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return supplier_id

    def get_supplier(self, supplier_id: int) -> Optional[Supplier]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, email, phone FROM suppliers WHERE id = ?", (supplier_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Supplier(id=row[0], name=row[1], email=row[2], phone=row[3])
        return None

    # Product operations
    def add_product(self, product: Product) -> int:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO products (sku, name, quantity, price) VALUES (?, ?, ?, ?)",
            (product.sku, product.name, product.quantity, product.price)
        )
        product_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return product_id

    def get_product(self, product_id: int) -> Optional[Product]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id, sku, name, quantity, price FROM products WHERE id = ?", (product_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Product(id=row[0], sku=row[1], name=row[2], quantity=row[3], price=row[4])
        return None

    def get_product_by_sku(self, sku: str) -> Optional[Product]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id, sku, name, quantity, price FROM products WHERE sku = ?", (sku,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Product(id=row[0], sku=row[1], name=row[2], quantity=row[3], price=row[4])
        return None

    def update_product(self, product: Product):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE products SET quantity = ? WHERE id = ?",
            (product.quantity, product.id)
        )
        conn.commit()
        conn.close()

    # Order operations
    def add_order(self, order: Order) -> int:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO orders (customer_id, status, total) VALUES (?, ?, ?)",
            (order.customer_id, order.status, order.total)
        )
        order_id = cursor.lastrowid
        
        for item in order.items:
            cursor.execute(
                "INSERT INTO order_items (order_id, product_id, sku, quantity, price) VALUES (?, ?, ?, ?, ?)",
                (order_id, item.product_id, item.sku, item.quantity, item.price)
            )
        
        conn.commit()
        conn.close()
        return order_id

    def get_order(self, order_id: int) -> Optional[Order]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id, customer_id, status, total FROM orders WHERE id = ?", (order_id,))
        row = cursor.fetchone()
        
        if not row:
            conn.close()
            return None
        
        # Get order items
        cursor.execute("SELECT product_id, sku, quantity, price FROM order_items WHERE order_id = ?", (order_id,))
        item_rows = cursor.fetchall()
        items = [OrderItem(product_id=r[0], sku=r[1], quantity=r[2], price=r[3]) for r in item_rows]
        
        conn.close()
        return Order(id=row[0], customer_id=row[1], items=items, status=row[2], total=row[3])

    def update_order(self, order: Order):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE orders SET status = ? WHERE id = ?",
            (order.status, order.id)
        )
        conn.commit()
        conn.close()


# Global repository instance
_repo: Optional[Repository] = None


def get_repository() -> Repository:
    global _repo
    if _repo is None:
        _repo = Repository()
    return _repo
