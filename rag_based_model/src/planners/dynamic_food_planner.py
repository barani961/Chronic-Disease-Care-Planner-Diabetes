"""
Dynamic food planner that generates personalized meal plans based on user preferences,
dietary restrictions, regional cuisine, and health goals.
"""

from typing import Dict, Any, List, Optional
import json


class DynamicFoodDatabase:
    """
    Extensible food database with dynamic filtering and recommendation.
    """
    
    def __init__(self):
        self.foods = self._initialize_database()
    
    def _initialize_database(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Initialize comprehensive food database with metadata.
        Can be extended with external APIs or databases.
        """
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
            ],
            "vegetables": [
                {"name": "spinach", "gi": "low", "region": ["universal"], "vegan": True, "fiber": "high", "type": "leafy_green"},
                {"name": "broccoli", "gi": "low", "region": ["universal"], "vegan": True, "fiber": "high", "type": "cruciferous"},
                {"name": "cauliflower", "gi": "low", "region": ["universal"], "vegan": True, "fiber": "high", "type": "cruciferous"},
                {"name": "bell peppers", "gi": "low", "region": ["universal"], "vegan": True, "fiber": "medium", "type": "non_starchy"},
                {"name": "okra (bhindi)", "gi": "low", "region": ["indian", "southern_us"], "vegan": True, "fiber": "high", "type": "non_starchy"},
                {"name": "eggplant (baingan)", "gi": "low", "region": ["indian", "mediterranean"], "vegan": True, "fiber": "medium", "type": "non_starchy"},
                {"name": "tomatoes", "gi": "low", "region": ["universal"], "vegan": True, "fiber": "medium", "type": "non_starchy"},
                {"name": "cucumber", "gi": "low", "region": ["universal"], "vegan": True, "fiber": "low", "type": "non_starchy"},
                {"name": "carrots", "gi": "medium", "region": ["universal"], "vegan": True, "fiber": "medium", "type": "root"},
                {"name": "green beans", "gi": "low", "region": ["universal"], "vegan": True, "fiber": "medium", "type": "non_starchy"},
            ],
            "fruits": [
                {"name": "berries (strawberries, blueberries)", "gi": "low", "region": ["universal"], "vegan": True, "fiber": "high"},
                {"name": "apples", "gi": "low", "region": ["universal"], "vegan": True, "fiber": "high"},
                {"name": "pears", "gi": "low", "region": ["universal"], "vegan": True, "fiber": "high"},
                {"name": "oranges", "gi": "low", "region": ["universal"], "vegan": True, "fiber": "medium"},
                {"name": "guava", "gi": "low", "region": ["indian", "tropical"], "vegan": True, "fiber": "high"},
                {"name": "papaya (small portion)", "gi": "medium", "region": ["tropical"], "vegan": True, "fiber": "medium"},
                {"name": "pomegranate", "gi": "medium", "region": ["indian", "middle_eastern"], "vegan": True, "fiber": "medium"},
            ],
            "snacks": [
                {"name": "almonds", "gi": "low", "region": ["universal"], "vegan": True, "fiber": "high", "type": "nuts"},
                {"name": "walnuts", "gi": "low", "region": ["universal"], "vegan": True, "fiber": "medium", "type": "nuts"},
                {"name": "roasted chana", "gi": "low", "region": ["indian"], "vegan": True, "fiber": "high", "type": "legume"},
                {"name": "hummus with vegetables", "gi": "low", "region": ["middle_eastern", "western"], "vegan": True, "fiber": "high", "type": "dip"},
                {"name": "sprouts", "gi": "low", "region": ["indian"], "vegan": True, "fiber": "high", "type": "legume"},
                {"name": "Greek yogurt (unsweetened)", "gi": "low", "region": ["western"], "vegan": False, "vegetarian": True, "fiber": "none", "type": "dairy"},
            ],
            "fats": [
                {"name": "olive oil", "gi": "low", "region": ["mediterranean", "western"], "vegan": True, "type": "oil"},
                {"name": "avocado", "gi": "low", "region": ["western", "latin_american"], "vegan": True, "fiber": "high", "type": "fruit_fat"},
                {"name": "nuts and seeds", "gi": "low", "region": ["universal"], "vegan": True, "fiber": "high", "type": "nuts_seeds"},
            ]
        }
    
    def filter_foods(
        self,
        category: str,
        diet_type: Optional[str] = None,
        region: Optional[str] = None,
        gi_preference: Optional[str] = "low",
        exclude_ingredients: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Dynamically filter foods based on multiple criteria.
        
        Args:
            category: Food category (grains, proteins, vegetables, etc.)
            diet_type: vegan, vegetarian, omnivore, pescatarian
            region: indian, western, asian, mediterranean, etc.
            gi_preference: low, medium (glycemic index)
            exclude_ingredients: List of ingredients to exclude (allergies, dislikes)
        
        Returns:
            Filtered list of foods
        """
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
            # omnivore = no filtering
        
        # Filter by region (prefer regional, but allow universal)
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
    """
    Advanced food planner that generates truly personalized meal plans.
    """
    
    def __init__(self):
        self.food_db = DynamicFoodDatabase()
        self.rules_applied = []
    
    def plan_meals(
        self,
        user_profile: Dict[str, Any],
        health_data: Dict[str, Any],
        guidelines: Dict[str, Any],
        preferences: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Generate fully personalized meal plan.
        
        Args:
            user_profile: Age, diet_type, region, activity_level
            health_data: Glucose readings, medical conditions
            guidelines: Retrieved clinical guidelines
            preferences: Optional user preferences (liked_foods, disliked_foods, allergies)
        
        Returns:
            Comprehensive meal plan
        """
        self.rules_applied = []
        preferences = preferences or {}
        
        # Extract user parameters
        diet_type = user_profile.get("diet_type", "omnivore")
        region = user_profile.get("region", "western")
        allergies = preferences.get("allergies", [])
        dislikes = preferences.get("dislikes", [])
        liked_foods = preferences.get("liked_foods", [])
        
        # Analyze health data and determine needs
        health_analysis = self._analyze_health_data(health_data, guidelines)
        
        # Generate meal plan
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
        
        # Rule 3: Always emphasize fiber (ADA guideline)
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
        """Generate a complete meal with components."""
        exclude = allergies + dislikes
        gi_pref = health_analysis["gi_preference"]
        
        meal = {"components": [], "portion_notes": []}
        
        if meal_type == "breakfast":
            # Grain + Protein/Fat
            grains = self.food_db.filter_foods("grains", diet_type, region, gi_pref, exclude)
            proteins = self.food_db.filter_foods("proteins", diet_type, region, gi_pref, exclude)
            
            if grains:
                grain = self._select_preferred(grains, liked_foods)
                portion = "Small portion (1/2 cup)" if health_analysis["portion_control"] else "1 cup"
                meal["components"].append(f"{grain['name']} ({portion})")
            
            if proteins:
                protein = self._select_preferred(proteins, liked_foods)
                meal["components"].append(protein["name"])
        
        elif meal_type in ["lunch", "dinner"]:
            # Grain + Protein + Vegetables
            grains = self.food_db.filter_foods("grains", diet_type, region, gi_pref, exclude)
            proteins = self.food_db.filter_foods("proteins", diet_type, region, gi_pref, exclude)
            vegetables = self.food_db.filter_foods("vegetables", diet_type, region, None, exclude)
            
            # Select different grain for lunch vs dinner
            if grains:
                if meal_type == "lunch":
                    grain = grains[0] if len(grains) > 0 else None
                else:  # dinner
                    grain = grains[1] if len(grains) > 1 else grains[0] if len(grains) > 0 else None
                
                if grain:
                    portion = "Small portion (1/2 cup)" if health_analysis["portion_control"] else "1 cup"
                    meal["components"].append(f"{grain['name']} ({portion})")
            
            # Select different protein for lunch vs dinner
            if proteins:
                if meal_type == "lunch":
                    protein = proteins[0] if len(proteins) > 0 else None
                else:  # dinner
                    protein = proteins[1] if len(proteins) > 1 else proteins[0] if len(proteins) > 0 else None
                
                if protein:
                    meal["components"].append(protein["name"])
            
            # Select 2 different vegetables
            if vegetables and len(vegetables) >= 2:
                veg1 = vegetables[0]
                veg2 = vegetables[1]
                meal["components"].append(f"{veg1['name']} and {veg2['name']}")
            elif vegetables:
                meal["components"].append(f"{vegetables[0]['name']}")
        
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
        if snacks:
            options.append(snacks[0]["name"])
        if fruits and len(options) < 2:
            options.append(f"{fruits[0]['name']} (1 small)")
        
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
        
        # Otherwise return first option
        return food_list[0]
    
    def _generate_shopping_list(self, meal_plan: Dict[str, Any]) -> List[str]:
        """Extract unique ingredients for shopping."""
        ingredients = set()
        
        for meal_name, meal_data in meal_plan.items():
            if isinstance(meal_data, dict):
                components = meal_data.get("components", [])
                for component in components:
                    # Extract base ingredient (remove portion info)
                    ingredient = component.split("(")[0].strip()
                    ingredients.add(ingredient)
                
                # Add snack options
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


# Convenience function
def create_dynamic_food_plan(
    user_profile: Dict[str, Any],
    health_data: Dict[str, Any],
    guidelines: Dict[str, Any],
    preferences: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Create dynamic, personalized food plan."""
    planner = DynamicFoodPlanner()
    return planner.plan_meals(user_profile, health_data, guidelines, preferences)


if __name__ == "__main__":
    # Test with various inputs
    test_cases = [
        {
            "name": "Vegan, Indian, High Glucose",
            "user_profile": {"age": 35, "diet_type": "vegan", "region": "indian", "activity_level": "moderate"},
            "health_data": {"avg_fasting_glucose": 170, "avg_post_meal_glucose": 220},
            "preferences": {"liked_foods": ["quinoa", "chickpeas"], "allergies": [], "dislikes": ["eggplant"]}
        },
        {
            "name": "Omnivore, Western, Normal Glucose",
            "user_profile": {"age": 50, "diet_type": "omnivore", "region": "western", "activity_level": "low"},
            "health_data": {"avg_fasting_glucose": 110, "avg_post_meal_glucose": 150},
            "preferences": {"liked_foods": ["salmon", "broccoli"], "allergies": ["nuts"], "dislikes": []}
        }
    ]
    
    guidelines = {
        "diet_guidelines": {"carbs": "low glycemic index", "fiber": ">=25g/day"},
        "safety_thresholds": {"fasting_glucose": {"target_max": 130}}
    }
    
    for test in test_cases:
        print(f"\n{'='*60}")
        print(f"Test Case: {test['name']}")
        print(f"{'='*60}")
        
        plan = create_dynamic_food_plan(
            test["user_profile"],
            test["health_data"],
            guidelines,
            test["preferences"]
        )
        
        print(f"\nBreakfast: {plan['meal_plan']['breakfast']['description']}")
        print(f"Lunch: {plan['meal_plan']['lunch']['description']}")
        print(f"Dinner: {plan['meal_plan']['dinner']['description']}")
        print(f"\nShopping List ({len(plan['shopping_list'])} items):")
        print(f"  {', '.join(plan['shopping_list'][:10])}...")