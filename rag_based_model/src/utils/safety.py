"""
Safety utilities for healthcare AI system.
Ensures all outputs include appropriate disclaimers and escalation logic.
"""

from typing import Dict, Any, List
from enum import Enum


class SafetyLevel(Enum):
    """Safety classification levels"""
    NORMAL = "normal"
    CAUTION = "caution"
    URGENT = "urgent"


class SafetyChecker:
    """
    Validates health data and determines safety levels.
    """
    
    # ADA-based thresholds
    GLUCOSE_THRESHOLDS = {
        "fasting_low": 70,
        "fasting_target_min": 80,
        "fasting_target_max": 130,
        "post_meal_target": 180,
        "red_flag": 250,
    }
    
    DISCLAIMER = (
        "⚠️ IMPORTANT DISCLAIMER: This is NOT medical advice. "
        "This system provides educational information based on public clinical guidelines. "
        "Always consult with your healthcare provider before making any changes to your "
        "diabetes management plan. In case of emergency, contact your doctor or emergency services immediately."
    )
    
    @classmethod
    def check_glucose_safety(cls, health_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Check glucose levels and determine safety status.
        
        Args:
            health_data: Dictionary containing glucose readings
            
        Returns:
            Dictionary with safety level, flags, and recommendations
        """
        safety_result = {
            "level": SafetyLevel.NORMAL.value,
            "flags": [],
            "escalation_required": False,
            "message": ""
        }
        
        fasting = health_data.get("avg_fasting_glucose")
        post_meal = health_data.get("avg_post_meal_glucose")
        
        # Check fasting glucose
        if fasting:
            if fasting >= cls.GLUCOSE_THRESHOLDS["red_flag"]:
                safety_result["level"] = SafetyLevel.URGENT.value
                safety_result["escalation_required"] = True
                safety_result["flags"].append("CRITICAL: Fasting glucose extremely high")
                safety_result["message"] = (
                    "🚨 URGENT: Your average fasting glucose is critically high (≥250 mg/dL). "
                    "Contact your healthcare provider IMMEDIATELY."
                )
                
            elif fasting < cls.GLUCOSE_THRESHOLDS["fasting_low"]:
                safety_result["level"] = SafetyLevel.URGENT.value
                safety_result["escalation_required"] = True
                safety_result["flags"].append("CRITICAL: Hypoglycemia risk")
                safety_result["message"] = (
                    "🚨 URGENT: Your average fasting glucose is too low (<70 mg/dL). "
                    "This indicates hypoglycemia risk. Contact your healthcare provider."
                )
                
            elif fasting > cls.GLUCOSE_THRESHOLDS["fasting_target_max"]:
                safety_result["level"] = SafetyLevel.CAUTION.value
                safety_result["flags"].append("Fasting glucose above target range")
                safety_result["message"] = (
                    "⚠️ Your fasting glucose is above the ADA target range (80-130 mg/dL). "
                    "Consider discussing this with your healthcare provider."
                )
        
        # Check post-meal glucose
        if post_meal:
            if post_meal >= cls.GLUCOSE_THRESHOLDS["red_flag"]:
                safety_result["level"] = SafetyLevel.URGENT.value
                safety_result["escalation_required"] = True
                safety_result["flags"].append("CRITICAL: Post-meal glucose extremely high")
                
            elif post_meal > cls.GLUCOSE_THRESHOLDS["post_meal_target"]:
                if safety_result["level"] != SafetyLevel.URGENT.value:
                    safety_result["level"] = SafetyLevel.CAUTION.value
                safety_result["flags"].append("Post-meal glucose above target")
        
        return safety_result
    
    @classmethod
    def add_disclaimer(cls, output: Dict[str, Any]) -> Dict[str, Any]:
        """
        Add mandatory disclaimer to all outputs.
        
        Args:
            output: Dictionary to add disclaimer to
            
        Returns:
            Updated dictionary with disclaimer
        """
        output["disclaimer"] = cls.DISCLAIMER
        output["generated_at"] = "This plan is generated based on clinical guidelines and your reported data."
        return output
    
    @classmethod
    def validate_input(cls, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate user input data for completeness and safety.
        
        Args:
            user_data: User profile and health data
            
        Returns:
            Validation result with errors if any
        """
        validation = {
            "valid": True,
            "errors": [],
            "warnings": []
        }
        
        # Check required fields
        required_profile = ["age"]
        required_health = ["avg_fasting_glucose"]
        
        profile = user_data.get("user_profile", {})
        health = user_data.get("health_data", {})
        
        for field in required_profile:
            if field not in profile:
                validation["valid"] = False
                validation["errors"].append(f"Missing required field: user_profile.{field}")
        
        for field in required_health:
            if field not in health:
                validation["valid"] = False
                validation["errors"].append(f"Missing required field: health_data.{field}")
        
        # Validate age
        age = profile.get("age")
        if age and (age < 18 or age > 100):
            validation["warnings"].append("Age outside typical range (18-100)")
        
        return validation
    
    @classmethod
    def check_medication_mention(cls, text: str) -> bool:
        """
        Check if text contains medication-related terms (should be avoided).
        
        Args:
            text: Text to check
            
        Returns:
            True if medication terms found
        """
        medication_keywords = [
            "metformin", "insulin", "medication", "drug", "prescription",
            "dose", "dosage", "medicine", "pill", "tablet"
        ]
        
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in medication_keywords)


def create_safe_response(
    plan: Dict[str, Any],
    safety_check: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Create a complete safe response with plan and safety information.
    
    Args:
        plan: Care plan dictionary
        safety_check: Safety check results
        
    Returns:
        Complete safe response
    """
    response = {
        "safety": safety_check,
        "plan": plan,
    }
    
    response = SafetyChecker.add_disclaimer(response)
    
    return response