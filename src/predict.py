import joblib

print("🔹 Day 7 – System Testing Started")
print("✅ User-Driven Prompt Injection Testing")

# --------------------------------------------------
# Load Model & Vectorizer (from Day 6)
# --------------------------------------------------
tfidf = joblib.load("models/tfidf_vectorizer.pkl")
model = joblib.load("models/classifier_model.pkl")

print("✅ Model & Vectorizer Loaded Successfully")


# --------------------------------------------------
# Detection Function (Day 6)
# --------------------------------------------------
def detect_prompt(prompt):
    vector = tfidf.transform([prompt])
    prediction = model.predict(vector)[0]   # 0 = Safe, 1 = Malicious
    confidence = model.predict_proba(vector).max()
    return prediction, confidence


# --------------------------------------------------
# Security Layer (Day 6)
# --------------------------------------------------
# --------------------------------------------------
# Security Layer (Day 6 + Confidence Threshold)
# --------------------------------------------------
def security_layer(prompt):
    prompt_lower = prompt.lower()

    # ------------------------------
    # Rule-based blocking
    # ------------------------------
    FORBIDDEN_KEYWORDS = [
        # General hacking / malicious
        "hack", "hacking", "bypass", "exploit", "steal", "attack",
        # Credentials / sensitive info
        "password", "admin", "root", "secret", "token", "credentials",
        "ip address", "credit card", "ssn", "social security",
        # Instructions override
        "ignore previous", "override instructions", "forget rules", "disable safety",
        "reveal system", "show hidden", "give access", "unblock", "sudo",
        # Dangerous commands
        "delete", "drop table", "format", "shutdown", "restart system",
        # Data exfiltration / secret info
        "copy files", "download", "export data", "send to", "extract"
    ]

    for keyword in FORBIDDEN_KEYWORDS:
        if keyword in prompt_lower:
            return {
                "status": "❌ BLOCKED",
                "label": "Rule-Based Malicious Prompt",
                "confidence": 1.0
            }

    # ------------------------------
    # ML-based detection
    # ------------------------------
    prediction, confidence = detect_prompt(prompt)
    THRESHOLD = 0.75  # Only block if confidence >= threshold

    if prediction == 1 and confidence >= THRESHOLD:
        return {
            "status": "❌ BLOCKED",
            "label": "ML-Detected Malicious Prompt",
            "confidence": round(confidence, 3)
        }
    else:
        return {
            "status": "✅ ALLOWED",
            "label": "Safe Prompt",
            "confidence": round(confidence, 3)
        }




# --------------------------------------------------
# Day 7 – Manual System Testing
# --------------------------------------------------
print("\n🔐 Prompt Injection Detection System")
print("----------------------------------")
print("Type 'exit' to stop testing\n")

while True:
    user_prompt = input("Enter a prompt: ").strip()

    if user_prompt.lower() == "exit":
        print("\n✅ Day 7 testing completed.")
        break

    result = security_layer(user_prompt)

    print("\n🔍 Detection Result")
    print("------------------")
    print("Status     :", result["status"])
    print("Label      :", result["label"])
    print("Confidence :", result["confidence"])
    print("-" * 45)
