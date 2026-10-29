
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Bilingual AI Customer Support API",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
        "http://127.0.0.1:5500",
        "https://bilingual-ai-customer.github.io",
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Temporary sample complaints until the ML model is connected.
sample_complaints = [
    {
        "id": 1,
        "text": "My order has not arrived yet.",
        "category": "Shipping & Delivery",
        "priority": "High",
        "status": "Open",
        "aiConfidence": 0.93,
        "reply": "We apologize for the delay. We will check your order.",
        "sources": ["Shipping Policy.pdf"],
    },
    {
        "id": 2,
        "text": "I cannot log in to my account.",
        "category": "Account",
        "priority": "Medium",
        "status": "In Progress",
        "aiConfidence": 0.88,
        "reply": "Please reset your password and try again.",
        "sources": ["Account Help.pdf"],
    },
    {
        "id": 3,
        "text": "I was charged twice for my purchase.",
        "category": "Payment",
        "priority": "High",
        "status": "Open",
        "aiConfidence": 0.96,
        "reply": "We will review the duplicate charge.",
        "sources": ["Payment Policy.pdf"],
    },
]


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/complaints")
def get_complaints():
    return sample_complaints
