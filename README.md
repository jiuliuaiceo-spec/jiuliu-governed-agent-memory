# Governed Agent Memory

An open-source reference implementation for auditable memory, read-only enterprise knowledge retrieval, five-layer agent traces, and governed self-growth.

This repository is a clean-room extraction. It contains no production credentials, company data, private adapters, or deployment configuration.

## Core guarantees

- Every memory operation requires `task_id`, `event_id`, `conversation_id`, and `connector_run_id`.
- `policy_hash` and `goal_hash` are bound across retain, publish, and consolidate.
- Knowledge retrieval is read-only by default.
- Self-growth uses an explicit candidate lifecycle; candidates are never implicitly approved.
- Unavailable memory returns a visible degraded result instead of silently using stale context.
- Five-layer traces are recorded as evidence: cognition, planning, execution, memory, supervision.

## Quick start

```bash
python -m unittest -v
```

See [ARCHITECTURE.md](ARCHITECTURE.md).
