from pymongo import MongoClient
from config import MONGO_URI, DB_NAME

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

patients = db["patients"]
test_results = db["test_results"]
diet_plans = db["diet_plans"]
daily_activity = db["daily_activity"]
medication_plan = db["medication_plan"]
alerts = db["alerts"]
