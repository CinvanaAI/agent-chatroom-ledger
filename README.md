# Agent Chatroom Ledger

Let several readers share a room without sharing one unread cursor.

Maintain a durable coordination room whose participants and independent consumers can resume reading after restart.

## See it work

**Input:** Two synthetic messages, read independently by Analyst and Reviewer.

**Result:** After restart: Analyst has 0 unread, Reviewer has 2; excluding message 1 leaves canonical IDs [1, 2] and visible ID [2].

[Read the captured output](examples/result.txt) | [Inspect the example](examples/walkthrough.py)

Python 3.11 or newer. From the repository root:

```sh
python -m pip install -e .
python -m examples.walkthrough
```

The example uses synthetic material and runs offline. The captured output comes from executing this example, not a hand-written mockup.

## How it works

Canonical message records, compiled views, and consumer cursors have separate lifetimes. The walkthrough creates two participants, posts two messages, advances one cursor, reconstructs the service, and excludes one message from the visible view while keeping both canonical records.

Implementation: [agent_chatroom_ledger/service.py](agent_chatroom_ledger/service.py), [agent_chatroom_ledger/store.py](agent_chatroom_ledger/store.py), [agent_chatroom_ledger/cli.py](agent_chatroom_ledger/cli.py).

## Limits

This is the durable room and CLI backend. It has no live model or host-process connector. Message bodies are stored locally in plaintext; compiled-view exclusion is not deletion.

[Reference and CLI details](docs/REFERENCE.md) | [Origin](ORIGIN.md) | [MIT license](LICENSE.md)
