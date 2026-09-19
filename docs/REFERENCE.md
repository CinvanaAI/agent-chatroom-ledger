# Agent Chatroom Ledger


A durable, file-backed coordination room for people and configured software participants.

Each room keeps canonical append-only message records, a human-readable compiled view, participant state, per-consumer cursors, optional message versions, compile policy, operation reports, and a verification path. Administrative mutations are dry-run-first and require `--apply`.

## What it demonstrates

- restart-safe message IDs and lock handling;
- participant-gated unread scans and independent cursors;
- canonical records separated from compiled projections;
- message exclusion, inclusion, and explicit stand-ins;
- 0–9 message versions and consumer-specific context lenses;
- room creation, archive/restore, placement, and policy operations with evidence logs;
- structural verification and recovery from stale projections.

## Run it

```powershell
python -m unittest discover -s tests -v
agent-chatroom-ledger --root ./demo-data create-room --title "Synthetic Review" --participants Avery,Codex --apply
agent-chatroom-ledger --root ./demo-data verify
```

Without `--root`, the CLI uses `./chatroom-data`. It never contacts a model or network service.

The public suite currently passes 24 backend tests; 3 tests for the excluded
private host connector remain explicitly skipped. GitHub Actions runs the
suite, compiles the package, and builds its distribution artifacts.

## Focused mechanism

**Message Version Bundle Builder** presents the canonical-message plus numbered
context-view packaging rule independently. That utility came from the same
chatroom/context lineage; this repository remains the complete durable room and
cursor implementation.

## Privacy boundary

Message bodies are intentionally stored on disk and are not encrypted. Use an access-controlled directory and do not treat this as a secrecy layer. The original private rooms, transcripts, participant connector, cursors, and generated state are excluded; tests use synthetic content.

The public extraction preserves the backend and CLI. The host-specific Tk UI and Claude/Codex process connectors remain outside this repository.

See [ORIGIN.md](../ORIGIN.md) and [SECURITY.md](../SECURITY.md).
