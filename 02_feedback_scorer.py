from pydantic import BaseModel, Field

from laya import Router


class FeedbackDecision(BaseModel):
    severity: float = Field(ge=0, le=3)
    needs_immediate_attention: bool


def main() -> None:
    feedback = (
        "The checkout page crashes for every customer, "
        "so nobody can complete a purchase."
    )

    router = Router()
    result = router.predict(
        {"feedback": feedback},
        {
            "severity": {
                "type": "score",
                "instructions": (
                    "Rate the impact of this feedback from 0 to 3."
                ),
                "criteria": [
                    "Cosmetic or negligible issue",
                    "Minor inconvenience",
                    "Major feature impaired",
                    "Critical workflow blocked",
                ],
            },
            "immediate": {
                "type": "noul",
                "instructions": (
                    "Does this issue require immediate attention?"
                ),
            },
        },
    )

    answers = result["answers"]
    decision = FeedbackDecision.model_validate(
        {
            "severity": answers["severity"]["score"],
            "needs_immediate_attention": (
                answers["immediate"]["noul"] >= 0.5
            ),
        }
    )

    print("Selected model:", result["routing"]["model"])
    print(decision.model_dump_json(indent=2))


if __name__ == "__main__":
    main()
