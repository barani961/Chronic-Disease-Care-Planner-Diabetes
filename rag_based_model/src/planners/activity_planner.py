"""
Activity planner using rule-based logic and ADA physical activity guidelines.
Generates safe, progressive exercise plans for diabetes management.
"""

from typing import Dict, Any, List
import json


class ActivityPlanner:
    """
    Rule-based activity planning for diabetes management.
    Follows ADA physical activity guidelines with safety considerations.
    """
    
    # Activity intensity levels
    ACTIVITY_LEVELS = {
        "sedentary": {
            "description": "Little to no regular exercise",
            "start_duration": 10,  # minutes per session
            "target_duration": 30
        },
        "low": {
            "description": "Light activity 1-2 days/week",
            "start_duration": 20,
            "target_duration": 30
        },
        "moderate": {
            "description": "Regular activity 3-4 days/week",
            "start_duration": 30,
            "target_duration": 40
        },
        "high": {
            "description": "Active lifestyle 5+ days/week",
            "start_duration": 40,
            "target_duration": 50
        }
    }
    
    # Exercise types by fitness level
    EXERCISE_OPTIONS = {
        "aerobic": {
            "beginner": ["brisk walking", "cycling on flat terrain", "water aerobics"],
            "intermediate": ["jogging", "swimming", "cycling", "dance"],
            "advanced": ["running", "cycling hills", "sports (tennis, basketball)"]
        },
        "resistance": {
            "beginner": ["bodyweight exercises (wall push-ups, chair squats)", "resistance bands", "light dumbbells (1-2 kg)"],
            "intermediate": ["moderate weight training", "resistance band exercises", "bodyweight circuits"],
            "advanced": ["weight training", "resistance exercises with heavier weights"]
        },
        "flexibility": {
            "all": ["stretching", "yoga", "tai chi"]
        }
    }
    
    def __init__(self):
        """Initialize activity planner."""
        self.rules_applied = []
    
    def plan_activities(
        self,
        user_profile: Dict[str, Any],
        health_data: Dict[str, Any],
        guidelines: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate personalized activity plan based on rules and guidelines.
        
        Args:
            user_profile: User demographics and current activity level
            health_data: Current health metrics
            guidelines: Retrieved clinical guidelines
            
        Returns:
            Structured activity plan with justification
        """
        self.rules_applied = []
        
        # Determine current fitness level
        activity_level = user_profile.get("activity_level", "low").lower()
        age = user_profile.get("age", 45)
        
        # Check glucose levels for safety
        avg_glucose = health_data.get("avg_fasting_glucose", 0)
        
        # Apply planning rules
        plan_params = self._apply_planning_rules(activity_level, age, avg_glucose, guidelines)
        
        # Generate activity recommendations
        activity_plan = self._generate_activity_recommendations(plan_params, activity_level, age)
        
        # Create progression plan
        progression = self._create_progression_plan(activity_level, plan_params)
        
        # Create justification
        justification = self._create_justification(activity_level, avg_glucose, guidelines)
        
        # Safety reminders
        safety_reminders = self._get_safety_reminders(avg_glucose)
        
        # Compile output
        output = {
            "activity_plan": activity_plan,
            "progression": progression,
            "rules_applied": self.rules_applied,
            "justification": justification,
            "safety_reminders": safety_reminders
        }
        
        return output
    
    def _apply_planning_rules(
        self,
        activity_level: str,
        age: int,
        avg_glucose: float,
        guidelines: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Apply rule-based logic for activity planning."""
        params = {
            "start_slow": False,
            "intensity": "moderate",
            "focus_aerobic": True,
            "include_resistance": True,
            "frequency_per_week": 5
        }
        
        # Rule 1: Sedentary or low activity → Start conservatively
        if activity_level in ["sedentary", "low"]:
            params["start_slow"] = True
            params["intensity"] = "low"
            params["frequency_per_week"] = 3
            self.rules_applied.append("Low activity level → Start with conservative plan and progress gradually")
        
        # Rule 2: High glucose → Emphasize activity for glucose control
        if avg_glucose > 150:
            params["focus_aerobic"] = True
            self.rules_applied.append("Elevated glucose → Emphasize aerobic activity for glucose control")
        
        # Rule 3: Older adults → Include balance and flexibility
        if age > 65:
            params["include_balance"] = True
            self.rules_applied.append("Age >65 → Include balance and flexibility exercises")
        
        # Rule 4: Follow ADA guidelines for frequency
        if activity_level not in ["sedentary", "low"]:
            params["frequency_per_week"] = 5
            self.rules_applied.append("ADA guideline → Target 150 minutes/week spread over 5+ days")
        
        return params
    
    def _generate_activity_recommendations(
        self,
        params: Dict[str, Any],
        activity_level: str,
        age: int
    ) -> Dict[str, Any]:
        """Generate specific activity recommendations."""
        # Determine fitness level for exercise selection
        if activity_level in ["sedentary", "low"]:
            fitness_level = "beginner"
        elif activity_level == "moderate":
            fitness_level = "intermediate"
        else:
            fitness_level = "advanced"
        
        # Get appropriate duration
        level_config = self.ACTIVITY_LEVELS.get(activity_level, self.ACTIVITY_LEVELS["low"])
        duration = level_config["start_duration"] if params["start_slow"] else level_config["target_duration"]
        
        plan = {}
        
        # Aerobic activity
        aerobic_options = self.EXERCISE_OPTIONS["aerobic"][fitness_level]
        plan["daily_aerobic"] = {
            "activity": aerobic_options[0],  # Primary recommendation
            "duration_minutes": duration,
            "intensity": params["intensity"],
            "alternatives": aerobic_options[1:] if len(aerobic_options) > 1 else []
        }
        
        # Weekly frequency
        plan["weekly_schedule"] = {
            "aerobic_days": params["frequency_per_week"],
            "rest_days": 7 - params["frequency_per_week"],
            "note": "No more than 2 consecutive days without activity"
        }
        
        # Resistance training
        if params.get("include_resistance", True):
            resistance_options = self.EXERCISE_OPTIONS["resistance"][fitness_level]
            plan["resistance_training"] = {
                "exercises": resistance_options[0],
                "frequency": "2-3 days per week on non-consecutive days",
                "focus": "All major muscle groups"
            }
        
        # Flexibility (always include)
        plan["flexibility"] = {
            "exercises": "Stretching or yoga",
            "frequency": "2-3 times per week",
            "duration": "10-15 minutes"
        }
        
        # Balance for older adults
        if age > 65:
            plan["balance"] = {
                "exercises": "Standing on one foot, heel-to-toe walk, tai chi",
                "frequency": "2-3 times per week"
            }
        
        return plan
    
    def _create_progression_plan(
        self,
        activity_level: str,
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create progressive increase plan."""
        if params["start_slow"]:
            progression = {
                "week_1_2": "Start with recommended duration and frequency",
                "week_3_4": "Increase duration by 5 minutes per session",
                "week_5_6": "Increase to 4 days per week if comfortable",
                "week_7_plus": "Progress toward 150 minutes per week (30 min × 5 days)",
                "principle": "Increase by no more than 10% per week"
            }
        else:
            progression = {
                "current": "Maintain current activity level",
                "next_step": "Gradually increase intensity or add variety",
                "principle": "Progress based on comfort and glucose response"
            }
        
        return progression
    
    def _create_justification(
        self,
        activity_level: str,
        avg_glucose: float,
        guidelines: Dict[str, Any]
    ) -> str:
        """Create human-readable justification."""
        justifications = []
        
        # Activity level justification
        if activity_level in ["sedentary", "low"]:
            justifications.append(
                "Starting with a conservative plan is important for building sustainable exercise habits and reducing injury risk"
            )
        
        # Glucose justification
        if avg_glucose > 150:
            justifications.append(
                f"Regular physical activity can help improve glucose control (current average: {avg_glucose} mg/dL)"
            )
        
        # ADA guideline reference
        ada_target = guidelines.get("activity_guidelines", {}).get("aerobic", "150 minutes per week")
        justifications.append(
            f"This plan follows ADA recommendations of {ada_target} of moderate-intensity aerobic activity"
        )
        
        return ". ".join(justifications) + "."
    
    def _get_safety_reminders(self, avg_glucose: float) -> List[str]:
        """Generate safety reminders based on glucose levels."""
        reminders = [
            "Check blood glucose before and after exercise",
            "Carry a fast-acting carbohydrate source (glucose tablets, juice)",
            "Stay well hydrated before, during, and after exercise",
            "Wear proper footwear to prevent foot injuries",
            "Stop exercising if you feel dizzy, short of breath, or experience chest pain"
        ]
        
        if avg_glucose > 250:
            reminders.insert(0, 
                "⚠️ CAUTION: Avoid vigorous exercise if glucose is >250 mg/dL. Check with healthcare provider."
            )
        
        return reminders


def create_activity_plan(
    user_profile: Dict[str, Any],
    health_data: Dict[str, Any],
    guidelines: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Convenience function to create activity plan.
    
    Args:
        user_profile: User demographics and activity level
        health_data: Current health metrics
        guidelines: Clinical guidelines from RAG
        
    Returns:
        Complete activity plan
    """
    planner = ActivityPlanner()
    return planner.plan_activities(user_profile, health_data, guidelines)


if __name__ == "__main__":
    # Example usage
    user_profile = {
        "age": 45,
        "activity_level": "low"
    }
    
    health_data = {
        "avg_fasting_glucose": 180
    }
    
    # Mock guidelines (would come from RAG in real usage)
    guidelines = {
        "activity_guidelines": {
            "aerobic": "150 minutes per week moderate-intensity",
            "strength": "2-3 days per week"
        }
    }
    
    plan = create_activity_plan(user_profile, health_data, guidelines)
    
    print("Activity Plan Generated:")
    print("="*60)
    print(json.dumps(plan, indent=2))