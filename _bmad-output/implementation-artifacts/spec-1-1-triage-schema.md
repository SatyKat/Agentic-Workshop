---
title: 'Triage Schema'
type: 'feature'
created: '2026-09-26'
status: 'in-progress'
route: 'oneshot'
review_loop_iteration: 0
baseline_commit: 'b019aa6'
context: ["_bmad-output/specs/spec-epic-1/SPEC.md", "_bmad-output/implementation-artifacts/epic-1-context.md"]
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** The agent needs a validated, strongly-typed schema for triage decisions so it can return decisions that conform to the Epic 1 contract. Every decision must have four fields (category, priority, route, rationale) with no flexibility — anything invalid must fail loudly.

**Approach:** Define a Pydantic model that encodes the valid values and validates automatically. Export a helper to parse and validate raw JSON.

## I/O & Edge-Case Matrix

| Scenario | Input | Expected Output | Error Handling |
|----------|-------|-----------------|----------------|
| Valid decision | `{"category": "billing", "priority": "P2", "route": "billing-team", "rationale": "customer is enterprise"}` | Parsed TriageDecision object | N/A |
| Invalid category | `{"category": "unknown", ...}` | — | Raise ValidationError with clear message |
| Missing field | `{"category": "billing", "priority": "P2"}` | — | Raise ValidationError naming the field |
| Invalid priority | `{"category": "bug", "priority": "P5", ...}` | — | Raise ValidationError with valid choices |

</frozen-after-approval>

## Implementation Notes

## Spec Change Log

## Review Triage Log

## Verification

**Commands:**
- `uv run pytest tests/test_triage_schema.py` -- all schema validation tests pass

**Manual checks:**
- `python -c "from triage import TriageDecision; d = TriageDecision(category='bug', priority='P1', route='bug-team', rationale='test'); print(d.model_dump_json())"` -- outputs valid JSON
