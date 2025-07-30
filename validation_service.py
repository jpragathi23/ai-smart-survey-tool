# backend/app/services/validation_service.py

from app.models.survey_models import Question

# ----------------------------
# Real-Time Answer Validator
# ----------------------------
def validate_answer(question: Question, answer):
    try:
        # Check required answer presence
        if question.is_mandatory and (answer is None or answer == ""):
            return "invalid", 0

        # Type-based validation
        if question.question_type == "radio" or question.question_type == "checkbox":
            if isinstance(answer, list):
                valid = all(opt in question.options for opt in answer)
            else:
                valid = answer in question.options
            if not valid:
                return "invalid", 30

        # Custom rules (basic only)
        rules = question.validation_rules or {}
        if rules.get("numeric_only") and not str(answer).isdigit():
            return "invalid", 20

        # Passed all checks
        return "valid", 100

    except Exception as e:
        print(f"Validation error: {e}")
        return "error", 0
