"""
Enhanced main entry point with dynamic input handling and personalized planning.
Supports flexible input formats and truly personalized care plans.
"""

import json
from pathlib import Path
from typing import Dict, Any

# Import dynamic modules
from src.rag.retrieve_guidelines import GuidelineRetriever
from src.planners.dynamic_food_planner import create_dynamic_food_plan
from src.planners.activity_planner import create_activity_plan
from src.utils.safety import SafetyChecker, create_safe_response
from src.utils.flexible_input_handler import FlexibleInputHandler


class DynamicChronicCarePlanner:
    """
    Enhanced care planner with dynamic input handling and personalization.
    """
    
    def __init__(self, index_dir: str = "data/faiss_index"):
        """Initialize with RAG system."""
        print("Initializing Dynamic Chronic Care Planner...")
        self.retriever = GuidelineRetriever(index_dir=index_dir)
        self.input_handler = FlexibleInputHandler()
        print("✓ RAG system and input handler loaded")
    
    def create_care_plan(self, raw_input: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create care plan from any input format.
        
        Args:
            raw_input: Flexible input format
            
        Returns:
            Complete personalized care plan
        """
        print("\n" + "="*60)
        print("CREATING DYNAMIC CARE PLAN")
        print("="*60)
        
        # Step 1: Process and normalize input
        print("\n1. Processing input...")
        user_data = self.input_handler.process_input(raw_input)
        
        validation = self.input_handler.get_validation_report()
        if not validation["valid"]:
            print(f"   ❌ Input validation failed:")
            for error in validation["errors"]:
                print(f"      - {error}")
            return {
                "error": "Invalid input data",
                "details": validation["errors"]
            }
        
        if validation["warnings"]:
            print(f"   ⚠ Warnings:")
            for warning in validation["warnings"]:
                print(f"      - {warning}")
        
        print("   ✓ Input processed and normalized")
        
        # Step 2: Safety check
        print("\n2. Performing safety checks...")
        health_data = user_data.get("health_data", {})
        safety_check = SafetyChecker.check_glucose_safety(health_data)
        print(f"   ✓ Safety level: {safety_check['level']}")
        if safety_check["flags"]:
            print(f"   ⚠ Flags: {', '.join(safety_check['flags'])}")
        
        # Step 3: Retrieve guidelines
        print("\n3. Retrieving clinical guidelines...")
        user_profile = user_data.get("user_profile", {})
        guidelines = self.retriever.extract_structured_guidelines(
            user_profile, health_data
        )
        print(f"   ✓ Guidelines retrieved from: {', '.join(guidelines['citations'])}")
        
        # Step 4: Generate personalized food plan
        print("\n4. Generating personalized food plan...")
        preferences = user_data.get("preferences", {})
        food_plan = create_dynamic_food_plan(
            user_profile, 
            health_data, 
            guidelines,
            preferences
        )
        print(f"   ✓ Food plan created with {len(food_plan['rules_applied'])} rules applied")
        print(f"   ✓ Shopping list has {len(food_plan['shopping_list'])} items")
        
        # Step 5: Generate activity plan
        print("\n5. Generating activity plan...")
        activity_plan = create_activity_plan(user_profile, health_data, guidelines)
        print(f"   ✓ Activity plan created with {len(activity_plan['rules_applied'])} rules applied")
        
        # Step 6: Compile complete plan
        print("\n6. Compiling complete personalized care plan...")
        complete_plan = {
            "user_profile": user_profile,
            "health_data": health_data,
            "preferences": preferences,
            "guidelines_used": {
                "glycemic_targets": guidelines["glycemic_targets"],
                "citations": guidelines["citations"]
            },
            "food_plan": food_plan,
            "activity_plan": activity_plan,
            "input_validation": validation
        }
        
        # Step 7: Add safety wrapper
        safe_response = create_safe_response(complete_plan, safety_check)
        
        print("   ✓ Care plan complete")
        print("\n" + "="*60)
        print("DYNAMIC CARE PLAN GENERATION COMPLETE")
        print("="*60 + "\n")
        
        return safe_response
    
    def create_plan_from_text(self, text: str) -> Dict[str, Any]:
        """
        Create care plan from natural language description.
        
        Args:
            text: Natural language input
            
        Returns:
            Complete care plan
        """
        print(f"Processing natural language input: '{text}'")
        parsed_input = self.input_handler.parse_natural_language_input(text)
        return self.create_care_plan(parsed_input)
    
    def update_plan_with_feedback(
        self,
        current_plan: Dict[str, Any],
        feedback: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Update care plan based on user feedback.
        
        Args:
            current_plan: Existing care plan
            feedback: User feedback (liked meals, exercise difficulty, etc.)
            
        Returns:
            Updated care plan
        """
        print("\n" + "="*60)
        print("UPDATING PLAN WITH USER FEEDBACK")
        print("="*60)
        
        # Extract user data from current plan
        user_data = {
            "user_profile": current_plan["plan"]["user_profile"],
            "health_data": current_plan["plan"]["health_data"],
            "preferences": current_plan["plan"].get("preferences", {})
        }
        
        # Update preferences based on feedback
        if "disliked_meals" in feedback:
            user_data["preferences"]["dislikes"] = user_data["preferences"].get("dislikes", []) + feedback["disliked_meals"]
        
        if "liked_meals" in feedback:
            user_data["preferences"]["liked_foods"] = user_data["preferences"].get("liked_foods", []) + feedback["liked_meals"]
        
        if "exercise_too_difficult" in feedback and feedback["exercise_too_difficult"]:
            # Lower activity level
            current_level = user_data["user_profile"].get("activity_level", "low")
            if current_level != "sedentary":
                levels = ["sedentary", "low", "moderate", "high"]
                current_index = levels.index(current_level)
                user_data["user_profile"]["activity_level"] = levels[max(0, current_index - 1)]
                print("   → Adjusting activity level down based on feedback")
        
        # Generate new plan
        return self.create_care_plan(user_data)


def demonstrate_flexibility():
    """Demonstrate the system's flexibility with various input formats."""
    print("\n" + "="*70)
    print("DEMONSTRATING DYNAMIC INPUT HANDLING")
    print("="*70)
    
    planner = DynamicChronicCarePlanner(index_dir="data/faiss_index")
    
    # Test Case 1: Structured input
    print("\n" + "="*70)
    print("TEST 1: Standard Structured Input")
    print("="*70)
    
    input1 = {
        "user_profile": {
            "age": 45,
            "diet_type": "vegetarian",
            "region": "indian",
            "activity_level": "low"
        },
        "health_data": {
            "avg_fasting_glucose": 160,
            "avg_post_meal_glucose": 210
        },
        "preferences": {
            "liked_foods": ["quinoa", "chickpeas"],
            "dislikes": ["eggplant"],
            "allergies": []
        }
    }
    
    plan1 = planner.create_care_plan(input1)
    display_plan_summary(plan1, "Vegetarian Indian")
    
    # Test Case 2: Flat unstructured input
    print("\n" + "="*70)
    print("TEST 2: Flat Unstructured Input")
    print("="*70)
    
    input2 = {
        "age": 52,
        "diet_type": "vegan",
        "region": "western",
        "fasting_glucose": 145,
        "postprandial_glucose": 190,
        "allergies": "nuts, soy",
        "liked_foods": "berries, oats, broccoli"
    }
    
    plan2 = planner.create_care_plan(input2)
    display_plan_summary(plan2, "Vegan Western")
    
    # Test Case 3: Natural language (basic)
    print("\n" + "="*70)
    print("TEST 3: Natural Language Input")
    print("="*70)
    
    nl_input = "I'm 38 years old, pescatarian from Mediterranean region, my fasting glucose is 155"
    plan3 = planner.create_plan_from_text(nl_input)
    display_plan_summary(plan3, "Pescatarian Mediterranean")


def display_plan_summary(plan: Dict[str, Any], label: str):
    """Display a concise summary of the care plan."""
    print(f"\n📋 CARE PLAN SUMMARY: {label}")
    print("-" * 60)
    
    if "error" in plan:
        print(f"❌ Error: {plan['error']}")
        return
    
    # Safety status
    print(f"\n🛡️  Safety Status: {plan['safety']['level'].upper()}")
    if plan['safety']['message']:
        print(f"   {plan['safety']['message']}")
    
    # Food plan
    food_plan = plan['plan']['food_plan']
    print(f"\n🍽️  MEALS:")
    print(f"   Breakfast: {food_plan['meal_plan']['breakfast']['description']}")
    print(f"   Lunch: {food_plan['meal_plan']['lunch']['description']}")
    print(f"   Dinner: {food_plan['meal_plan']['dinner']['description']}")
    
    # Shopping list preview
    shopping = food_plan['shopping_list']
    print(f"\n🛒 Shopping List ({len(shopping)} items):")
    print(f"   {', '.join(shopping[:8])}...")
    
    # Activity plan
    activity = plan['plan']['activity_plan']['activity_plan']
    print(f"\n🏃 ACTIVITY:")
    print(f"   Daily: {activity['daily_aerobic']['activity']} for {activity['daily_aerobic']['duration_minutes']} minutes")
    print(f"   Weekly: {activity['weekly_schedule']['aerobic_days']} days/week")
    
    # Rules applied
    rules = food_plan['rules_applied'] + plan['plan']['activity_plan']['rules_applied']
    print(f"\n📊 Rules Applied ({len(rules)}):")
    for rule in rules[:3]:
        print(f"   • {rule}")
    
    print("\n" + "-" * 60)


if __name__ == "__main__":
    # Run demonstration of flexibility
    demonstrate_flexibility()
    
    # Or run with specific input
    # planner = DynamicChronicCarePlanner()
    # my_input = {...}
    # plan = planner.create_care_plan(my_input)