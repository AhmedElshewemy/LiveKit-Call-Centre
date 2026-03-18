import sqlite3
from typing import Optional
from dataclasses import dataclass
from contextlib import contextmanager

@dataclass
class SeafoodProduct:
    product_id: str
    supplier: str
    type: str
    harvest_date: str

@dataclass
class MenuItem:
    dish_id: int
    dish_name: str
    arabic_name: str
    category: str
    price: float
    description: str
    arabic_description: str
    ingredients: str
    allergens: str
    availability: str

class DatabaseDriver:
    def __init__(self, db_path: str = "seafood_db.sqlite"):
        self.db_path = db_path
        self._init_db()

    @contextmanager
    def _get_connection(self):
        conn = sqlite3.connect(self.db_path)
        try:
            yield conn
        finally:
            conn.close()

    def _init_db(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # Create seafood_products table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS seafood_products (
                    product_id TEXT PRIMARY KEY,
                    supplier TEXT NOT NULL,
                    type TEXT NOT NULL,
                    harvest_date TEXT NOT NULL
                )
            """)
            
            # Create menu_items table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS menu_items (
                    dish_id INTEGER PRIMARY KEY,
                    dish_name TEXT NOT NULL,
                    arabic_name TEXT,
                    category TEXT NOT NULL,
                    price REAL NOT NULL,
                    description TEXT NOT NULL,
                    arabic_description TEXT,
                    ingredients TEXT NOT NULL,
                    allergens TEXT,
                    availability TEXT NOT NULL
                )
            """)
            conn.commit()

    def create_seafood_product(self, product_id: str, supplier: str, type: str, harvest_date: str) -> SeafoodProduct:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO seafood_products (product_id, supplier, type, harvest_date) VALUES (?, ?, ?, ?)",
                (product_id, supplier, type, harvest_date)
            )
            conn.commit()
            return SeafoodProduct(product_id=product_id, supplier=supplier, type=type, harvest_date=harvest_date)

    def get_seafood_by_product_id(self, product_id: str) -> Optional[SeafoodProduct]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM seafood_products WHERE product_id = ?", (product_id,))
            row = cursor.fetchone()
            if not row:
                return None
            
            return SeafoodProduct(
                product_id=row[0],
                supplier=row[1],
                type=row[2],
                harvest_date=row[3]
            )

    def load_menu_from_csv(self, csv_file_path: str):
        """Load menu items from CSV file"""
        import csv
        with self._get_connection() as conn:
            cursor = conn.cursor()
            # Clear existing menu items
            cursor.execute("DELETE FROM menu_items")
            
            with open(csv_file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    cursor.execute(
                        """INSERT INTO menu_items 
                           (dish_id, dish_name, arabic_name, category, price, description, arabic_description, ingredients, allergens, availability)
                           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                        (int(row['dish_id']), row['dish_name'], row.get('arabic_name', ''), row['category'], float(row['price']), 
                         row['description'], row.get('arabic_description', ''), row['ingredients'], row['allergens'], row['availability'])
                    )
            conn.commit()

    def get_menu_item_by_id(self, dish_id: int) -> Optional[MenuItem]:
        """Get a menu item by its ID"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM menu_items WHERE dish_id = ?", (dish_id,))
            row = cursor.fetchone()
            if not row:
                return None
            
            return MenuItem(
                dish_id=row[0],
                dish_name=row[1],
                arabic_name=row[2],
                category=row[3],
                price=row[4],
                description=row[5],
                arabic_description=row[6],
                ingredients=row[7],
                allergens=row[8],
                availability=row[9]
            )

    def get_menu_items_by_category(self, category: str) -> list:
        """Get all menu items in a specific category"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM menu_items WHERE category = ?", (category,))
            rows = cursor.fetchall()
            
            items = []
            for row in rows:
                items.append(MenuItem(
                    dish_id=row[0],
                    dish_name=row[1],
                    arabic_name=row[2],
                    category=row[3],
                    price=row[4],
                    description=row[5],
                    arabic_description=row[6],
                    ingredients=row[7],
                    allergens=row[8],
                    availability=row[9]
                ))
            return items

    def search_menu_by_name(self, dish_name: str) -> list:
        """Search menu items by name"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM menu_items WHERE dish_name LIKE ? OR arabic_name LIKE ?", (f"%{dish_name}%", f"%{dish_name}%"))
            rows = cursor.fetchall()
            
            items = []
            for row in rows:
                items.append(MenuItem(
                    dish_id=row[0],
                    dish_name=row[1],
                    arabic_name=row[2],
                    category=row[3],
                    price=row[4],
                    description=row[5],
                    arabic_description=row[6],
                    ingredients=row[7],
                    allergens=row[8],
                    availability=row[9]
                ))
            return items

    def get_all_menu_items(self) -> list:
        """Get all menu items"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM menu_items")
            rows = cursor.fetchall()
            
            items = []
            for row in rows:
                items.append(MenuItem(
                    dish_id=row[0],
                    dish_name=row[1],
                    arabic_name=row[2],
                    category=row[3],
                    price=row[4],
                    description=row[5],
                    arabic_description=row[6],
                    ingredients=row[7],
                    allergens=row[8],
                    availability=row[9]
                ))
            return items
