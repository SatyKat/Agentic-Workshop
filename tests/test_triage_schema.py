"""Tests for the triage decision schema.

Validates that TriageDecision enforces the contract: category, priority, route,
and rationale are all required, have restricted valid values, and validation
errors provide clear messages.
"""

import json

import pytest
from pydantic import ValidationError

from triage import TriageDecision, parse_triage_decision


class TestTriageDecisionValidation:
    """Tests for TriageDecision model validation."""

    def test_valid_decision(self) -> None:
        """A valid decision with all required fields parses correctly."""
        decision = TriageDecision(
            category="billing",
            priority="P2",
            route="billing-team",
            rationale="Customer was double-charged this month."
        )
        assert decision.category == "billing"
        assert decision.priority == "P2"
        assert decision.route == "billing-team"
        assert decision.rationale == "Customer was double-charged this month."

    def test_valid_decision_all_categories(self) -> None:
        """All valid categories are accepted."""
        categories = ["billing", "bug", "access", "performance", "how-to"]
        for cat in categories:
            decision = TriageDecision(
                category=cat,
                priority="P1",
                route="billing-team",
                rationale="test"
            )
            assert decision.category == cat

    def test_valid_decision_all_priorities(self) -> None:
        """All valid priorities are accepted."""
        priorities = ["P1", "P2", "P3", "P4"]
        for priority in priorities:
            decision = TriageDecision(
                category="billing",
                priority=priority,
                route="billing-team",
                rationale="test"
            )
            assert decision.priority == priority

    def test_valid_decision_all_routes(self) -> None:
        """All valid routes are accepted."""
        routes = ["billing-team", "bug-team", "access-team", "performance-team", "how-to-team"]
        for route in routes:
            decision = TriageDecision(
                category="billing",
                priority="P1",
                route=route,
                rationale="test"
            )
            assert decision.route == route

    def test_invalid_category(self) -> None:
        """An invalid category raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            TriageDecision(
                category="unknown",
                priority="P1",
                route="billing-team",
                rationale="test"
            )
        error = exc_info.value
        assert "category" in str(error).lower()

    def test_invalid_priority(self) -> None:
        """An invalid priority raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            TriageDecision(
                category="billing",
                priority="P5",
                route="billing-team",
                rationale="test"
            )
        error = exc_info.value
        assert "priority" in str(error).lower()

    def test_invalid_route(self) -> None:
        """An invalid route raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            TriageDecision(
                category="billing",
                priority="P1",
                route="unknown-team",
                rationale="test"
            )
        error = exc_info.value
        assert "route" in str(error).lower()

    def test_missing_category(self) -> None:
        """Missing category field raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            TriageDecision(
                priority="P1",
                route="billing-team",
                rationale="test"
            )
        error = exc_info.value
        assert "category" in str(error).lower()

    def test_missing_priority(self) -> None:
        """Missing priority field raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            TriageDecision(
                category="billing",
                route="billing-team",
                rationale="test"
            )
        error = exc_info.value
        assert "priority" in str(error).lower()

    def test_missing_route(self) -> None:
        """Missing route field raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            TriageDecision(
                category="billing",
                priority="P1",
                rationale="test"
            )
        error = exc_info.value
        assert "route" in str(error).lower()

    def test_missing_rationale(self) -> None:
        """Missing rationale field raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            TriageDecision(
                category="billing",
                priority="P1",
                route="billing-team"
            )
        error = exc_info.value
        assert "rationale" in str(error).lower()

    def test_empty_rationale(self) -> None:
        """An empty rationale string is accepted (no length validation in spec)."""
        decision = TriageDecision(
            category="billing",
            priority="P1",
            route="billing-team",
            rationale=""
        )
        assert decision.rationale == ""


class TestTriageDecisionSerialization:
    """Tests for JSON serialization and deserialization."""

    def test_to_json(self) -> None:
        """A TriageDecision can be serialized to JSON."""
        decision = TriageDecision(
            category="billing",
            priority="P2",
            route="billing-team",
            rationale="Customer was double-charged."
        )
        json_str = decision.model_dump_json()
        data = json.loads(json_str)
        assert data["category"] == "billing"
        assert data["priority"] == "P2"
        assert data["route"] == "billing-team"
        assert data["rationale"] == "Customer was double-charged."

    def test_to_dict(self) -> None:
        """A TriageDecision can be converted to a dictionary."""
        decision = TriageDecision(
            category="bug",
            priority="P1",
            route="bug-team",
            rationale="Export button broken in Firefox."
        )
        data = decision.model_dump()
        assert data == {
            "category": "bug",
            "priority": "P1",
            "route": "bug-team",
            "rationale": "Export button broken in Firefox."
        }


class TestParseTriageDecision:
    """Tests for the parse_triage_decision helper function."""

    def test_parse_from_dict(self) -> None:
        """parse_triage_decision accepts a dictionary."""
        data = {
            "category": "billing",
            "priority": "P2",
            "route": "billing-team",
            "rationale": "Customer was double-charged."
        }
        decision = parse_triage_decision(data)
        assert decision.category == "billing"
        assert decision.priority == "P2"

    def test_parse_from_json_string(self) -> None:
        """parse_triage_decision accepts a JSON string."""
        json_str = json.dumps({
            "category": "bug",
            "priority": "P1",
            "route": "bug-team",
            "rationale": "Export button broken."
        })
        decision = parse_triage_decision(json_str)
        assert decision.category == "bug"
        assert decision.priority == "P1"

    def test_parse_invalid_dict(self) -> None:
        """parse_triage_decision raises ValidationError for invalid dict."""
        data = {
            "category": "unknown",
            "priority": "P1",
            "route": "billing-team",
            "rationale": "test"
        }
        with pytest.raises(ValidationError):
            parse_triage_decision(data)

    def test_parse_invalid_json_string(self) -> None:
        """parse_triage_decision raises ValidationError for invalid JSON values."""
        json_str = json.dumps({
            "category": "billing",
            "priority": "P99",
            "route": "billing-team",
            "rationale": "test"
        })
        with pytest.raises(ValidationError):
            parse_triage_decision(json_str)

    def test_parse_malformed_json_string(self) -> None:
        """parse_triage_decision raises JSONDecodeError for malformed JSON."""
        with pytest.raises(json.JSONDecodeError):
            parse_triage_decision("not valid json {")
