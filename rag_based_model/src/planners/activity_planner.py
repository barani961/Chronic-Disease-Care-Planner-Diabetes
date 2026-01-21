"""
FIXED Activity planner with proper glucose-risk-based duration logic.
"""

from typing import Dict, Any, List
import json


class ActivityPlanner:
    """
    Rule-based activity planning for diabetes management.
    Prioritizes GLUCOSE RISK over fitness level for safety.
    """
    
    ACTIVITY_LEVELS = {
        "sedentary": {"description": "Little to no regular exercise"},
        "low": {"description": "Light activity 1-2 days/week"},
        "moderate": {"description": "Regular activity 3-4 days/week"},
        "high": {"description": "Active lifestyle 5+ days/week"},
        "very_high": {"description": "Athlete level 6-7 days/week"}
    }
    
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
        }
    }
    
    def __init__(self):
        self.rules_applied = []
    
    def plan_activities(
        self,
        user_profile: Dict[str, Any],
        health_data: Dict[str, Any],
        guidelines: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate activity plan prioritizing SAFETY (glucose risk) first.
        """
        self.rules_applied = []
        
        activity_level = user_profile.get("activity_level", "low").lower()
        age = user_profile.get("age", 45)
        avg_glucose = health_data.get("avg_fasting_glucose", 0)
        
        # CRITICAL: Determine plan based on GLUCOSE RISK first, then fitness
        plan_params = self._determine_safe_plan(avg_glucose, activity_level, age)
        
        # Generate activity recommendations
        activity_plan = self._generate_activity_recommendations(plan_params, activity_level, age)
        
        # Create progression plan
        progression = self._create_progression_plan(activity_level, plan_params)
        
        # Create justification
        justification = self._create_justification(activity_level, avg_glucose, guidelines)
        
        # Safety reminders
        safety_reminders = self._get_safety_reminders(avg_glucose)
        
        return {
            "activity_plan": activity_plan,
            "progression": progression,
            "rules_applied": self.rules_applied,
            "justification": justification,
            "safety_reminders": safety_reminders
        }
    
    def _determine_safe_plan(
        self,
        avg_glucose: float,
        activity_level: str,
        age: int
    ) -> Dict[str, Any]:
        """
        FIXED: Prioritize glucose risk over activity level for safety.
        """
        params = {
            "start_slow": False,
            "intensity": "moderate",
            "focus_aerobic": True,
            "include_resistance": True,
            "frequency_per_week": 5,
            "duration": 30,
            "fitness_level": "intermediate"
        }
        
        # PRIORITY 1: GLUCOSE RISK (overrides everything)
        if avg_glucose >= 250:
            # CRITICAL glucose - very gentle start
            params["start_slow"] = True
            params["intensity"] = "very_light"
            params["duration"] = 10
            params["frequency_per_week"] = 3
            params["fitness_level"] = "beginner"
            self.rules_applied.append("CRITICAL glucose (≥250) → Start with very gentle activity (10 min)")
            
        elif avg_glucose >= 180:
            # High glucose - gentle start
            params["start_slow"] = True
            params["intensity"] = "light"
            params["duration"] = 15
            params["frequency_per_week"] = 4
            params["fitness_level"] = "beginner"
            self.rules_applied.append("High glucose (≥180) → Gentle activity recommended (15 min)")
            
        elif avg_glucose >= 150:
            # Elevated glucose - moderate caution
            params["intensity"] = "light_to_moderate"
            params["duration"] = 20
            params["frequency_per_week"] = 4
            params["fitness_level"] = "beginner"
            self.rules_applied.append("Elevated glucose (≥150) → Moderate activity (20 min)")
        
        # PRIORITY 2: FITNESS LEVEL (only if glucose is controlled)
        elif avg_glucose < 150:
            # Glucose controlled - can use fitness level
            if activity_level == "sedentary":
                params["duration"] = 15
                params["frequency_per_week"] = 3
                params["fitness_level"] = "beginner"
                self.rules_applied.append("Sedentary lifestyle → Start with 15 min, 3 days/week")
                
            elif activity_level == "low":
                params["duration"] = 20
                params["frequency_per_week"] = 4
                params["fitness_level"] = "beginner"
                self.rules_applied.append("Low activity level → Progressive plan starting 20 min")
                
            elif activity_level == "moderate":
                params["duration"] = 30
                params["frequency_per_week"] = 5
                params["fitness_level"] = "intermediate"
                self.rules_applied.append("Moderate activity → Maintain 30 min, 5 days/week")
                
            elif activity_level in ["high", "very_high"]:
                params["duration"] = 40
                params["frequency_per_week"] = 5
                params["fitness_level"] = "intermediate"
                self.rules_applied.append("High activity level → 40 min sessions recommended")
        
        # PRIORITY 3: AGE CONSIDERATIONS
        if age > 65:
            params["include_balance"] = True
            params["duration"] = min(params["duration"], 30)  # Cap at 30 min
            self.rules_applied.append("Age >65 → Include balance exercises, cap duration at 30 min")
        
        # PRIORITY 4: ADA GUIDELINES
        if avg_glucose < 150 and activity_level not in ["sedentary", "low"]:
            self.rules_applied.append("ADA guideline → Target 150 minutes/week moderate activity")
        
        return params
    
    def _generate_activity_recommendations(
        self,
        params: Dict[str, Any],
        activity_level: str,
        age: int
    ) -> Dict[str, Any]:
        """Generate specific activity recommendations."""
        fitness_level = params["fitness_level"]
        duration = params["duration"]
        
        plan = {}
        
        # Aerobic activity
        aerobic_options = self.EXERCISE_OPTIONS["aerobic"][fitness_level]
        plan["daily_aerobic"] = {
            "activity": aerobic_options[0],
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
                "week_1_2": f"Start with {params['duration']} minutes, {params['frequency_per_week']} days/week",
                "week_3_4": "Increase duration by 5 minutes per session",
                "week_5_6": "Add 1 more day per week if comfortable",
                "week_7_plus": "Progress toward 150 minutes per week (30 min × 5 days)",
                "principle": "Increase by no more than 10% per week"
            }
        else:
            progression = {
                "current": f"Maintain {params['duration']} minutes, {params['frequency_per_week']} days/week",
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
        
        # Glucose justification (priority)
        if avg_glucose >= 250:
            justifications.append(
                f"Your glucose level ({avg_glucose} mg/dL) is critically high. Starting with very gentle activity for safety"
            )
        elif avg_glucose >= 180:
            justifications.append(
                f"Your glucose level ({avg_glucose} mg/dL) is elevated. Gentle aerobic activity can help improve control"
            )
        elif avg_glucose >= 150:
            justifications.append(
                f"Regular physical activity can help improve glucose control (current: {avg_glucose} mg/dL)"
            )
        else:
            justifications.append(
                f"Your glucose is well-controlled. Activity helps maintain this control"
            )
        
        # Activity level justification
        if activity_level in ["sedentary", "low"]:
            justifications.append(
                "Starting conservatively is important for building sustainable exercise habits"
            )
        
        # ADA guideline reference
        justifications.append(
            "This plan follows ADA recommendations for diabetes management"
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
                "🚨 CRITICAL: Avoid vigorous exercise if glucose is >250 mg/dL. Consult healthcare provider before starting."
            )
        elif avg_glucose > 180:
            reminders.insert(0,
                "⚠️ CAUTION: Monitor glucose closely during and after exercise. Stay in light-moderate intensity zone."
            )
        
        return reminders


def create_activity_plan(
    user_profile: Dict[str, Any],
    health_data: Dict[str, Any],
    guidelines: Dict[str, Any]
) -> Dict[str, Any]:
    """Convenience function to create activity plan."""
    planner = ActivityPlanner()
    return planner.plan_activities(user_profile, health_data, guidelines)