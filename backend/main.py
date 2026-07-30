from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import torch
from transformers import MarianMTModel, MarianTokenizer
import pandas as pd
import os

app = FastAPI(title="Synctype Khmer Translator API", version="1.0.0")

# ------------------------------------
# CORS — allow production URLs
# ------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",   # Vite dev server
        "http://127.0.0.1:5173",
        "http://localhost:3000",   # Alternative port
        "http://127.0.0.1:3000",
        os.getenv("FRONTEND_URL", ""),  # Environment variable for custom URL
    ],
    allow_origin_regex=r"https://.*\.vercel\.app",  # Allow any Vercel deployment
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------------
# Load Model + Tokenizer (once)
# ------------------------------------
MODEL_PATH = "./synctype-final"
model = None
tokenizer = None
device = None

def load_model():
    global model, tokenizer, device
    if model is None:
        m = MarianMTModel.from_pretrained(MODEL_PATH)
        t = MarianTokenizer.from_pretrained(MODEL_PATH)
        d = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        m = m.to(d)
        m.eval()
        model, tokenizer, device = m, t, d
    return model, tokenizer, device

# ------------------------------------
# Load Dictionary
# ------------------------------------
CSV_PATH = "./combined_dataset_v2.csv"
lookup: dict = {}

def load_lookup():
    global lookup
    if not lookup and os.path.exists(CSV_PATH):
        df = pd.read_csv(CSV_PATH)
        for _, row in df.iterrows():
            lookup[str(row["roman"]).strip().lower()] = str(row["khmer"]).strip()
    return lookup

# ------------------------------------
# Startup
# ------------------------------------
@app.on_event("startup")
async def startup_event():
    load_lookup()
    # Model loads lazily on first request via load_model()
    # This ensures the port opens quickly for Render's health check

# ------------------------------------
# Preprocessing
# ------------------------------------
def to_char_level(text: str) -> str:
    return " ".join(list(str(text).strip()))

# ------------------------------------
# Model Prediction
# ------------------------------------
def predict(text: str) -> str:
    m, t, d = load_model()
    text = text.lower().strip()
    text = to_char_level(text)

    inputs = t(
        text,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=80,
    ).to(d)

    with torch.no_grad():
        outputs = m.generate(**inputs, max_length=80)

    decoded = t.decode(outputs[0], skip_special_tokens=True)
    return decoded.replace(" ", "")

# ------------------------------------
# Hybrid Prediction
# ------------------------------------
def hybrid_predict(sentence: str) -> str:
    lkp = load_lookup()
    words = sentence.lower().split()
    result = []
    for w in words:
        if w in lkp:
            result.append(lkp[w])
        else:
            result.append(predict(w))
    return "".join(result)

# ------------------------------------
# Request / Response schemas
# ------------------------------------
class TranslateRequest(BaseModel):
    text: str
    mode: str = "hybrid"   # "hybrid" | "model"

class TranslateResponse(BaseModel):
    result: str
    mode: str

class TranslateRequestNew(BaseModel):
    text: str

class TranslateResponseNew(BaseModel):
    translation: str
    confidence: float | None = None
    matched_roman: str = ""

class SuggestRequest(BaseModel):
    text: str
    max_results: int = 5

class SuggestResponse(BaseModel):
    suggestions: list[dict]

# ------------------------------------
# Endpoints
# ------------------------------------
@app.get("/")
def root():
    return {"status": "ok", "message": "Synctype Khmer Translator API"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/translate", response_model=TranslateResponse)
def translate(body: TranslateRequest):
    text = body.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="Text must not be empty.")

    try:
        if body.mode == "model":
            result = predict(text)
        else:
            result = hybrid_predict(text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Translation error: {str(e)}")

    return TranslateResponse(result=result, mode=body.mode)

@app.post("/api/translate", response_model=TranslateResponseNew)
def translate_new(body: TranslateRequestNew):
    """New endpoint for the updated frontend"""
    text = body.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="Text must not be empty.")

    try:
        # Use hybrid mode by default
        lkp = load_lookup()
        words = text.lower().split()
        
        # Check if we have a direct match in dictionary
        matched_roman = ""
        confidence = None
        
        # If it's a single word and in dictionary, set high confidence
        if len(words) == 1 and words[0] in lkp:
            result = lkp[words[0]]
            matched_roman = words[0]
            confidence = 0.95
        else:
            # Use hybrid prediction
            result = hybrid_predict(text)
            # Calculate rough confidence based on dictionary matches
            matches = sum(1 for w in words if w in lkp)
            if len(words) > 0:
                confidence = matches / len(words)
            else:
                confidence = 0.5
            
            # Try to find the closest match in dictionary
            if words and words[0] in lkp:
                matched_roman = words[0]
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Translation error: {str(e)}")

    return TranslateResponseNew(
        translation=result,
        confidence=confidence,
        matched_roman=matched_roman
    )

@app.post("/api/suggest", response_model=SuggestResponse)
def suggest(body: SuggestRequest):
    """Suggest possible translations based on dictionary matches"""
    text = body.text.strip().lower()
    if not text:
        return SuggestResponse(suggestions=[])
    
    try:
        lkp = load_lookup()
        suggestions = []
        
        # Find exact matches and partial matches
        for roman, khmer in lkp.items():
            if roman.startswith(text):
                suggestions.append({
                    "roman": roman,
                    "khmer": khmer,
                    "confidence": 0.9 if roman == text else 0.7
                })
        
        # Sort by confidence and limit results
        suggestions.sort(key=lambda x: x["confidence"], reverse=True)
        suggestions = suggestions[:body.max_results]
        
    except Exception as e:
        return SuggestResponse(suggestions=[])
    
    return SuggestResponse(suggestions=suggestions)
