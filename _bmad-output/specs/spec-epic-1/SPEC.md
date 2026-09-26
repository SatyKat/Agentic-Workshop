---
id: SPEC-epic-1
companions: []
sources: [../../../INTENT.md]
---

> **Canonical contract.** This SPEC and the files in `companions:` are the complete, preservation-validated contract for what to build, test, and validate. Source documents listed in frontmatter are for traceability — consult them only if you need narrative rationale or prose color this contract intentionally omits.

# Epic 1: triage data and schema

## Why

The workshop needs a foundation for Epics 2 and 3. Epic 1 provides two things: a JSON schema that defines what a triage decision looks like (contract), and a loader that populates the SQLite database from CSV seed data. With these in place, the agent (Epic 2) has a clear decision format to work toward, and the MCP server already has data to query.

## Capabilities

- **CAP-1**
  - **intent:** Every triage decision conforms to a single JSON schema.
  - **success:** A triage decision is a JSON object with category (one of: billing, bug, access, performance, how-to), priority (P1, P2, P3, or P4), route (one of: billing-team, bug-team, access-team, performance-team, how-to-team), and rationale (a single sentence). Anything that fails this schema is rejected with a clear error message.

- **CAP-2**
  - **intent:** A person can load seed data into the database with one command.
  - **success:** Running `uv run python load_seed.py` reads `seed/tickets.csv` and `seed/customers.csv`, creates a local SQLite database at `app.db`, and populates two tables named `tickets` and `customers` with the same columns as the CSV files. Running the command twice produces an identical database (idempotent).

## Constraints

- Python 3.12 or newer, managed with uv.
- The `seed/` directory is read-only — no changes to `seed/tickets.csv`, `seed/customers.csv`, or any other files under `seed/`.
- No network calls and no API keys in this epic. All work is local to the machine.
- The MCP server at `mcp/triage_server.py` already reads from `app.db`. Table names (`tickets`, `customers`) and column names must remain compatible so the MCP server's queries continue to work.

## Non-goals

- The agent that makes triage decisions (Epic 2).
- MCP tools, evaluation harness, or any user interface.
- Integration with external systems or APIs.

## Success signal

Running `uv run python load_seed.py` creates `app.db` with `tickets` and `customers` tables. A triage decision JSON that matches CAP-1's schema validates; one that doesn't is rejected with a clear error. The MCP server at `mcp/triage_server.py` successfully queries the populated database without modification.
