from livekit.agents import llm
import enum
from typing import Annotated
import logging
import os
from db_driver import DatabaseDriver

logger = logging.getLogger("user-data")
logger.setLevel(logging.INFO)

DB = DatabaseDriver()

# Load menu data on startup
menu_csv_path = os.path.join(os.path.dirname(__file__), "menu_data.csv")
if os.path.exists(menu_csv_path):
    try:
        DB.load_menu_from_csv(menu_csv_path)
        logger.info("Menu loaded successfully from %s", menu_csv_path)
    except Exception as e:
        logger.error("Failed to load menu from CSV: %s", e)


class SeafoodDetails(enum.Enum):
    ProductID = "product_id"
    Supplier = "supplier"
    Type = "type"
    HarvestDate = "harvest_date"
    

class AssistantFnc(llm.FunctionContext):
    def __init__(self):
        super().__init__()
        
        self._seafood_details = {
            SeafoodDetails.ProductID: "",
            SeafoodDetails.Supplier: "",
            SeafoodDetails.Type: "",
            SeafoodDetails.HarvestDate: ""
        }
    
    def get_seafood_str(self):
        seafood_str = ""
        for key, value in self._seafood_details.items():
            seafood_str += f"{key}: {value}\n"
            
        return seafood_str
    
    def has_seafood(self):
        return self._seafood_details[SeafoodDetails.ProductID] != ""
    
    @llm.ai_callable(description="lookup a seafood product by its product id")
    def lookup_seafood(self, product_id: Annotated[str, llm.TypeInfo(description="The product id of the seafood to lookup")]):
        logger.info("lookup seafood - product_id: %s", product_id)
        
        result = DB.get_seafood_by_product_id(product_id)
        if result is None:
            return "Seafood product not found"
        
        self._seafood_details = {
            SeafoodDetails.ProductID: result.product_id,
            SeafoodDetails.Supplier: result.supplier,
            SeafoodDetails.Type: result.type,
            SeafoodDetails.HarvestDate: result.harvest_date
        }
        
        return f"The seafood product details are: {self.get_seafood_str()}"
    
    @llm.ai_callable(description="get the details of the current seafood product")
    def get_seafood_details(self):
        logger.info("get seafood details")
        return f"The seafood product details are: {self.get_seafood_str()}"
    
    @llm.ai_callable(description="create a new seafood product")
    def create_seafood_product(
        self, 
        product_id: Annotated[str, llm.TypeInfo(description="The product id of the seafood")],
        supplier: Annotated[str, llm.TypeInfo(description="The supplier of the seafood")],
        type: Annotated[str, llm.TypeInfo(description="The type of the seafood (e.g. Salmon, Shrimp)")],
        harvest_date: Annotated[str, llm.TypeInfo(description="The harvest date of the seafood")]
    ):
        logger.info("create seafood product - product_id: %s, supplier: %s, type: %s, harvest_date: %s", product_id, supplier, type, harvest_date)
        result = DB.create_seafood_product(product_id, supplier, type, harvest_date)
        if result is None:
            return "Failed to create seafood product"
        
        self._seafood_details = {
            SeafoodDetails.ProductID: result.product_id,
            SeafoodDetails.Supplier: result.supplier,
            SeafoodDetails.Type: result.type,
            SeafoodDetails.HarvestDate: result.harvest_date
        }
        
        return "seafood product created!"
    
    def has_seafood(self):
        return self._seafood_details[SeafoodDetails.ProductID] != ""
    
    def _get_dish_name(self, item, lang: str = "en"):
        """Helper to get dish name in selected language"""
        return item.arabic_name if lang == "ar" and item.arabic_name else item.dish_name
    
    def _get_dish_desc(self, item, lang: str = "en"):
        """Helper to get dish description in selected language"""
        return item.arabic_description if lang == "ar" and item.arabic_description else item.description
    
    @llm.ai_callable(description="search for menu items by dish name in English or Arabic")
    def search_menu_by_name(self, dish_name: Annotated[str, llm.TypeInfo(description="The name or type of dish to search for")], language: Annotated[str, llm.TypeInfo(description="Language: 'en' for English or 'ar' for Arabic")] = "en"):
        logger.info("search menu - dish_name: %s, language: %s", dish_name, language)
        results = DB.search_menu_by_name(dish_name)
        
        if not results:
            no_found = "No menu items found matching" if language == "en" else "لم يتم العثور على عناصر قائمة"
            return f"{no_found} '{dish_name}'"
        
        menu_text = ""
        for item in results:
            name = self._get_dish_name(item, language)
            desc = self._get_dish_desc(item, language)
            menu_text += f"• {name} (${item.price}) - {desc}\n"
        
        return menu_text
    
    @llm.ai_callable(description="get menu items by category in English or Arabic")
    def get_menu_by_category(self, category: Annotated[str, llm.TypeInfo(description="The category to search (e.g., Mains, Appetizers, Soups, Salads)")], language: Annotated[str, llm.TypeInfo(description="Language: 'en' for English or 'ar' for Arabic")] = "en"):
        logger.info("get menu by category - category: %s, language: %s", category, language)
        results = DB.get_menu_items_by_category(category)
        
        if not results:
            no_items = f"No items found in the {category} category" if language == "en" else f"لا توجد عناصر في فئة {category}"
            return no_items
        
        menu_text = f"**{category}:**\n"
        for item in results:
            name = self._get_dish_name(item, language)
            desc = self._get_dish_desc(item, language)
            menu_text += f"• {name} (${item.price}) - {desc}\n"
        
        return menu_text
    
    @llm.ai_callable(description="get menu item details including allergens and ingredients in English or Arabic")
    def get_menu_item_details(self, dish_id: Annotated[int, llm.TypeInfo(description="The dish ID or name to get details for")], language: Annotated[str, llm.TypeInfo(description="Language: 'en' for English or 'ar' for Arabic")] = "en"):
        logger.info("get menu item details - dish_id: %s, language: %s", dish_id, language)
        try:
            dish_id_int = int(dish_id)
            item = DB.get_menu_item_by_id(dish_id_int)
        except:
            # If not a number, try searching by name
            results = DB.search_menu_by_name(str(dish_id))
            if not results:
                return "Dish not found" if language == "en" else "لم يتم العثور على الطبق"
            item = results[0]
        
        if not item:
            return "Dish not found" if language == "en" else "لم يتم العثور على الطبق"
        
        name = self._get_dish_name(item, language)
        desc = self._get_dish_desc(item, language)
        
        if language == "ar":
            allergen_label = "الحساسيات:"
            ingredient_label = "المكونات:"
            availability_label = "التوفر:"
            allergen_info = f"**{allergen_label}** {item.allergens}" if item.allergens else f"**{allergen_label}** لا توجد"
        else:
            allergen_label = "Allergens:"
            ingredient_label = "Ingredients:"
            availability_label = "Availability:"
            allergen_info = f"**{allergen_label}** {item.allergens}" if item.allergens else f"**{allergen_label}** None listed"
        
        ingredient_info = f"**{ingredient_label}** {item.ingredients}"
        availability_info = f"**{availability_label}** {item.availability}"
        
        return f"**{name}** (${item.price})\n{desc}\n\n{ingredient_info}\n{allergen_info}\n{availability_info}"
    
    @llm.ai_callable(description="get the full restaurant menu in English or Arabic")
    def get_full_menu(self, language: Annotated[str, llm.TypeInfo(description="Language: 'en' for English or 'ar' for Arabic")] = "en"):
        logger.info("get full menu - language: %s", language)
        items = DB.get_all_menu_items()
        
        if not items:
            return "Menu is currently empty" if language == "en" else "القائمة فارغة حالياً"
        
        menu_title = "**FULL MENU**" if language == "en" else "**القائمة الكاملة**"
        menu_text = f"{menu_title}\n\n"
        current_category = None
        
        for item in sorted(items, key=lambda x: (x.category, x.dish_name)):
            if current_category != item.category:
                current_category = item.category
                menu_text += f"\n**{item.category}:**\n"
            name = self._get_dish_name(item, language)
            menu_text += f"• {name} - ${item.price}\n"
        
        return menu_text