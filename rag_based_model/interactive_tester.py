"""
Interactive tester for Chronic Care Planner.
Allows manual input of patient data to test different scenarios.
"""

import json
from main_dynamic import DynamicChronicCarePlanner


class InteractiveTester:
    """Interactive testing interface for care planner."""
    
    def __init__(self):
        print("\n" + "="*70)
        print("CHRONIC CARE PLANNER - INTERACTIVE TESTER")
        print("="*70)
        print("\nInitializing system...")
        self.planner = DynamicChronicCarePlanner()
        print("✓ System ready!\n")
    
    def get_user_input(self) -> dict:
        """Get user data through interactive prompts."""
        print("\n" + "="*70)
        print("ENTER PATIENT DATA")
        print("="*70)
        print("(Press Enter to use default values shown in brackets)\n")
        
        user_data = {
            "user_profile": {},
            "health_data": {},
            "preferences": {}
        }
        
        # User Profile
        print("--- PERSONAL INFORMATION ---")
        
        age = input("Age [45]: ").strip()
        user_data["user_profile"]["age"] = int(age) if age else 45
        
        print("\nDiet Types: vegan, vegetarian, pescatarian, omnivore")
        diet = input("Diet Type [vegetarian]: ").strip().lower()
        user_data["user_profile"]["diet_type"] = diet if diet else "vegetarian"
        
        print("\nRegions: indian, western, asian, mediterranean, middle_eastern")
        region = input("Region [indian]: ").strip().lower()
        user_data["user_profile"]["region"] = region if region else "indian"
        
        print("\nActivity Levels: sedentary, low, moderate, high, very_high")
        activity = input("Activity Level [low]: ").strip().lower()
        user_data["user_profile"]["activity_level"] = activity if activity else "low"
        
        # Health Data
        print("\n--- HEALTH INFORMATION ---")
        
        fasting = input("Fasting Glucose (mg/dL) [160]: ").strip()
        user_data["health_data"]["avg_fasting_glucose"] = float(fasting) if fasting else 160
        
        post_meal = input("Post-Meal Glucose (mg/dL) [210]: ").strip()
        if post_meal:
            user_data["health_data"]["avg_post_meal_glucose"] = float(post_meal)
        else:
            user_data["health_data"]["avg_post_meal_glucose"] = 210
        
        # Preferences
        print("\n--- PREFERENCES (Optional) ---")
        
        allergies = input("Allergies (comma-separated): ").strip()
        if allergies:
            user_data["preferences"]["allergies"] = [a.strip() for a in allergies.split(",")]
        
        dislikes = input("Foods you dislike (comma-separated): ").strip()
        if dislikes:
            user_data["preferences"]["dislikes"] = [d.strip() for d in dislikes.split(",")]
        
        liked = input("Foods you like (comma-separated): ").strip()
        if liked:
            user_data["preferences"]["liked_foods"] = [l.strip() for l in liked.split(",")]
        
        return user_data
    
    def display_results(self, plan: dict):
        """Display care plan in readable format."""
        print("\n" + "="*70)
        print("CARE PLAN GENERATED")
        print("="*70)
        
        if "error" in plan:
            print(f"\n❌ ERROR: {plan['error']}")
            return
        
        # Safety Status
        safety = plan["safety"]
        print(f"\n🛡️  SAFETY STATUS: {safety['level'].upper()}")
        if safety["message"]:
            print(f"   {safety['message']}")
        if safety["flags"]:
            print(f"\n   Flags:")
            for flag in safety["flags"]:
                print(f"   • {flag}")
        
        # Food Plan
        food_plan = plan["plan"]["food_plan"]
        print(f"\n🍽️  MEAL PLAN:")
        print(f"\n   Breakfast:")
        print(f"   {food_plan['meal_plan']['breakfast']['description']}")
        
        print(f"\n   Morning Snack:")
        print(f"   {food_plan['meal_plan']['morning_snack']['description']}")
        
        print(f"\n   Lunch:")
        print(f"   {food_plan['meal_plan']['lunch']['description']}")
        
        print(f"\n   Afternoon Snack:")
        print(f"   {food_plan['meal_plan']['afternoon_snack']['description']}")
        
        print(f"\n   Dinner:")
        print(f"   {food_plan['meal_plan']['dinner']['description']}")
        
        # Shopping List
        shopping = food_plan["shopping_list"]
        print(f"\n🛒 SHOPPING LIST ({len(shopping)} items):")
        for i, item in enumerate(shopping, 1):
            print(f"   {i}. {item}")
        
        # Activity Plan
        activity = plan["plan"]["activity_plan"]["activity_plan"]
        print(f"\n🏃 ACTIVITY PLAN:")
        print(f"   Daily Aerobic: {activity['daily_aerobic']['activity']}")
        print(f"   Duration: {activity['daily_aerobic']['duration_minutes']} minutes")
        print(f"   Intensity: {activity['daily_aerobic']['intensity']}")
        print(f"   Frequency: {activity['weekly_schedule']['aerobic_days']} days/week")
        
        if "resistance_training" in activity:
            print(f"\n   Resistance Training:")
            print(f"   {activity['resistance_training']['exercises']}")
            print(f"   {activity['resistance_training']['frequency']}")
        
        # Rules Applied
        rules = food_plan["rules_applied"] + plan["plan"]["activity_plan"]["rules_applied"]
        print(f"\n📊 RULES APPLIED ({len(rules)}):")
        for rule in rules:
            print(f"   • {rule}")
        
        # Justification
        print(f"\n📝 JUSTIFICATION:")
        print(f"   {food_plan['justification']}")
        
        print(f"\n{plan['disclaimer']}")
    
    def save_plan(self, plan: dict, filename: str = None):
        """Save plan to JSON file."""
        if not filename:
            filename = f"care_plan_{plan['plan']['user_profile']['age']}yo.json"
        
        with open(filename, 'w') as f:
            json.dump(plan, f, indent=2)
        
        print(f"\n💾 Plan saved to: {filename}")
    
    def run_interactive(self):
        """Run interactive testing loop."""
        while True:
            try:
                # Get input
                user_data = self.get_user_input()
                
                # Generate plan
                print("\n⏳ Generating care plan...")
                plan = self.planner.create_care_plan(user_data)
                
                # Display results
                self.display_results(plan)
                
                # Ask to save
                save = input("\n💾 Save this plan? (y/n) [n]: ").strip().lower()
                if save == 'y':
                    filename = input("   Filename [auto]: ").strip()
                    self.save_plan(plan, filename if filename else None)
                
                # Continue or exit
                print("\n" + "="*70)
                again = input("\n🔄 Test another case? (y/n) [y]: ").strip().lower()
                if again == 'n':
                    print("\n✅ Thank you for testing!")
                    break
                
            except KeyboardInterrupt:
                print("\n\n✅ Testing interrupted. Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {str(e)}")
                print("Let's try again...\n")


