from typing import Literal

from laya import Router
from pydantic import BaseModel, Field


class HebrewTicketDecision(BaseModel):
    department: Literal[
        "חיובים", "תמיכה טכנית", "מכירות", "אחר"
    ]
    urgency: float = Field(ge=0, le=2)
    needs_human: bool


def main() -> None:
    message = (
        "חויבתי פעמיים על אותו מנוי.\n"
        "בנוסף, האפליקציה קורסת ואני לא מצליח להשתמש בשירות.\n"
        "אשמח לעזרה בהקדם."
    )

    # Router detects Hebrew and selects the appropriate checkpoint.
    # Do not force the English-only model for Hebrew input.
    router = Router()

    result = router.predict(
        {"message": message},
        {
            "department": {
                "type": "choice",
                "instructions": "איזה צוות צריך לטפל בפנייה?",
                "criteria": {
                    "חיובים": "תשלומים, חשבוניות והחזרים",
                    "תמיכה טכנית": "תקלות, קריסות ובעיות טכניות",
                    "מכירות": "רכישה, מחירים ושדרוגים",
                    "אחר": "נושאים אחרים",
                },
            },
            "urgency": {
                "type": "score",
                "instructions": "מה רמת הדחיפות של הפנייה?",
                "criteria": [
                    "דחיפות נמוכה",
                    "דחיפות בינונית",
                    "דחיפות קריטית",
                ],
            },
            "needs_human": {
                "type": "noul",
                "instructions": "האם נדרשת בדיקה של נציג אנושי?",
            },
        },
    )

    answers = result["answers"]

    # Convert the model's probability into an explicit application policy.
    decision = HebrewTicketDecision.model_validate(
        {
            "department": answers["department"]["choice"],
            "urgency": answers["urgency"]["score"],
            "needs_human": answers["needs_human"]["noul"] >= 0.5,
        }
    )

    print("Selected model:", result["routing"]["model"])
    print("Routing details:", result["routing"])
    print("החלטה מובנית:")
    print(decision.model_dump_json(indent=2))


if __name__ == "__main__":
    main()
