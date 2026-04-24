# views.py
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
import joblib
from .models import PromptLog

from django.shortcuts import render
from .models import PromptLog

def dashboard_page(request):

    prompts = PromptLog.objects.order_by('-created_at')

    return render(request, "index.html", {
        "prompts": prompts
    })
# ---------------------------
# Page Views
# ---------------------------


def detect_page(request):
    return render(request, "detect.html")


# ---------------------------
# ML Model Setup
# ---------------------------
# Get project root directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # detection/
PROJECT_DIR = os.path.dirname(BASE_DIR)  # Parent folder

# Model file paths
VECTORIZER_PATH = os.path.join(PROJECT_DIR, 'models', 'tfidf_vectorizer.pkl')
MODEL_PATH = os.path.join(PROJECT_DIR, 'models', 'classifier_model.pkl')

# Load ML models safely
try:
    tfidf = joblib.load(VECTORIZER_PATH)
    model = joblib.load(MODEL_PATH)
    print("✅ ML models loaded successfully.")
except Exception as e:
    print("⚠️ ML models not loaded. Check paths and server.")
    print(e)
    tfidf = None
    model = None


# ---------------------------
# Analyze Prompt Endpoint
# ---------------------------
@csrf_exempt
def analyze(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request"})

    if not tfidf or not model:
        return JsonResponse({
            "status": "danger",
            "message": "⚠️ ML models not loaded. Check server."
        })

    prompt = request.POST.get("prompt", "").strip()
    prompt_lower = prompt.lower()

    # Rule-based forbidden keywords
    FORBIDDEN_KEYWORDS = [
        "hack", "reveal","hacking", "bypass", "exploit", "steal", "attack",
        "password", "admin", "root", "secret", "token", "credentials",
        "ip address", "credit card", "ssn", "social security",
        "ignore previous", "override instructions", "forget rules",
        "disable safety", "reveal system", "show hidden",
        "give access", "unblock", "sudo","leak", "delete", "drop table",
        "format", "shutdown", "restart system", "copy files", "download",
        "export data", "send to", "confidential","extract"
        
    ]

    # Check for forbidden keywords (Rule-based detection)
    for keyword in FORBIDDEN_KEYWORDS:
        if keyword in prompt_lower:
            # Save to DB
            PromptLog.objects.create(
                prompt_text=prompt,
                detection_type="Rule-Based",
                status="danger",
                confidence=1.0
            )
            return JsonResponse({
                "status": "danger",
                "message": "Status : ❌ BLOCKED\nLabel : Rule-Based Malicious Prompt\nConfidence : 1.000"
            })

    # ML-based prediction
    try:
        vector = tfidf.transform([prompt])
        prediction = model.predict(vector)[0]
        confidence = max(model.predict_proba(vector)[0])
    except Exception as e:
        print("⚠️ ML prediction error:", e)
        return JsonResponse({
            "status": "danger",
            "message": "⚠️ Error processing prompt. Check server."
        })

    THRESHOLD = 0.75

    if prediction == 1 and confidence >= THRESHOLD:
        # ML-detected malicious
        PromptLog.objects.create(
            prompt_text=prompt,
            detection_type="ML-Based",
            status="danger",
            confidence=confidence
        )
        return JsonResponse({
            "status": "danger",
            "message": f"Status : ❌ BLOCKED\nLabel : ML-Detected Malicious Prompt\nConfidence : {confidence:.3f}"
        })
    else:
        # Safe prompt
        PromptLog.objects.create(
            prompt_text=prompt,
            detection_type="ML-Based",
            status="safe",
            confidence=confidence
        )
        return JsonResponse({
            "status": "safe",
            "message": f"Status : ✅ ALLOWED\nLabel : Safe Prompt\nConfidence : {confidence:.3f}"
        })