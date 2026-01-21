from fastapi import FastAPI
from database import (
    patients,
    test_results,
    diet_plans,
    daily_activity,
    medication_plan,
    alerts
)
from models import (
    Patient,
    TestResult,
    DietPlan,
    DailyActivity,
    MedicationPlan
)
from agents.planner import create_plan
from agents.trend import analyze
from agents.safety import check
from services.llm import ask_llama
import requests

app = FastAPI(title="Chronic Care Planner API")

# ---------------- BASIC ----------------
@app.get("/")
def root():
    return {"status": "Backend connected"}

# ---------------- PATIENT ----------------
@app.post("/patient")
def add_patient(p: Patient):
    patients.insert_one(p.dict())
    return {"status": "Patient added"}

# ---------------- TEST RESULTS ----------------
@app.post("/test")
def add_test(test: TestResult):
    test_results.insert_one(test.dict())
    return {"status": "Test result saved"}

@app.get("/test/latest/{patient_id}")
def get_latest_test(patient_id: str):
    test = test_results.find_one(
        {"patient_id": patient_id},
        sort=[("_id", -1)]
    )
    if not test:
        return {"error": "No test results"}
    test["_id"] = str(test["_id"])
    return test

# ---------------- DIET PLAN ----------------
@app.post("/diet")
def save_diet(plan: DietPlan):
    diet_plans.insert_one(plan.dict())
    return {"status": "Diet plan saved"}

@app.get("/diet/{patient_id}/{day}")
def get_diet(patient_id: str, day: str):
    plan = diet_plans.find_one({"patient_id": patient_id, "day": day})
    if not plan:
        return {"error": "Diet plan not found"}
    plan["_id"] = str(plan["_id"])
    return plan

# ---------------- DAILY ACTIVITY ----------------
@app.post("/activity")
def log_activity(activity: DailyActivity):
    daily_activity.insert_one(activity.dict())
    return {"status": "Activity logged"}

@app.get("/activity/{patient_id}/{date}")
def get_activity(patient_id: str, date: str):
    log = daily_activity.find_one({"patient_id": patient_id, "date": date})
    if not log:
        return {"error": "No activity found"}
    log["_id"] = str(log["_id"])
    return log

# ---------------- MEDICATION PLAN ----------------
@app.post("/medication")
def save_medication(plan: MedicationPlan):
    medication_plan.insert_one(plan.dict())
    return {"status": "Medication plan saved"}

@app.get("/medication/{patient_id}")
def get_medication(patient_id: str):
    plan = medication_plan.find_one(
        {"patient_id": patient_id},
        sort=[("_id", -1)]
    )
    if not plan:
        return {"error": "No medication plan"}
    plan["_id"] = str(plan["_id"])
    return plan

# ---------------- AGENTIC AI ----------------
@app.get("/trend/{patient_id}")
def trends(patient_id: str):
    logs = list(test_results.find({"patient_id": patient_id}))
    if not logs:
        return {"error": "No data"}
    return {"trend": analyze(logs)}

@app.get("/alert/{patient_id}")
def alert(patient_id: str):
    last = test_results.find_one(
        {"patient_id": patient_id},
        sort=[("_id", -1)]
    )
    if not last:
        return {"error": "No test data"}
    return {"alert": check(last["fasting_sugar"])}

# ---------------- OLLAMA TEST ----------------
@app.get("/ollama-test")
def test_ollama():
    r = requests.post(
        "http://127.0.0.1:11434/api/generate",
        json={
            "model": "llama3.2",
            "prompt": "Reply in one sentence: Weekly care advice",
            "stream": False
        }
    )
    return {"response": r.json()["response"]}

@app.get("/llama-test")
def llama_test():
    return {"response": ask_llama("Explain Type 2 Diabetes in one line")}
