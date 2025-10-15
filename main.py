import requests
from fastapi import FastAPI, UploadFile, File, Form
from pydantic import BaseModel
import pytesseract
from PIL import Image
import time
from typing import List

app = FastAPI()

# Hugging Face API endpoint and headers
HF_API_URL = "https://api-inference.huggingface.co/models/bert-base-uncased"
HF_API_KEY = "your_hugging_face_api_key_here"  # Replace with your Hugging Face API key

headers = {
    "Authorization": f"Bearer {HF_API_KEY}"
}

# OCR function for prescription recognition
def ocr_recognition(image: UploadFile) -> str:
    img = Image.open(image.file)
    text = pytesseract.image_to_string(img)
    return text

# Function to make requests to Hugging Face API for drug compatibility and recommendation
def hugface_request(payload: dict) -> dict:
    response = requests.post(HF_API_URL, headers=headers, json=payload)
    return response.json()

# Drug compatibility checker (simplified for demonstration)
def check_compatibility(drugs: List[str]) -> str:
    # Example using Hugging Face model (you can use a model specific to drug interaction analysis)
    payload = {"inputs": "Check compatibility between " + ", ".join(drugs)}
    response = hugface_request(payload)
    # Assuming response contains compatibility information
    return response.get('compatibility_info', 'No information available')

# Recommend drugs based on symptoms using Hugging Face model
def recommend_drug(symptoms: str) -> str:
    payload = {"inputs": symptoms}
    response = hugface_request(payload)
    # Assuming response contains a recommended drug
    return response.get('recommended_drug', 'No recommendation available')

# Purchase functionality (simplified)
def purchase_medication(medication: str) -> str:
    return f"Medication {medication} purchased successfully."

class PrescriptionData(BaseModel):
    image: UploadFile

class DrugRequest(BaseModel):
    symptoms: str

class PurchaseRequest(BaseModel):
    medication: str

@app.post("/ocr/")
async def ocr_endpoint(prescription: PrescriptionData):
    start_time = time.time()
    text = ocr_recognition(prescription.image)
    latency = time.time() - start_time
    return {"ocr_text": text, "latency": latency}

@app.post("/check_compatibility/")
async def compatibility_endpoint(drugs: List[str]):
    return {"compatibility_check": check_compatibility(drugs)}

@app.post("/recommend/")
async def recommend_endpoint(request: DrugRequest):
    return {"recommendation": recommend_drug(request.symptoms)}

@app.post("/purchase/")
async def purchase_endpoint(request: PurchaseRequest):
    return {"purchase_status": purchase_medication(request.medication)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
