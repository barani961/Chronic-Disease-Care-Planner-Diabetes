"""
LLM prompt templates for care planning system.
Designed to be conservative, guideline-based, and safe.
"""

from typing import Dict, Any
import json


class PlannerPrompts:
    """
    Manages prompt templates for LLM-assisted care planning.
    All prompts emphasize safety, guidelines, and disclaimers.
    """
    
    # System prompt for LLM
    SYSTEM_PROMPT = """You are a healthcare AI assistant specializing in diabetes care planning. Your role is to:

1. FOLLOW CLINICAL GUIDELINES STRICTLY
   - Base all recommendations on ADA (American Diabetes Association) standards
   - Never contradict evidence-based guidelines
   - Always cite guideline sources

2. PRIORITIZE SAFETY
   - Never provide medication advice or dosage recommendations
   - Never diagnose conditions
   - Escalate concerning values to healthcare providers
   - Include appropriate disclaimers in all responses

3. BE CONSERVATIVE AND EXPLAINABLE
   - Explain reasoning behind each recommendation
   - Use deterministic rules when possible
   - Be transparent about limitations
   - Avoid overconfident claims

4. MAINTAIN APPROPRIATE BOUNDARIES
   - This is a care planning tool, not medical advice
   - Encourage users to consult healthcare providers
   - Do not create false sense of security

MANDATORY DISCLAIMER (include in all responses):
"⚠️ This is not medical advice. Always consult your healthcare provider before making changes to your diabetes management plan."

Your responses should be:
- Evidence-based
- Conservative
- Explainable
- Actionable
- Safe"""

    @staticmethod
    def create_meal_explanation_prompt(
        user_profile: Dict[str, Any],
        health_data: Dict[str, Any],
        meal_plan: Dict[str, Any],
        guidelines: Dict[str, Any]
    ) -> str:
        """
        Create prompt for LLM to explain meal plan in natural language.
        
        Args:
            user_profile: User demographics
            health_data: Current health metrics
            meal_plan: Generated meal plan
            guidelines: Clinical guidelines used
            
        Returns:
            Formatted prompt string
        """
        prompt = f"""Based on the following information, provide a brief, supportive explanation of this meal plan:

USER PROFILE:
- Age: {user_profile.get('age')}
- Diet Type: {user_profile.get('diet_type', 'No restrictions')}
- Region: {user_profile.get('region', 'Not specified')}

CURRENT HEALTH DATA:
- Average Fasting Glucose: {health_data.get('avg_fasting_glucose')} mg/dL
- Average Post-Meal Glucose: {health_data.get('avg_post_meal_glucose', 'Not provided')} mg/dL

MEAL PLAN GENERATED:
{json.dumps(meal_plan, indent=2)}

GUIDELINES APPLIED:
- Target fasting glucose: {guidelines.get('safety_thresholds', {}).get('fasting_glucose', {}).get('target_min', 80)}-{guidelines.get('safety_thresholds', {}).get('fasting_glucose', {}).get('target_max', 130)} mg/dL
- Target post-meal glucose: <{guidelines.get('safety_thresholds', {}).get('post_meal_glucose', {}).get('target', 180)} mg/dL
- Fiber recommendation: {guidelines.get('diet_guidelines', {}).get('fiber', '25-30g/day')}

INSTRUCTIONS:
1. Explain WHY this meal plan was created (based on glucose levels and guidelines)
2. Highlight 2-3 key benefits of the recommended foods
3. Be encouraging but realistic
4. Keep explanation under 150 words
5. Include the mandatory disclaimer
6. Do NOT suggest medication changes
7. Do NOT make medical diagnoses

Focus on: empowerment, education, and guideline adherence."""

        return prompt

    @staticmethod
    def create_activity_explanation_prompt(
        user_profile: Dict[str, Any],
        health_data: Dict[str, Any],
        activity_plan: Dict[str, Any],
        guidelines: Dict[str, Any]
    ) -> str:
        """
        Create prompt for LLM to explain activity plan in natural language.
        
        Args:
            user_profile: User demographics
            health_data: Current health metrics
            activity_plan: Generated activity plan
            guidelines: Clinical guidelines used
            
        Returns:
            Formatted prompt string
        """
        prompt = f"""Based on the following information, provide a brief, motivating explanation of this activity plan:

USER PROFILE:
- Age: {user_profile.get('age')}
- Current Activity Level: {user_profile.get('activity_level', 'Not specified')}

CURRENT HEALTH DATA:
- Average Fasting Glucose: {health_data.get('avg_fasting_glucose')} mg/dL

ACTIVITY PLAN GENERATED:
{json.dumps(activity_plan, indent=2)}

ADA GUIDELINES:
- Recommended: {guidelines.get('activity_guidelines', {}).get('aerobic', '150 minutes/week moderate-intensity')}
- Resistance training: {guidelines.get('activity_guidelines', {}).get('strength', '2-3 days/week')}

INSTRUCTIONS:
1. Explain WHY this activity plan is appropriate for the user's current level
2. Emphasize the glucose control benefits of physical activity
3. Acknowledge starting point and progression plan
4. Be motivating but realistic about effort required
5. Keep explanation under 150 words
6. Include the mandatory disclaimer
7. Remind about safety precautions (glucose monitoring, hydration)

Focus on: motivation, safety, and achievable progression."""

        return prompt

    @staticmethod
    def create_weekly_summary_prompt(
        weekly_data: Dict[str, Any],
        previous_plan: Dict[str, Any],
        guidelines: Dict[str, Any]
    ) -> str:
        """
        Create prompt for LLM to summarize weekly progress and suggest adjustments.
        
        Args:
            weekly_data: Week's glucose readings and adherence
            previous_plan: Last week's care plan
            guidelines: Clinical guidelines
            
        Returns:
            Formatted prompt string
        """
        prompt = f"""Analyze this week's diabetes management data and provide guidance:

WEEKLY GLUCOSE DATA:
{json.dumps(weekly_data.get('glucose_readings', {}), indent=2)}

ADHERENCE DATA:
- Meal Plan Adherence: {weekly_data.get('meal_adherence', 'Not tracked')}%
- Activity Plan Adherence: {weekly_data.get('activity_adherence', 'Not tracked')}%

PREVIOUS PLAN:
{json.dumps(previous_plan, indent=2)}

GUIDELINES FOR REFERENCE:
- Target fasting: {guidelines.get('safety_thresholds', {}).get('fasting_glucose', {}).get('target_min', 80)}-{guidelines.get('safety_thresholds', {}).get('fasting_glucose', {}).get('target_max', 130)} mg/dL
- Target post-meal: <{guidelines.get('safety_thresholds', {}).get('post_meal_glucose', {}).get('target', 180)} mg/dL

INSTRUCTIONS:
1. Identify trends: Are glucose levels improving, stable, or worsening?
2. Recognize adherence efforts (even if glucose hasn't changed yet)
3. Suggest ONE specific, actionable adjustment if needed
4. If glucose is in red flag range, emphasize medical consultation
5. Keep summary under 200 words
6. Be supportive and evidence-based
7. Include mandatory disclaimer
8. NEVER suggest medication changes

Focus on: pattern recognition, encouragement, and one clear next step."""

        return prompt

    @staticmethod
    def create_escalation_prompt(
        health_data: Dict[str, Any],
        safety_flags: List[str]
    ) -> str:
        """
        Create prompt for LLM to communicate urgent situations appropriately.
        
        Args:
            health_data: Current health metrics
            safety_flags: List of safety concerns identified
            
        Returns:
            Formatted prompt string
        """
        prompt = f"""URGENT: Create a clear, calm message for a user with concerning glucose levels:

HEALTH DATA:
{json.dumps(health_data, indent=2)}

SAFETY FLAGS TRIGGERED:
{json.dumps(safety_flags, indent=2)}

INSTRUCTIONS:
1. Clearly state the concern without causing panic
2. Emphasize IMMEDIATE need to contact healthcare provider
3. List specific actions to take NOW:
   - Contact doctor/diabetes care team
   - Monitor glucose more frequently
   - Have emergency contact ready
4. Do NOT provide specific medical treatment advice
5. Keep message under 100 words
6. Be clear and direct while remaining supportive
7. Use urgent but not alarming tone

This is a safety-critical communication. Prioritize clarity and action."""

        return prompt

    @staticmethod
    def format_llm_request(
        system_prompt: str,
        user_prompt: str
    ) -> Dict[str, Any]:
        """
        Format prompts for LLM API call.
        
        Args:
            system_prompt: System-level instructions
            user_prompt: User-specific prompt
            
        Returns:
            Formatted request dictionary
        """
        return {
            "model": "claude-sonnet-4-5-20250929",  # or your preferred model
            "max_tokens": 1000,
            "system": system_prompt,
            "messages": [
                {
                    "role": "user",
                    "content": user_prompt
                }
            ]
        }


