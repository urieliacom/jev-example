from typing import Literal

from pydantic import BaseModel, Field

import laya


class TicketDecision(BaseModel):
    department: Literal["billing", "technical", "sales", "other"] = Field(
        description="Which team should handle the ticket?"
    )
    urgency: int = Field(
        ge=0, le=2,
        description="Urgency: 0=low, 1=medium, 2=critical"
    )
    needs_human: bool = Field(
        description="Does this ticket require human review?"
    )


def main() -> None:
    message = (
        "We were charged twice for our subscription.\n"
        "The payment system is also failing for our team.\n"
        "Please resolve this urgently."
    )

    # Schema-driven decisions with a Pydantic model.
    agent = laya.load("convaiinnovations/laya")
    raw = agent.decide(message, schema=TicketDecision)
    decision = TicketDecision.model_validate(raw)

    print(decision.model_dump_json(indent=2))


if __name__ == "__main__":
    main()
