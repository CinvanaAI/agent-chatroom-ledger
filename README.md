# Agent Chatroom Ledger

Let several readers share a room without sharing one unread cursor.

A local coordination backend for keeping messages, room policy and each consumer's reading position across restarts. It grew from the historical Python workbench's multi-participant rooms: a rendered chat view and a model's context window both needed to be replaceable without losing the conversation's records. This extraction keeps the file-backed backend and CLI; the original UI and model-process connectors are outside the package. [Origin](ORIGIN.md).

Use it as a storage layer for your own reader, worker or context builder. It never contacts a model or messaging service.

## Watch two readers diverge, then recover a view

Python 3.11 or newer, from the checkout:

```sh
python -m pip install -e .
python -m examples.walkthrough
```

[Walkthrough source](examples/walkthrough.py) · [Captured synthetic output](examples/result.txt)

Two synthetic messages arrive for Analyst and Reviewer. Analyst acknowledges message 2; a new service instance reports Analyst has 0 unread while Reviewer still has 2. Excluding message 1 produces visible IDs `[2]` while canonical IDs remain `[1, 2]`.

The example then deliberately breaks the compiled view. A canonical lens still returns message 2, `compile_chat` rebuilds the visible file, and Reviewer's cursor stays unchanged until an explicit acknowledgement. Final verification reports no structural issues. The demonstration is offline and uses a disposable temporary directory.

## Integrate a reader

```python
from pathlib import Path
from agent_chatroom_ledger.service import ChatroomService

service = ChatroomService(Path("./my-rooms"))
room = service.create_chat("Synthetic Review", participants=["Reviewer"])
room_id = room["state"]["chat_id"]
service.post_message(room_id, "Reviewer", "A synthetic observation.")
lens = service.render_chat_lens(room_id)
# Process or display lens["messages"] successfully before acknowledging.
service.mark_seen("Reviewer", Path("./reviewer.cursor.json"), room_id,
                  message_id=lens["last_message_id"])
```

The recipe creates local files. Keep one cursor file per independent consumer. Reading or rendering does not mark anything seen; advance a cursor only after your consumer has handled the intended range. The example acknowledges the latest canonical position intentionally, including excluded records; if that is unsuitable for your application, select the acknowledged ID explicitly.

## Follow the mechanism

| State | Responsibility and entry point |
| --- | --- |
| Canonical message records | [ChatroomStore](agent_chatroom_ledger/store.py) appends records and allocates message IDs under its room lock. `load_chat` reads these records. |
| Visible room file | `compile_chat` builds a projection from messages plus compile policy. It is replaceable. |
| Context selection | `exclude_messages`, `include_messages` and stand-ins change the compiled view; exclusion does not erase the original message. |
| Independent progress | [scanner](agent_chatroom_ledger/scanner.py) compares room state with [consumer cursors](agent_chatroom_ledger/cursors.py); `mark_seen` persists acknowledgement. |
| Application boundary | [ChatroomService](agent_chatroom_ledger/service.py) exposes the operations; your application supplies transport, scheduling and model execution. |

The [CLI reference](docs/REFERENCE.md) covers room creation, archive/restore, placement, message versions and verification. Administrative CLI operations default to a dry run and need `--apply` to write. Python service calls are direct operations; they are not implicitly dry runs.

## Boundaries and further work

Participant gating selects which rooms a consumer sees; it is not user authentication. Messages and cursors are plaintext. Use trusted callers and an access-controlled directory. A lock coordinates writers, but the room consists of several files; this is not a transactional database or a network replication protocol. A broken compiled view can be rebuilt only while canonical messages and state remain intact.

A useful next integration would adapt one real consumer to read a lens, process it, and acknowledge only on success. That adapter and live model connectors are not included or demonstrated. [Message Version Bundle Builder](https://github.com/CinvanaAI/message-version-bundle-builder) isolates the related numbered-context-view mechanism if you only need that part.

```sh
python -m pip install pytest
python -m pytest -q
```

Excluded historical host-connector tests remain explicitly skipped; backend checks and the runnable example use synthetic local data. [MIT license](LICENSE.md) · [Security boundary](SECURITY.md)
