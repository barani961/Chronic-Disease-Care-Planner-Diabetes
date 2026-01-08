from fastapi import FastAPI
from database import patients, logs, plans, alerts
from models import Patient, DailyLog
from agents.planner import create_plan
from agents.trend import analyze
from agents.safety import check
from services.llm import ask_llama
import requests

app = FastAPI()

@app.get("/")
def hello():
    return {"status": "connected"}

@app.post("/patient")
def add_patient(p: Patient):
    patients.insert_one(p.dict())
    return {"status": "Patient added"}

@app.post("/log")
def add_log(log: DailyLog):
    logs.insert_one(log.dict())
    return {"status": "Log saved"}

@app.get("/plan/{patient_id}")
def generate_plan(patient_id: str):
    patient = patients.find_one({"patient_id": patient_id})
    if not patient:
        return {"error": "Patient not found"}

    plan = create_plan(patient)
    plans.insert_one({"patient_id": patient_id, "plan": plan})
    return {"plan": plan}

@app.get("/trend/{patient_id}")
def trends(patient_id: str):
    user_logs = list(logs.find({"patient_id": patient_id}))
    if not user_logs:
        return {"error": "No logs found"}

    return {"trend": analyze(user_logs)}

@app.get("/alert/{patient_id}")
def alert(patient_id: str):
    last = logs.find_one(
        {"patient_id": patient_id},
        sort=[("_id", -1)]
    )

    if not last:
        return {"error": "No logs found"}

    return {"alert": check(last["glucose"])}

# 🔥 Test Ollama directly
@app.get("/ollama-test")
def test_ollama():
    r = requests.post("http://127.0.0.1:11434/api/generate", json={
        "model": "llama3.2",
        "prompt": "Reply in one sentence: What is diabetes?",
        "stream": False
    })
    return {"ollama_response": r.json()["response"]}

# 🔥 Test via your LLM service wrapper
@app.get("/llama-test")
def llama_test():
    answer = ask_llama("In one line, explain Type 2 Diabetes")
    return {"llama_response": answer}
