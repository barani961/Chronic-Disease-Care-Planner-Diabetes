"""
FIXED Dynamic food planner with proper meal variety and selection logic.
"""

from typing import Dict, Any, List, Optional
import random


class DynamicFoodDatabase:
    """Extensible food database with dynamic filtering."""
    
    def __init__(self):
        self.foods = self._initialize_database()
    
    def _initialize_database(self) -> Dict[str, List[Dict[str, Any]]]:
        """Initialize comprehensive food database."""
        return {
            "grains": [
                {"name": "brown rice", "gi": "medium", "region": ["indian", "asian", "western"], "vegan": True, "gluten_free": True, "fiber": "medium"},
                {"name": "quinoa", "gi": "low", "region": ["western", "south_american"], "vegan": True, "gluten_free": True, "fiber": "high"},
                {"name": "whole wheat chapati", "gi": "medium", "region": ["indian"], "vegan": True, "gluten_free": False, "fiber": "high"},
                {"name": "oats", "gi": "low", "region": ["western", "indian"], "vegan": True, "gluten_free": True, "fiber": "high"},
                {"name": "millets (ragi, bajra)", "gi": "low", "region": ["indian"], "vegan": True, "gluten_free": True, "fiber": "high"},
                {"name": "barley", "gi": "low", "region": ["western", "middle_eastern"], "vegan": True, "gluten_free": False, "fiber": "high"},
                {"name": "whole wheat pasta", "gi": "medium", "region": ["western", "italian"], "vegan": True, "gluten_free": False, "fiber": "medium"},
            ],
            "proteins": [
                {"name": "lentils (dal)", "gi": "low", "region": ["indian", "middle_eastern"], "vegan": True, "type": "plant", "fiber": "high"},
                {"name": "chickpeas", "gi": "low", "region": ["indian", "middle_eastern", "mediterranean"], "vegan": True, "type": "plant", "fiber": "high"},
                {"name": "black beans", "gi": "low", "region": ["latin_american", "western"], "vegan": True, "type": "plant", "fiber": "high"},
                {"name": "tofu", "gi": "low", "region": ["asian", "western"], "vegan": True, "type": "plant", "fiber": "low"},
                {"name": "paneer (low-fat)", "gi": "low", "region": ["indian"], "vegan": False, "vegetarian": True, "type": "dairy", "fiber": "none"},
                {"name": "greek yogurt", "gi": "low", "region": ["western", "mediterranean"], "vegan": False, "vegetarian": True, "type": "dairy", "fiber": "none"},
                {"name": "eggs", "gi": "low", "region": ["universal"], "vegan": False, "vegetarian": True, "type": "animal", "fiber": "none"},
                {"name": "chicken breast (grilled)", "gi": "low", "region": ["universal"], "vegan": False, "vegetarian": False, "type": "meat", "fiber": "none"},
                {"name": "fish (salmon, mackerel)", "gi": "low", "region": ["universal"], "vegan": False, "vegetarian": False, "type": "seafood", "fiber": "none"},
                {"name": "tempeh", "gi": "low", "region": ["asian"], "vegan": True, "type": "plant", "fiber": "high"},
                {"name": "kidney beans", "gi": "low", "region": ["indian", "latin_american"], "vegan": True, "type": "plant", "fiber": "high"},
                {"name": "moong dal", "gi": "low", "region": ["indian"], "vegan": True, "type": "plant", "fiber": "high"},
            ],
            "vegetables": [
                {"name": "spinach (palak)", "gi": "low", "region": ["universal"], "vegan": True, "fiber": "high", "type": "leafy_green"},
                {"name": "broccoli", "gi": "low", "region": ["universal"], "vegan": True, "fiber": "high", "type": "cruciferous"},
                {"name": "cauliflower", "gi": "low", "region": ["universal"], "vegan": True, "fiber": "high", "type": "cruciferous"},
                {"name": "bell peppers", "gi": "low", "region": ["universal"], "vegan": True, "fiber": "medium", "type": "non_starchy"},
                {"name": "okra (bhindi)", "gi": "low", "region": ["indian", "southern_us"], "vegan": True, "fiber": "high", "type": "non_starchy"},
                {"name": "eggplant (baingan)", "gi": "low", "region": ["indian", "mediterranean"], "vegan": True, "fiber": "medium", "type": "non_starchy"},
                {"name": "tomatoes", "gi": "low", "region": ["universal"], "vegan": True, "fiber": "medium", "type": "non_starchy"},
                {"name": "cucumber", "gi": "low", "region": ["universal"], "vegan": True, "fiber": "low", "type": "non_starchy"},
                {"name": "carrots", "gi": "medium", "region": ["universal"], "vegan": True, "fiber": "medium", "type": "root"},
                {"name": "green beans", "gi": "low", "region": ["universal"], "vegan": True, "fiber": "medium", "type": "non_starchy"},
                {"name": "zucchini", "gi": "low", "region": ["western", "mediterranean"], "vegan": True, "fiber": "medium", "type": "non_starchy"},
                {"name": "cabbage", "gi": "low", "region": ["universal"], "vegan": True, "fiber": "high", "type": "cruciferous"},
                {"name": "bitter gourd (karela)", "gi": "low", "region": ["indian"], "vegan": True, "fiber": "medium", "type": "non_starchy"},
            ],
            "fruits": [
                {"name": "berries (strawberries, blueberries)", "gi": "low", "region": ["universal"], "vegan": True, "fiber": "high"},
                {"name": "apple", "gi": "low", "region": ["universal"], "vegan": True, "fiber": "high"},
                {"name": "pear", "gi": "low", "region": ["universal"], "vegan": True, "fiber": "high"},
                {"name": "orange", "gi": "low", "region": ["universal"], "vegan": True, "fiber": "medium"},
                {"name": "guava", "gi": "low", "region": ["indian", "tropical"], "vegan": True, "fiber": "high"},
            ],
            "snacks": [
                {"name": "almonds", "gi": "low", "region": ["universal"], "vegan": True, "fiber": "high", "type": "nuts"},
                {"name": "walnuts", "gi": "low", "region": ["universal"], "vegan": True, "fiber": "medium", "type": "nuts"},
                {"name": "roasted chana", "gi": "low", "region": ["indian"], "vegan": True, "fiber": "high", "type": "legume"},
                {"name": "hummus with vegetables", "gi": "low", "region": ["middle_eastern", "western"], "vegan": True, "fiber": "high", "type": "dip"},
                {"name": "sprouts", "gi": "low", "region": ["indian"], "vegan": True, "fiber": "high", "type": "legume"},
                {"name": "greek yogurt (unsweetened)", "gi": "low", "region": ["western"], "vegan": False, "vegetarian": True, "fiber": "none", "type": "dairy"},
            ],
        }
    
    def filter_foods(
        self,
        category: str,
        diet_type: Optional[str] = None,
        region: Optional[str] = None,
        gi_preference: Optional[str] = "low",
        exclude_ingredients: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """Dynamically filter foods based on multiple criteria."""
        if category not in self.foods:
            return []
        
        foods = self.foods[category].copy()
        exclude_ingredients = exclude_ingredients or []
        
        # Filter by diet type
        if diet_type:
            if diet_type == "vegan":
                foods = [f for f in foods if f.get("vegan", False)]
            elif diet_type == "vegetarian":
                foods = [f for f in foods if f.get("vegan", False) or f.get("vegetarian", False)]
            elif diet_type == "pescatarian":
                foods = [f for f in foods if f.get("vegan", False) or f.get("vegetarian", False) or f.get("type") == "seafood"]
        
        # Filter by region
        if region:
            region_lower = region.lower()
            foods = [f for f in foods if region_lower in [r.lower() for r in f.get("region", [])] or "universal" in f.get("region", [])]
        
        # Filter by GI preference
        if gi_preference:
            foods = [f for f in foods if f.get("gi", "medium") == gi_preference or f.get("gi") == "low"]
        
        # Exclude specific ingredients
        for exclude in exclude_ingredients:
            foods = [f for f in foods if exclude.lower() not in f["name"].lower()]
        
        return foods
    
    def add_custom_food(self, category: str, food_data: Dict[str, Any]):
        """Allow users to add custom foods."""
        if category not in self.foods:
            self.foods[category] = []
        self.foods[category].append(food_data)


class DynamicFoodPlanner:
    """Advanced food planner with true meal variety."""
    
    def __init__(self):
        self.food_db = DynamicFoodDatabase()
        self.rules_applied = []
        self.used_foods = []  # Track used foods for variety
    
    def plan_meals(
        self,
        user_profile: Dict[str, Any],
        health_data: Dict[str, Any],
        guidelines: Dict[str, Any],
        preferences: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Generate fully personalized meal plan with variety."""
        self.rules_applied = []
        self.used_foods = []  # Reset for each plan
        preferences = preferences or {}
        
        # Extract parameters
        diet_type = user_profile.get("diet_type", "omnivore")
        region = user_profile.get("region", "western")
        allergies = preferences.get("allergies", [])
        dislikes = preferences.get("dislikes", [])
        liked_foods = preferences.get("liked_foods", [])
        
        # Analyze health data
        health_analysis = self._analyze_health_data(health_data, guidelines)
        
        # Generate varied meal plan
        meal_plan = {
            "breakfast": self._generate_meal(
                "breakfast", diet_type, region, health_analysis, allergies, dislikes, liked_foods
            ),
            "morning_snack": self._generate_snack(
                diet_type, region, health_analysis, allergies, dislikes
            ),
            "lunch": self._generate_meal(
                "lunch", diet_type, region, health_analysis, allergies, dislikes, liked_foods
            ),
            "afternoon_snack": self._generate_snack(
                diet_type, region, health_analysis, allergies, dislikes
            ),
            "dinner": self._generate_meal(
                "dinner", diet_type, region, health_analysis, allergies, dislikes, liked_foods
            ),
        }
        
        # Generate shopping list
        shopping_list = self._generate_shopping_list(meal_plan)
        
        # Create justification
        justification = self._create_justification(health_data, health_analysis, guidelines)
        
        return {
            "meal_plan": meal_plan,
            "shopping_list": shopping_list,
            "rules_applied": self.rules_applied,
            "justification": justification,
            "nutritional_goals": health_analysis["goals"],
            "foods_to_emphasize": health_analysis["emphasize"],
            "foods_to_limit": health_analysis["limit"]
        }
    
    def _analyze_health_data(
        self,
        health_data: Dict[str, Any],
        guidelines: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Analyze health data to determine nutritional needs."""
        analysis = {
            "gi_preference": "low",
            "fiber_priority": "high",
            "portion_control": False,
            "goals": [],
            "emphasize": [],
            "limit": []
        }
        
        fasting = health_data.get("avg_fasting_glucose", 0)
        post_meal = health_data.get("avg_post_meal_glucose", 0)
        
        # Rule 1: High glucose → Low GI focus
        if fasting > 130 or post_meal > 180:
            analysis["gi_preference"] = "low"
            analysis["goals"].append("Lower glycemic index foods to improve glucose control")
            self.rules_applied.append("Elevated glucose → Prioritize low GI foods")
        
        # Rule 2: Very high glucose → Strict portion control
        if fasting > 150:
            analysis["portion_control"] = True
            analysis["goals"].append("Portion control to manage blood sugar")
            self.rules_applied.append("Significantly elevated glucose → Emphasize portion control")
        
        # Rule 3: Always emphasize fiber
        analysis["fiber_priority"] = "high"
        analysis["emphasize"].extend(["High fiber foods", "Non-starchy vegetables", "Legumes"])
        self.rules_applied.append("ADA guideline → Minimum 25-30g fiber per day")
        
        # Rule 4: Post-meal spikes → Reduce refined carbs
        if post_meal > 180:
            analysis["limit"].extend(["Refined carbohydrates", "White bread", "White rice", "Sugary foods"])
            self.rules_applied.append("Post-meal glucose elevated → Limit refined carbohydrates")
        
        return analysis
    
    def _generate_meal(
        self,
        meal_type: str,
        diet_type: str,
        region: str,
        health_analysis: Dict[str, Any],
        allergies: List[str],
        dislikes: List[str],
        liked_foods: List[str]
    ) -> Dict[str, Any]:
        """Generate a meal with VARIETY - avoid repetition."""
        exclude = allergies + dislikes
        gi_pref = health_analysis["gi_preference"]
        
        meal = {"components": [], "portion_notes": []}
        
        # Get filtered foods
        grains = self.food_db.filter_foods("grains", diet_type, region, gi_pref, exclude)
        proteins = self.food_db.filter_foods("proteins", diet_type, region, gi_pref, exclude)
        vegetables = self.food_db.filter_foods("vegetables", diet_type, region, None, exclude)
        
        # Remove already used foods for variety
        grains = [g for g in grains if g["name"] not in self.used_foods]
        proteins = [p for p in proteins if p["name"] not in self.used_foods]
        vegetables = [v for v in vegetables if v["name"] not in self.used_foods]
        
        # If we've used everything, reset
        if not grains or not proteins:
            self.used_foods = []
            grains = self.food_db.filter_foods("grains", diet_type, region, gi_pref, exclude)
            proteins = self.food_db.filter_foods("proteins", diet_type, region, gi_pref, exclude)
        
        if meal_type == "breakfast":
            # Breakfast: grain + protein
            if grains:
                grain = self._select_preferred(grains, liked_foods)
                portion = "Small portion (1/2 cup)" if health_analysis["portion_control"] else "1 cup"
                meal["components"].append(f"{grain['name']} ({portion})")
                self.used_foods.append(grain["name"])
            
            if proteins:
                protein = self._select_preferred(proteins, liked_foods)
                meal["components"].append(protein["name"])
                self.used_foods.append(protein["name"])
        
        elif meal_type in ["lunch", "dinner"]:
            # Main meals: grain + protein + vegetables
            if grains:
                grain = self._select_preferred(grains, liked_foods)
                portion = "Small portion (1/2 cup)" if health_analysis["portion_control"] else "1 cup"
                meal["components"].append(f"{grain['name']} ({portion})")
                self.used_foods.append(grain["name"])
            
            if proteins:
                protein = self._select_preferred(proteins, liked_foods)
                meal["components"].append(protein["name"])
                self.used_foods.append(protein["name"])
            
            # Select 2 DIFFERENT vegetables
            if vegetables and len(vegetables) >= 2:
                random.shuffle(vegetables)  # Randomize for variety
                veg1 = vegetables[0]
                veg2 = vegetables[1]
                meal["components"].append(f"{veg1['name']} and {veg2['name']}")
                self.used_foods.append(veg1["name"])
                self.used_foods.append(veg2["name"])
            elif vegetables:
                veg = vegetables[0]
                meal["components"].append(veg["name"])
                self.used_foods.append(veg["name"])
        
        meal["description"] = ", ".join(meal["components"]) if meal["components"] else "Whole grain with vegetables"
        return meal
    
    def _generate_snack(
        self,
        diet_type: str,
        region: str,
        health_analysis: Dict[str, Any],
        allergies: List[str],
        dislikes: List[str]
    ) -> Dict[str, Any]:
        """Generate healthy snack options."""
        exclude = allergies + dislikes
        
        snacks = self.food_db.filter_foods("snacks", diet_type, region, "low", exclude)
        fruits = self.food_db.filter_foods("fruits", diet_type, region, "low", exclude)
        
        options = []
        if snacks and snacks[0]["name"] not in self.used_foods:
            options.append(snacks[0]["name"])
        elif snacks and len(snacks) > 1:
            options.append(snacks[1]["name"])
        
        if fruits and len(options) < 2:
            fruit = [f for f in fruits if f["name"] not in self.used_foods]
            if fruit:
                options.append(f"{fruit[0]['name']} (1 small)")
        
        return {
            "options": options,
            "description": " OR ".join(options) if options else "Vegetable sticks with hummus"
        }
    
    def _select_preferred(
        self,
        food_list: List[Dict[str, Any]],
        liked_foods: List[str]
    ) -> Dict[str, Any]:
        """Select food, preferring user's liked foods."""
        if not food_list:
            return {"name": "unavailable"}
        
        # Check if any liked food is in the list
        for food in food_list:
            for liked in liked_foods:
                if liked.lower() in food["name"].lower():
                    return food
        
        # Otherwise return first unused option
        return food_list[0]
    
    def _generate_shopping_list(self, meal_plan: Dict[str, Any]) -> List[str]:
        """Extract unique ingredients for shopping."""
        ingredients = set()
        
        for meal_name, meal_data in meal_plan.items():
            if isinstance(meal_data, dict):
                components = meal_data.get("components", [])
                for component in components:
                    ingredient = component.split("(")[0].strip()
                    # Split "X and Y" into separate items
                    if " and " in ingredient:
                        parts = ingredient.split(" and ")
                        for part in parts:
                            ingredients.add(part.strip())
                    else:
                        ingredients.add(ingredient)
                
                options = meal_data.get("options", [])
                for option in options:
                    ingredient = option.split("(")[0].strip()
                    ingredients.add(ingredient)
        
        return sorted(list(ingredients))
    
    def _create_justification(
        self,
        health_data: Dict[str, Any],
        health_analysis: Dict[str, Any],
        guidelines: Dict[str, Any]
    ) -> str:
        """Create detailed justification."""
        parts = []
        
        fasting = health_data.get("avg_fasting_glucose")
        if fasting and fasting > 130:
            parts.append(f"Your average fasting glucose ({fasting} mg/dL) is above the ADA target range (80-130 mg/dL)")
        
        parts.extend(health_analysis["goals"])
        parts.append("All recommendations follow ADA nutritional guidelines for diabetes management")
        
        return ". ".join(parts) + "."


def create_dynamic_food_plan(
    user_profile: Dict[str, Any],
    health_data: Dict[str, Any],
    guidelines: Dict[str, Any],
    preferences: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Create dynamic, personalized food plan."""
    planner = DynamicFoodPlanner()
    return planner.plan_meals(user_profile, health_data, guidelines, preferences)