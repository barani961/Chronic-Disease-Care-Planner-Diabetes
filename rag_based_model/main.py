"""
Main entry point for Chronic Disease Care Planner.
Integrates all modules: RAG, Food Planner, Activity Planner, Safety.
"""

import json
from pathlib import Path
from typing import Dict, Any

# Import all modules
from src.rag.retrieve_guidelines import GuidelineRetriever
from src.planners.food_planner import create_food_plan
from src.planners.activity_planner import create_activity_plan
from src.utils.safety import SafetyChecker, create_safe_response


class ChronicCarePlanner:
    """
    Main care planner orchestrator.
    Coordinates RAG, planning, and safety checks.
    """
    
    def __init__(self, index_dir: str = "data/faiss_index"):
        """
        Initialize care planner with RAG system.
        
        Args:
            index_dir: Path to FAISS index directory
        """
        print("Initializing Chronic Care Planner...")
        self.retriever = GuidelineRetriever(index_dir=index_dir)
        print("✓ RAG system loaded")
    
    def create_care_plan(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create complete care plan for user.
        
        Args:
            user_data: Dictionary containing user_profile and health_data
            
        Returns:
            Complete care plan with safety checks
        """
        print("\n" + "="*60)
        print("CREATING CARE PLAN")
        print("="*60)
        
        # Step 1: Validate input
        print("\n1. Validating input data...")
        validation = SafetyChecker.validate_input(user_data)
        if not validation["valid"]:
            return {
                "error": "Invalid input data",
                "details": validation["errors"]
            }
        print("   ✓ Input validated")
        
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
        
        # Step 4: Generate food plan
        print("\n4. Generating food plan...")
        food_plan = create_food_plan(user_profile, health_data, guidelines)
        print(f"   ✓ Food plan created with {len(food_plan['rules_applied'])} rules applied")
        
        # Step 5: Generate activity plan
        print("\n5. Generating activity plan...")
        activity_plan = create_activity_plan(user_profile, health_data, guidelines)
        print(f"   ✓ Activity plan created with {len(activity_plan['rules_applied'])} rules applied")
        
        # Step 6: Compile complete plan
        print("\n6. Compiling complete care plan...")
        complete_plan = {
            "user_profile": user_profile,
            "health_data": health_data,
            "guidelines_used": {
                "glycemic_targets": guidelines["glycemic_targets"],
                "citations": guidelines["citations"]
            },
            "food_plan": food_plan,
            "activity_plan": activity_plan
        }
        
        # Step 7: Add safety wrapper
        safe_response = create_safe_response(complete_plan, safety_check)
        
        print("   ✓ Care plan complete")
        print("\n" + "="*60)
        print("CARE PLAN GENERATION COMPLETE")
        print("="*60 + "\n")
        
        return safe_response
    
    def update_weekly_plan(
        self,
        user_data: Dict[str, Any],
        weekly_progress: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Update care plan based on weekly progress.
        
        Args:
            user_data: Current user data
            weekly_progress: Week's adherence and glucose data
            
        Returns:
            Updated care plan
        """
        print("\n" + "="*60)
        print("UPDATING WEEKLY PLAN")
        print("="*60)
        
        # Analyze trends
        print("\n1. Analyzing weekly trends...")
        avg_fasting = sum(weekly_progress.get("fasting_readings", [0])) / max(len(weekly_progress.get("fasting_readings", [1])), 1)
        
        # Update health data with weekly average
        user_data["health_data"]["avg_fasting_glucose"] = avg_fasting
        
        print(f"   ✓ Average fasting glucose this week: {avg_fasting:.1f} mg/dL")
        
        # Generate new plan with updated data
        updated_plan = self.create_care_plan(user_data)
        
        # Add progress commentary
        updated_plan["weekly_summary"] = {
            "average_fasting_glucose": avg_fasting,
            "trend": self._determine_trend(weekly_progress),
            "adherence": {
                "meals": weekly_progress.get("meal_adherence", 0),
                "activity": weekly_progress.get("activity_adherence", 0)
            }
        }
        
        return updated_plan
    
    def _determine_trend(self, weekly_progress: Dict[str, Any]) -> str:
        """Determine if glucose is improving, stable, or worsening."""
        readings = weekly_progress.get("fasting_readings", [])
        if len(readings) < 2:
            return "insufficient_data"
        
        first_half = sum(readings[:len(readings)//2]) / (len(readings)//2)
        second_half = sum(readings[len(readings)//2:]) / (len(readings) - len(readings)//2)
        
        if second_half < first_half - 10:
            return "improving"
        elif second_half > first_half + 10:
            return "worsening"
        else:
            return "stable"


def load_example_input() -> Dict[str, Any]:
    """Load example input from JSON file."""
    example_path = Path("examples/sample_input.json")
    if example_path.exists():
        with open(example_path, 'r') as f:
            return json.load(f)
    
    # Return default if file doesn't exist
    return {
        "user_profile": {
            "age": 45,
            "diet_type": "vegetarian",
            "region": "India",
            "activity_level": "low"
        },
        "health_data": {
            "avg_fasting_glucose": 160,
            "avg_post_meal_glucose": 210
        }
    }


def save_output(output: Dict[str, Any], filename: str = "examples/sample_output.json"):
    """Save output to JSON file."""
    output_path = Path(filename)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"\n✓ Output saved to {filename}")


def main():
    """Main execution function."""
    print("\n" + "="*60)
    print("CHRONIC DISEASE CARE PLANNER - DIABETES FOCUSED")
    print("="*60)
    
    # Initialize planner
    planner = ChronicCarePlanner(index_dir="data/faiss_index")
    
    # Load example input
    print("\nLoading example input...")
    user_data = load_example_input()
    
    print("\nUser Profile:")
    print(f"  Age: {user_data['user_profile']['age']}")
    print(f"  Diet: {user_data['user_profile']['diet_type']}")
    print(f"  Region: {user_data['user_profile']['region']}")
    print(f"  Activity Level: {user_data['user_profile']['activity_level']}")
    
    print("\nHealth Data:")
    print(f"  Avg Fasting Glucose: {user_data['health_data']['avg_fasting_glucose']} mg/dL")
    print(f"  Avg Post-Meal Glucose: {user_data['health_data']['avg_post_meal_glucose']} mg/dL")
    
    # Create care plan
    care_plan = planner.create_care_plan(user_data)
    
    # Display summary
    print("\n" + "="*60)
    print("CARE PLAN SUMMARY")
    print("="*60)
    
    print(f"\nSafety Status: {care_plan['safety']['level'].upper()}")
    if care_plan['safety']['message']:
        print(f"Message: {care_plan['safety']['message']}")
    
    print("\n--- FOOD PLAN ---")
    meal_plan = care_plan['plan']['food_plan']['meal_plan']
    print(f"Breakfast: {meal_plan['breakfast']}")
    print(f"Lunch: {meal_plan['lunch']}")
    print(f"Dinner: {meal_plan['dinner']}")
    print(f"Snacks: {meal_plan['snacks']}")
    
    print("\n--- ACTIVITY PLAN ---")
    activity = care_plan['plan']['activity_plan']['activity_plan']
    print(f"Daily Aerobic: {activity['daily_aerobic']['activity']} for {activity['daily_aerobic']['duration_minutes']} minutes")
    print(f"Weekly Schedule: {activity['weekly_schedule']['aerobic_days']} days per week")
    print(f"Resistance Training: {activity['resistance_training']['frequency']}")
    
    print("\n--- GUIDELINES APPLIED ---")
    print(f"Citations: {', '.join(care_plan['plan']['guidelines_used']['citations'])}")
    
    print(f"\n{care_plan['disclaimer']}")
    
    # Save output
    save_output(care_plan)
    
    print("\n" + "="*60)
    print("EXECUTION COMPLETE")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()