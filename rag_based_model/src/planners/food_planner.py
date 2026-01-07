"""
Food planner using rule-based logic and guideline-based recommendations.
Generates personalized meal plans for diabetes management.
"""

from typing import Dict, Any, List
import json


class FoodPlanner:
    """
    Rule-based food planning for diabetes management.
    Uses ADA guidelines and deterministic logic.
    """
    
    # Regional food databases
    INDIAN_FOODS = {
        "breakfast": {
            "low_gi": ["vegetable oats", "moong dal chilla", "idli with sambar", "poha with vegetables"],
            "high_fiber": ["oats upma", "ragi dosa", "quinoa idli"]
        },
        "lunch": {
            "grains": ["brown rice", "quinoa", "millets", "whole wheat chapati"],
            "proteins": ["dal (lentils)", "chickpea curry", "paneer", "tofu"],
            "vegetables": ["mixed vegetable curry", "palak (spinach)", "bhindi (okra)", "broccoli"]
        },
        "dinner": {
            "light_options": ["vegetable soup", "chapati with dal", "vegetable khichdi", "grilled paneer with vegetables"]
        },
        "snacks": {
            "healthy": ["roasted chana", "nuts (almonds, walnuts)", "sprouts", "cucumber with hummus", "low-GI fruits (apple, pear, berries)"]
        }
    }
    
    WESTERN_FOODS = {
        "breakfast": {
            "low_gi": ["steel-cut oats", "whole grain toast with avocado", "Greek yogurt with berries"],
            "high_fiber": ["oatmeal with nuts", "whole grain cereal with almond milk"]
        },
        "lunch": {
            "grains": ["quinoa", "brown rice", "whole wheat pasta", "barley"],
            "proteins": ["grilled chicken breast", "baked fish", "lentil soup", "chickpeas"],
            "vegetables": ["mixed green salad", "steamed broccoli", "roasted vegetables"]
        },
        "dinner": {
            "light_options": ["grilled salmon with vegetables", "chicken stir-fry", "lentil soup", "vegetable and bean chili"]
        },
        "snacks": {
            "healthy": ["almonds", "carrot sticks with hummus", "apple slices", "hard-boiled eggs"]
        }
    }
    
    def __init__(self):
        """Initialize food planner."""
        self.rules_applied = []
    
    def plan_meals(
        self,
        user_profile: Dict[str, Any],
        health_data: Dict[str, Any],
        guidelines: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate personalized meal plan based on rules and guidelines.
        
        Args:
            user_profile: User demographics and preferences
            health_data: Current health metrics
            guidelines: Retrieved clinical guidelines
            
        Returns:
            Structured meal plan with justification
        """
        self.rules_applied = []
        
        # Determine region-specific foods
        region = user_profile.get("region", "Western").lower()
        food_db = self.INDIAN_FOODS if "india" in region or "indian" in region else self.WESTERN_FOODS
        
        # Determine diet type
        diet_type = user_profile.get("diet_type", "").lower()
        
        # Apply planning rules
        plan = self._apply_planning_rules(user_profile, health_data, guidelines, food_db)
        
        # Generate meal recommendations
        meal_plan = self._generate_meal_recommendations(plan, food_db, diet_type)
        
        # Create justification
        justification = self._create_justification(health_data, guidelines)
        
        # Compile output
        output = {
            "meal_plan": meal_plan,
            "rules_applied": self.rules_applied,
            "justification": justification,
            "nutritional_focus": plan["focus_areas"],
            "foods_to_limit": self._get_foods_to_limit(guidelines)
        }
        
        return output
    
    def _apply_planning_rules(
        self,
        user_profile: Dict[str, Any],
        health_data: Dict[str, Any],
        guidelines: Dict[str, Any],
        food_db: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Apply rule-based logic for meal planning."""
        plan = {
            "focus_areas": [],
            "restrictions": [],
            "priorities": []
        }
        
        fasting = health_data.get("avg_fasting_glucose", 0)
        post_meal = health_data.get("avg_post_meal_glucose", 0)
        
        # Rule 1: High glucose → Low GI foods
        if fasting > 130 or post_meal > 180:
            plan["focus_areas"].append("low_glycemic_index")
            plan["priorities"].append("carbohydrate_control")
            self.rules_applied.append("High glucose levels → Prioritize low GI foods")
        
        # Rule 2: Always emphasize fiber
        plan["focus_areas"].append("high_fiber")
        self.rules_applied.append("ADA guideline → Minimum 25-30g fiber per day")
        
        # Rule 3: Reduce refined carbohydrates
        if post_meal > 180:
            plan["restrictions"].append("refined_carbs")
            self.rules_applied.append("Post-meal glucose elevated → Limit refined carbohydrates")
        
        # Rule 4: Portion control for high glucose
        if fasting > 150:
            plan["priorities"].append("portion_control")
            self.rules_applied.append("Fasting glucose significantly elevated → Emphasize portion control")
        
        return plan
    
    def _generate_meal_recommendations(
        self,
        plan: Dict[str, Any],
        food_db: Dict[str, Any],
        diet_type: str
    ) -> Dict[str, Any]:
        """Generate specific meal recommendations."""
        meals = {}
        
        # Breakfast
        if "low_glycemic_index" in plan["focus_areas"]:
            meals["breakfast"] = self._select_meal(food_db["breakfast"]["low_gi"])
        else:
            meals["breakfast"] = self._select_meal(
                food_db["breakfast"].get("high_fiber", food_db["breakfast"]["low_gi"])
            )
        
        # Lunch
        lunch_components = []
        
        # Grain selection
        if "carbohydrate_control" in plan["priorities"]:
            lunch_components.append(f"Small portion of {food_db['lunch']['grains'][0]}")
        else:
            lunch_components.append(f"{food_db['lunch']['grains'][0]}")
        
        # Protein
        proteins = food_db["lunch"]["proteins"]
        if "vegetarian" in diet_type or "vegan" in diet_type:
            proteins = [p for p in proteins if not any(meat in p.lower() for meat in ["chicken", "fish", "meat"])]
        
        lunch_components.append(proteins[0] if proteins else food_db["lunch"]["proteins"][0])
        
        # Vegetables (always emphasize)
        lunch_components.append(food_db["lunch"]["vegetables"][0])
        
        meals["lunch"] = ", ".join(lunch_components)
        
        # Dinner (lighter than lunch)
        meals["dinner"] = self._select_meal(food_db["dinner"]["light_options"])
        
        # Snacks
        meals["snacks"] = ", ".join(food_db["snacks"]["healthy"][:3])
        
        return meals
    
    def _select_meal(self, options: List[str]) -> str:
        """Select first meal option (can be randomized if needed)."""
        return options[0] if options else "Whole grain option with vegetables"
    
    def _create_justification(
        self,
        health_data: Dict[str, Any],
        guidelines: Dict[str, Any]
    ) -> str:
        """Create human-readable justification for meal plan."""
        justifications = []
        
        fasting = health_data.get("avg_fasting_glucose")
        post_meal = health_data.get("avg_post_meal_glucose")
        
        if fasting and fasting > 130:
            target = guidelines.get("safety_thresholds", {}).get("fasting_glucose", {})
            target_max = target.get("target_max", 130)
            justifications.append(
                f"Your average fasting glucose ({fasting} mg/dL) exceeds the ADA target range (80-{target_max} mg/dL)"
            )
        
        if post_meal and post_meal > 180:
            justifications.append(
                f"Your average post-meal glucose ({post_meal} mg/dL) is above the recommended target (<180 mg/dL)"
            )
        
        justifications.append(
            "This meal plan emphasizes low glycemic index foods and high fiber content as recommended by ADA guidelines"
        )
        
        return ". ".join(justifications) + "."
    
    def _get_foods_to_limit(self, guidelines: Dict[str, Any]) -> List[str]:
        """Extract foods to avoid from guidelines."""
        diet_guidelines = guidelines.get("diet_guidelines", {})
        avoid_list = diet_guidelines.get("avoid", [])
        
        return avoid_list if avoid_list else [
            "refined carbohydrates (white bread, white rice)",
            "sugary beverages",
            "added sugars and desserts",
            "processed foods high in sodium"
        ]


def create_food_plan(
    user_profile: Dict[str, Any],
    health_data: Dict[str, Any],
    guidelines: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Convenience function to create food plan.
    
    Args:
        user_profile: User demographics and preferences
        health_data: Current health metrics
        guidelines: Clinical guidelines from RAG
        
    Returns:
        Complete food plan
    """
    planner = FoodPlanner()
    return planner.plan_meals(user_profile, health_data, guidelines)


if __name__ == "__main__":
    # Example usage
    user_profile = {
        "age": 45,
        "diet_type": "vegetarian",
        "region": "India"
    }
    
    health_data = {
        "avg_fasting_glucose": 160,
        "avg_post_meal_glucose": 210
    }
    
    # Mock guidelines (would come from RAG in real usage)
    guidelines = {
        "diet_guidelines": {
            "carbs": "low glycemic index",
            "fiber": ">=25g/day",
            "avoid": ["sugary drinks", "refined carbs"]
        },
        "safety_thresholds": {
            "fasting_glucose": {"target_max": 130},
            "post_meal_glucose": {"target": 180}
        }
    }
    
    plan = create_food_plan(user_profile, health_data, guidelines)
    
    print("Food Plan Generated:")
    print("="*60)
    print(json.dumps(plan, indent=2))