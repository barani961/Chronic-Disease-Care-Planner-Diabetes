from services.llm import ask_llama


def create_plan(patient):
    prompt = f"""
    Create a Type-2 diabetes daily care plan for:
    Age: {patient['age']}
    Conditions: {patient['condition']}
    Return JSON.
    """
    return ask_llama(prompt)
