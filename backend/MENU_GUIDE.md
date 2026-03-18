# Restaurant Menu Management Guide

This guide explains how to manage the menu data for the Seafood Restaurant AI Assistant.

## Menu Format

The menu is stored as CSV data in `menu_data.csv` with the following columns:

| Column | Description | Example |
|--------|-------------|---------|
| `dish_id` | Unique identifier for the dish | 1 |
| `dish_name` | Name of the dish | Grilled Atlantic Salmon |
| `category` | Menu category | Mains |
| `price` | Price in USD | 24.99 |
| `description` | Dish description | Fresh Atlantic Salmon grilled with lemon butter sauce |
| `ingredients` | Comma-separated ingredients | Salmon;lemon;butter;herbs |
| `allergens` | Comma-separated allergens | Fish;Dairy |
| `availability` | Current availability | Available |

### Menu Categories

Standard categories include:
- **Appetizers** - Starters and small plates
- **Soups** - Soups and bisques
- **Salads** - Salads
- **Mains** - Main courses
- **Desserts** - Desserts (add as needed)

## How to Update the Menu

### Option 1: Direct CSV Edit

1. Open `menu_data.csv` in a text editor or spreadsheet application
2. Add, modify, or remove rows as needed
3. Save the file
4. Reload the menu using the load script:
   ```bash
   python load_menu.py
   ```

### Option 2: Using the Load Script

```bash
# Load the default menu_data.csv
python load_menu.py

# Load a custom CSV file
python load_menu.py my_menu.csv
```

## Sample Menu Entry

```csv
1,Grilled Atlantic Salmon,Mains,24.99,Fresh Atlantic Salmon grilled with lemon butter sauce,Salmon;lemon;butter;herbs,Fish;Dairy,Available
```

## Important Notes

### Allergens Field
Always list allergens separated by semicolons. Common allergens include:
- Fish
- Shellfish
- Crustaceans
- Dairy
- Eggs
- Gluten
- Alcohol
- Tree nuts
- Soy
- Sulfites

### Availability Field
Use one of:
- `Available` - Item is currently available
- `Out of Stock` - Item is temporarily unavailable
- `Seasonal` - Item is seasonal

### Ingredients Field
List ingredients separated by semicolons for clarity. This helps with allergen tracking and nutritional information.

## Menu Features Available to Customers

The AI assistant can help customers with:

1. **Search by name**: "Do you have salmon?"
2. **Browse by category**: "What appetizers do you have?"
3. **Allergen information**: "What are the allergens in the shrimp scampi?"
4. **Full menu**: "Show me your whole menu"
5. **Detailed information**: "Tell me more about the lobster tail"

## Example CSV Format

```csv
dish_id,dish_name,category,price,description,ingredients,allergens,availability
1,Grilled Atlantic Salmon,Mains,24.99,Fresh Atlantic Salmon grilled with lemon butter sauce,Salmon;lemon;butter;herbs,Fish;Dairy,Available
2,Pan-Seared Scallops,Mains,28.99,Large sea scallops seared to perfection with garlic,Scallops;garlic;olive oil;butter,Shellfish;Dairy,Available
3,Shrimp Saganaki,Appetizers,16.99,Shrimp with tomato sauce and melted feta cheese,Shrimp;feta;tomato;garlic,Shellfish;Dairy,Available
```

## Troubleshooting

### Menu not loading
- Check that `menu_data.csv` is in the same directory as `load_menu.py`
- Verify the CSV format is correct (check for missing commas)
- Look for encoding issues (should be UTF-8)

### Changes not appearing
- Make sure you run `load_menu.py` after editing the CSV
- Restart the server to reload the menu
- Check `seafood_db.sqlite` hasn't been corrupted

### Database issues
- Delete `seafood_db.sqlite` to reset the database
- Run `load_menu.py` again to reload fresh data