def run_predefined_scenarios():
    """Run predefined test scenarios automatically."""
    print("\n" + "="*70)
    print("RUNNING PREDEFINED TEST SCENARIOS")
    print("="*70)
    
    planner = DynamicChronicCarePlanner()
    
    scenarios = [
        {
            "name": "🔴 HIGH RISK - Urgent Case",
            "data": {
                "user_profile": {
                    "age": 62,
                    "diet_type": "omnivore",
                    "region": "western",
                    "activity_level": "sedentary"
                },
                "health_data": {
                    "avg_fasting_glucose": 280,  # CRITICAL!
                    "avg_post_meal_glucose": 320
                },
                "preferences": {
                    "allergies": [],
                    "dislikes": [],
                    "liked_foods": []
                }
            }
        },
        {
            "name": "🟡 MODERATE RISK - Needs Attention",
            "data": {
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
                    "allergies": ["peanuts"],
                    "dislikes": ["eggplant"],
                    "liked_foods": ["quinoa", "chickpeas"]
                }
            }
        },
        {
            "name": "🟢 LOW RISK - Well Controlled",
            "data": {
                "user_profile": {
                    "age": 38,
                    "diet_type": "pescatarian",
                    "region": "mediterranean",
                    "activity_level": "moderate"
                },
                "health_data": {
                    "avg_fasting_glucose": 95,
                    "avg_post_meal_glucose": 125
                },
                "preferences": {
                    "allergies": [],
                    "dislikes": [],
                    "liked_foods": ["salmon", "olive oil", "berries"]
                }
            }
        },
        {
            "name": "🔵 SPECIAL CASE - Vegan + Allergies",
            "data": {
                "user_profile": {
                    "age": 52,
                    "diet_type": "vegan",
                    "region": "western",
                    "activity_level": "moderate"
                },
                "health_data": {
                    "avg_fasting_glucose": 145,
                    "avg_post_meal_glucose": 190
                },
                "preferences": {
                    "allergies": ["nuts", "soy"],
                    "dislikes": ["mushrooms"],
                    "liked_foods": ["quinoa", "berries", "oats"]
                }
            }
        },
        {
            "name": "🟣 ACTIVE PERSON - High Activity",
            "data": {
                "user_profile": {
                    "age": 35,
                    "diet_type": "omnivore",
                    "region": "western",
                    "activity_level": "high"
                },
                "health_data": {
                    "avg_fasting_glucose": 110,
                    "avg_post_meal_glucose": 140
                },
                "preferences": {
                    "allergies": [],
                    "dislikes": [],
                    "liked_foods": ["chicken", "salmon", "broccoli"]
                }
            }
        }
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n{'='*70}")
        print(f"SCENARIO {i}: {scenario['name']}")
        print(f"{'='*70}")
        
        print(f"\nInput Data:")
        print(f"  Age: {scenario['data']['user_profile']['age']}")
        print(f"  Diet: {scenario['data']['user_profile']['diet_type']}")
        print(f"  Region: {scenario['data']['user_profile']['region']}")
        print(f"  Activity: {scenario['data']['user_profile']['activity_level']}")
        print(f"  Fasting Glucose: {scenario['data']['health_data']['avg_fasting_glucose']} mg/dL")
        print(f"  Post-Meal Glucose: {scenario['data']['health_data']['avg_post_meal_glucose']} mg/dL")
        
        # Generate plan
        plan = planner.create_care_plan(scenario["data"])
        
        # Display summary
        print(f"\n🛡️  Safety: {plan['safety']['level'].upper()}")
        if plan['safety']['message']:
            print(f"   {plan['safety']['message']}")
        
        food_plan = plan['plan']['food_plan']
        print(f"\n🍽️  Sample Meals:")
        print(f"   Breakfast: {food_plan['meal_plan']['breakfast']['description']}")
        print(f"   Lunch: {food_plan['meal_plan']['lunch']['description']}")
        
        activity = plan['plan']['activity_plan']['activity_plan']
        print(f"\n🏃 Activity:")
        print(f"   {activity['daily_aerobic']['activity']} - {activity['daily_aerobic']['duration_minutes']} min/day")
        
        print(f"\n📊 Rules Applied: {len(food_plan['rules_applied']) + len(plan['plan']['activity_plan']['rules_applied'])}")
        
        input("\n⏸️  Press Enter to continue to next scenario...")
    
    print(f"\n{'='*70}")
    print("✅ All scenarios completed!")
    print(f"{'='*70}\n")


def main():
    """Main menu."""
    print("\n" + "="*70)
    print("CHRONIC CARE PLANNER - TESTING INTERFACE")
    print("="*70)
    print("\nChoose testing mode:\n")
    print("1. Interactive Mode - Enter data manually")
    print("2. Predefined Scenarios - Run 5 test cases automatically")
    print("3. Exit")
    
    choice = input("\nYour choice [1]: ").strip()
    
    if not choice or choice == "1":
        tester = InteractiveTester()
        tester.run_interactive()
    elif choice == "2":
        run_predefined_scenarios()
    elif choice == "3":
        print("\n✅ Goodbye!")
    else:
        print("\n❌ Invalid choice. Exiting.")


if __name__ == "__main__":
    main()