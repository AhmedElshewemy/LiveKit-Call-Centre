#!/usr/bin/env python3
"""
Menu data loader script for the Seafood Restaurant AI assistant.
This script loads menu items from a CSV file into the database.

Usage:
    python load_menu.py [csv_file_path]

If no csv_file_path is provided, it will look for menu_data.csv in the same directory.
"""

import sys
import os
from db_driver import DatabaseDriver

def load_menu(csv_file_path="menu_data.csv"):
    """Load menu from CSV file into database"""
    
    # Check if file exists
    if not os.path.exists(csv_file_path):
        print(f"Error: File not found: {csv_file_path}")
        return False
    
    try:
        db = DatabaseDriver()
        db.load_menu_from_csv(csv_file_path)
        print(f"✓ Menu loaded successfully from: {csv_file_path}")
        
        # Show what was loaded
        items = db.get_all_menu_items()
        print(f"✓ Total items loaded: {len(items)}")
        
        # Group by category
        categories = {}
        for item in items:
            if item.category not in categories:
                categories[item.category] = []
            categories[item.category].append(item.dish_name)
        
        print("\nMenu Summary:")
        for category, dishes in sorted(categories.items()):
            print(f"  • {category}: {len(dishes)} items")
        
        return True
    except Exception as e:
        print(f"Error loading menu: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        csv_file = sys.argv[1]
    else:
        csv_file = "menu_data.csv"
    
    success = load_menu(csv_file)
    sys.exit(0 if success else 1)
