"""
Flexible input handler that processes various input formats and structures.
Handles missing data, validates inputs, and normalizes to standard format.
"""

from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
import re


class FlexibleInputHandler:
    """
    Processes and normalizes various input formats for the care planner.
    """
    
    # Supported diet types
    DIET_TYPES = ["vegan", "vegetarian", "pescatarian", "omnivore", "keto", "paleo", "mediterranean"]
    
    # Supported regions
    REGIONS = ["indian", "western", "asian", "mediterranean", "middle_eastern", "latin_american", "african"]
    
    # Activity levels
    ACTIVITY_LEVELS = ["sedentary", "low", "moderate", "high", "very_high"]
    
    def __init__(self):
        self.errors = []
        self.warnings = []
    
    def process_input(self, raw_input: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process raw input and normalize to standard format.
        
        Args:
            raw_input: Various possible input formats
            
        Returns:
            Normalized input dictionary
        """
        self.errors = []
        self.warnings = []
        
        # Handle different input structures
        if "user_profile" in raw_input and "health_data" in raw_input:
            # Already structured
            normalized = raw_input.copy()
        else:
            # Flatten structure
            normalized = {
                "user_profile": {},
                "health_data": {},
                "preferences": {}
            }
            
            # Extract fields intelligently
            for key, value in raw_input.items():
                if key in ["age", "diet_type", "region", "activity_level", "gender", "height", "weight"]:
                    normalized["user_profile"][key] = value
                elif "glucose" in key.lower() or "sugar" in key.lower() or "hba1c" in key.lower():
                    normalized["health_data"][key] = value
                elif key in ["allergies", "dislikes", "liked_foods", "meal_timing_preference"]:
                    normalized["preferences"][key] = value
                else:
                    # Try to infer category
                    normalized["user_profile"][key] = value
        
        # Validate and normalize user profile
        normalized["user_profile"] = self._process_user_profile(normalized.get("user_profile", {}))
        
        # Validate and normalize health data
        normalized["health_data"] = self._process_health_data(normalized.get("health_data", {}))
        
        # Process preferences
        normalized["preferences"] = self._process_preferences(normalized.get("preferences", {}))
        
        return normalized
    
    def _process_user_profile(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and normalize user profile."""
        processed = {}
        
        # Age
        age = profile.get("age")
        if age:
            try:
                age_int = int(age)
                if 0 < age_int < 120:
                    processed["age"] = age_int
                else:
                    self.warnings.append(f"Age {age_int} outside normal range")
                    processed["age"] = max(18, min(100, age_int))
            except ValueError:
                self.errors.append(f"Invalid age: {age}")
        else:
            self.warnings.append("Age not provided, using default 45")
            processed["age"] = 45
        
        # Diet type
        diet = profile.get("diet_type", "").lower()
        if diet in self.DIET_TYPES:
            processed["diet_type"] = diet
        else:
            # Try to infer
            if any(word in diet for word in ["veg", "plant"]):
                if "egg" in diet or "dairy" in diet:
                    processed["diet_type"] = "vegetarian"
                else:
                    processed["diet_type"] = "vegan"
            elif "fish" in diet or "seafood" in diet:
                processed["diet_type"] = "pescatarian"
            else:
                processed["diet_type"] = "omnivore"
                if diet:
                    self.warnings.append(f"Unknown diet type '{diet}', using omnivore")
        
        # Region
        region = profile.get("region", "").lower()
        if any(r in region for r in self.REGIONS):
            # Extract matching region
            for r in self.REGIONS:
                if r in region:
                    processed["region"] = r
                    break
        else:
            processed["region"] = "western"
            if region:
                self.warnings.append(f"Unknown region '{region}', using western")
        
        # Activity level
        activity = profile.get("activity_level", "").lower()
        if activity in self.ACTIVITY_LEVELS:
            processed["activity_level"] = activity
        else:
            # Try to infer from description
            if any(word in activity for word in ["none", "never", "rarely", "desk"]):
                processed["activity_level"] = "sedentary"
            elif any(word in activity for word in ["little", "minimal", "1-2"]):
                processed["activity_level"] = "low"
            elif any(word in activity for word in ["regular", "3-4", "moderate"]):
                processed["activity_level"] = "moderate"
            elif any(word in activity for word in ["active", "5-6", "daily"]):
                processed["activity_level"] = "high"
            else:
                processed["activity_level"] = "low"
                if activity:
                    self.warnings.append(f"Unknown activity level '{activity}', using low")
        
        # Optional fields
        if "gender" in profile:
            processed["gender"] = profile["gender"]
        
        if "height" in profile:
            processed["height"] = profile["height"]
        
        if "weight" in profile:
            processed["weight"] = profile["weight"]
        
        return processed
    
    def _process_health_data(self, health_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and normalize health data."""
        processed = {}
        
        # Process fasting glucose
        fasting_keys = ["avg_fasting_glucose", "fasting_glucose", "fasting_sugar", "morning_glucose"]
        fasting = None
        for key in fasting_keys:
            if key in health_data:
                fasting = health_data[key]
                break
        
        if fasting:
            try:
                fasting_val = float(fasting)
                if 40 < fasting_val < 600:  # Reasonable range
                    processed["avg_fasting_glucose"] = fasting_val
                else:
                    self.errors.append(f"Fasting glucose {fasting_val} outside reasonable range")
            except (ValueError, TypeError):
                self.errors.append(f"Invalid fasting glucose value: {fasting}")
        else:
            self.errors.append("Fasting glucose data required")
        
        # Process post-meal glucose
        postmeal_keys = ["avg_post_meal_glucose", "post_meal_glucose", "postprandial_glucose", "after_meal_glucose"]
        postmeal = None
        for key in postmeal_keys:
            if key in health_data:
                postmeal = health_data[key]
                break
        
        if postmeal:
            try:
                postmeal_val = float(postmeal)
                if 40 < postmeal_val < 600:
                    processed["avg_post_meal_glucose"] = postmeal_val
            except (ValueError, TypeError):
                self.warnings.append(f"Invalid post-meal glucose value: {postmeal}")
        
        # Process HbA1c if provided
        if "hba1c" in health_data:
            try:
                hba1c_val = float(health_data["hba1c"])
                if 4 < hba1c_val < 15:
                    processed["hba1c"] = hba1c_val
            except (ValueError, TypeError):
                self.warnings.append(f"Invalid HbA1c value: {health_data['hba1c']}")
        
        # Process glucose readings array if provided
        if "glucose_readings" in health_data:
            readings = health_data["glucose_readings"]
            if isinstance(readings, list) and readings:
                processed["glucose_readings"] = readings
                # Calculate average if not provided
                if "avg_fasting_glucose" not in processed:
                    avg = sum(readings) / len(readings)
                    processed["avg_fasting_glucose"] = avg
                    self.warnings.append(f"Calculated average glucose from readings: {avg:.1f}")
        
        # Medical conditions
        if "conditions" in health_data:
            processed["conditions"] = health_data["conditions"]
        
        # Medications (for context, not for prescribing)
        if "medications" in health_data:
            processed["medications"] = health_data["medications"]
        
        return processed
    
    def _process_preferences(self, preferences: Dict[str, Any]) -> Dict[str, Any]:
        """Process user preferences."""
        processed = {}
        
        # Allergies
        allergies = preferences.get("allergies", [])
        if isinstance(allergies, str):
            # Parse comma-separated string
            allergies = [a.strip() for a in allergies.split(",")]
        processed["allergies"] = [a.lower() for a in allergies if a]
        
        # Dislikes
        dislikes = preferences.get("dislikes", [])
        if isinstance(dislikes, str):
            dislikes = [d.strip() for d in dislikes.split(",")]
        processed["dislikes"] = [d.lower() for d in dislikes if d]
        
        # Liked foods
        liked = preferences.get("liked_foods", [])
        if isinstance(liked, str):
            liked = [l.strip() for l in liked.split(",")]
        processed["liked_foods"] = [l.lower() for l in liked if l]
        
        # Meal timing preferences
        if "meal_timing_preference" in preferences:
            processed["meal_timing_preference"] = preferences["meal_timing_preference"]
        
        # Budget constraints
        if "budget" in preferences:
            processed["budget"] = preferences["budget"]
        
        # Cooking skill level
        if "cooking_skill" in preferences:
            processed["cooking_skill"] = preferences["cooking_skill"]
        
        return processed
    
    def get_validation_report(self) -> Dict[str, Any]:
        """Get validation errors and warnings."""
        return {
            "valid": len(self.errors) == 0,
            "errors": self.errors,
            "warnings": self.warnings
        }
    def parse_natural_language_input(self, text: str) -> Dict[str, Any]:
        """Parse natural language input (basic implementation)."""
        parsed = {
            "user_profile": {},
            "health_data": {},
            "preferences": {}
        }
        
        text_lower = text.lower()
        
        # Extract age - more flexible patterns
        age_match = re.search(r"(\d{2,3})\s*(?:years?\s*old|yrs?\s*old|yo|year)", text_lower)
        if age_match:
            parsed["user_profile"]["age"] = int(age_match.group(1))
        
        # Extract diet type
        for diet in self.DIET_TYPES:
            if diet in text_lower:
                parsed["user_profile"]["diet_type"] = diet
                break
        
        # Extract region - more flexible
        for region in self.REGIONS:
            if region in text_lower or region.replace("_", " ") in text_lower:
                parsed["user_profile"]["region"] = region
                break
        
        # Extract glucose - IMPROVED PATTERN
        # Look for patterns like "glucose is 155", "glucose 155", "fasting glucose: 155"
        glucose_patterns = [
            r'(?:fasting\s+)?glucose\s+is\s+(?:usually\s+)?(?:around\s+)?(\d{2,3})',
            r'(?:fasting\s+)?glucose[:\s]+(\d{2,3})',
            r'(?:fasting\s+)?sugar\s+is\s+(?:usually\s+)?(?:around\s+)?(\d{2,3})',
            r'my\s+(?:fasting\s+)?(?:glucose|sugar)\s+(?:is\s+)?(\d{2,3})',
            r'glucose\s+of\s+(\d{2,3})',
        ]
        
        for pattern in glucose_patterns:
            glucose_match = re.search(pattern, text_lower)
            if glucose_match:
                parsed["health_data"]["avg_fasting_glucose"] = int(glucose_match.group(1))
                break
        
        return self.process_input(parsed)
    
    


if __name__ == "__main__":
    handler = FlexibleInputHandler()
    
    # Test case 1: Flat structure
    print("Test 1: Flat structure")
    input1 = {
        "age": "45",
        "diet_type": "plant-based",
        "region": "South India",
        "fasting_sugar": 160,
        "post_meal_glucose": 210,
        "allergies": "peanuts, shellfish",
        "liked_foods": "quinoa, chickpeas"
    }
    result1 = handler.process_input(input1)
    print(f"Normalized: {result1}")
    print(f"Validation: {handler.get_validation_report()}\n")
    
    # Test case 2: Natural language
    print("Test 2: Natural language")
    nl_input = "I'm 52 years old, vegan, from western region, fasting glucose is 145"
    result2 = handler.parse_natural_language_input(nl_input)
    print(f"Parsed: {result2}")
    print(f"Validation: {handler.get_validation_report()}\n")
    
    # Test case 3: Missing data
    print("Test 3: Missing critical data")
    input3 = {"age": 30, "region": "india"}
    result3 = handler.process_input(input3)
    print(f"Normalized: {result3}")
    print(f"Validation: {handler.get_validation_report()}")