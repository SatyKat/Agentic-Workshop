# Epic 1 Context: Triage Data and Schema

<!-- Compiled from spec-epic-1/SPEC.md and stories.yaml -->

## Goal

Provide the foundation for the workshop's triage agent. Epic 1 establishes what a triage decision looks like (a validated JSON schema) and how to load the seed data the agent will reason over. With these in place, Epic 2's agent has a clear decision format to work toward, and the MCP server has populated tables to query.

## Stories

- Story 1.1: Triage Schema — Define and validate the triage-decision JSON schema
- Story 1.2: Seed Data Loader — Load seed data into SQLite database

## Requirements & Constraints

- **Triage Decision Schema (CAP-1):** Every decision is a JSON object with four fields:
  - `category` (one of: billing, bug, access, performance, how-to)
  - `priority` (one of: P1, P2, P3, P4)
  - `route` (one of: billing-team, bug-team, access-team, performance-team, how-to-team)
  - `rationale` (a single sentence)
  - Any decision that doesn't match this schema must be rejected with a clear error message.

- **Seed Data Loader (CAP-2):** One command `uv run python load_seed.py` loads two CSV files (`seed/tickets.csv`, `seed/customers.csv`) into a local SQLite database (`app.db`) with two tables (`tickets`, `customers`) with the same columns as the CSV files. The loader must be idempotent — running it twice produces an identical database.

- **Python & Package Management:** Python 3.12 or newer, managed with uv.
- **Read-Only Seed Data:** The `seed/` directory is read-only. No modifications to seed files.
- **Local Only:** No network calls and no API keys in this epic. All work is local.
- **MCP Compatibility:** The MCP server at `mcp/triage_server.py` already reads from `app.db`. Table and column names must remain compatible so the server's queries work without modification.

## Cross-Story Dependencies

Story 1.1 (Schema) has no dependencies. Story 1.2 (Loader) depends on Story 1.1 being complete so the schema can validate loaded data if needed.
