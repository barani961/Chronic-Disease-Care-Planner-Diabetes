from pydantic import BaseModel
from typing import List

class Patient(BaseModel):
    patient_id: str
    age: int
    condition: List[str]

class DailyLog(BaseModel):
    patient_id: str
    glucose: int
    bp: str
    steps: int
