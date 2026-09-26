"""Triage decision schema and validation.

This module defines a Pydantic model for triage decisions that ensures all
decisions conform to the Epic 1 contract: a JSON object with category, priority,
route, and rationale fields, all strongly typed and validated.
"""

import json
from typing import Literal

from pydantic import BaseModel, Field, ValidationError


class TriageDecision(BaseModel):
    """A validated triage decision for a support ticket.

    Attributes:
        category: The issue category (billing, bug, access, performance, or how-to)
        priority: The urgency level (P1, P2, P3, or P4)
        route: The team responsible for handling the ticket
        rationale: A single-sentence explanation for the decision
    """

    category: Literal["billing", "bug", "access", "performance", "how-to"]
    priority: Literal["P1", "P2", "P3", "P4"]
    route: Literal["billing-team", "bug-team", "access-team", "performance-team", "how-to-team"]
    rationale: str = Field(..., description="A single sentence explaining the decision")

    model_config = {"json_schema_extra": {"examples": [
        {
            "category": "billing",
            "priority": "P2",
            "route": "billing-team",
            "rationale": "Customer was double-charged this month."
        }
    ]}}


def parse_triage_decision(data: dict | str) -> TriageDecision:
    """Parse and validate a triage decision from raw data.

    Args:
        data: Either a dictionary or a JSON string containing triage decision fields

    Returns:
        A validated TriageDecision object

    Raises:
        ValidationError: If the data doesn't conform to the schema
        json.JSONDecodeError: If data is a string that isn't valid JSON
    """
    if isinstance(data, str):
        data = json.loads(data)
    return TriageDecision(**data)