# Example usage and testing
if __name__ == "__main__":
    prompts = PlannerPrompts()
    
    # Example: Meal plan explanation
    user_profile = {
        "age": 45,
        "diet_type": "vegetarian",
        "region": "India"
    }
    
    health_data = {
        "avg_fasting_glucose": 160,
        "avg_post_meal_glucose": 210
    }
    
    meal_plan = {
        "breakfast": "Vegetable oats with nuts",
        "lunch": "Brown rice, dal, mixed vegetables",
        "dinner": "Chapati with vegetable curry"
    }
    
    guidelines = {
        "safety_thresholds": {
            "fasting_glucose": {"target_min": 80, "target_max": 130},
            "post_meal_glucose": {"target": 180}
        },
        "diet_guidelines": {
            "fiber": "25-30g/day"
        }
    }
    
    print("="*60)
    print("SYSTEM PROMPT")
    print("="*60)
    print(prompts.SYSTEM_PROMPT)
    print("\n" + "="*60)
    print("MEAL EXPLANATION PROMPT")
    print("="*60)
    
    meal_prompt = prompts.create_meal_explanation_prompt(
        user_profile, health_data, meal_plan, guidelines
    )
    print(meal_prompt)
    
    print("\n" + "="*60)
    print("FORMATTED API REQUEST")
    print("="*60)
    
    api_request = prompts.format_llm_request(
        prompts.SYSTEM_PROMPT,
        meal_prompt
    )
    print(json.dumps(api_request, indent=2))