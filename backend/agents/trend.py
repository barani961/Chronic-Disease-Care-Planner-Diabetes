import pandas as pd

def analyze(logs):
    df = pd.DataFrame(logs)
    trend = df["glucose"].mean()

    if trend > 160:
        return "Glucose trending high"
    return "Stable"
