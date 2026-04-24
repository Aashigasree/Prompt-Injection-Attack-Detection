from django.db import models

class PromptLog(models.Model):
    prompt_text = models.TextField()
    detection_type = models.CharField(max_length=50)  # Rule-Based / ML
    status = models.CharField(max_length=20)  # safe / danger
    confidence = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.status} - {self.prompt_text[:40]}"