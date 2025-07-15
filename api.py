import uvicorn
import pandas as pd
from fastapi import FastAPI
from utils.common import process_single_customer

"""STILL IN PROGRESS.... DO NOT RUN YET"""

app = FastAPI()

@app.post("/flashcard-customer")
def flashcard_generation_for_specific_customer(data: dict):
    customer_name = data['customer_name']
    prompt_variation = data['prompt_variation']
    model_name = data['model_name']

    return process_single_customer(customer_name, prompt_variation, model_name)

@app.get("/flashcard-data-csv/{user_name}")
def retrieve_flashcard_data_csv(user_name: str):
    best_combinations = pd.read_csv("results/best_combinations.csv")
    user_data = best_combinations[best_combinations['customer_name'] == user_name]
    flashcard = user_data['flashcard'].values[0]
    academic_scores = user_data['academic_scores'].values[0]
    return {"flashcard": flashcard, "academic_scores": academic_scores}
    
if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)