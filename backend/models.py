from pydantic import BaseModel
from typing import List

# ---------------- PATIENT ----------------
class Patient(BaseModel):
    patient_id: str
    name: str
    age: int
    conditions: List[str]

# ---------------- TEST RESULT ----------------
class TestResult(BaseModel):
    patient_id: str
    fasting_sugar: int
    post_meal_sugar: int
    date: str

# ---------------- DIET PLAN ----------------
class DietPlan(BaseModel):
    patient_id: str
    day: str  # Monday, Tuesday...
    morning: str
    afternoon: str
    night: str
    lifestyle: str

# ---------------- DAILY ACTIVITY ----------------
class DailyActivity(BaseModel):
    patient_id: str
    date: str

    day_food: bool
    day_medicine: bool
    exercise: bool

    afternoon_food: bool
    afternoon_medicine: bool

    night_food: bool
    night_medicine: bool

# ---------------- MEDICATION PLAN ----------------
class MedicationPlan(BaseModel):
    patient_id: str
    day: int
    afternoon: int
    night: int
