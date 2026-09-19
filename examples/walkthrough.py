"""Two independent readers resume after restart while raw messages survive exclusion."""
import json
import tempfile
from pathlib import Path
from agent_chatroom_ledger.service import ChatroomService
from agent_chatroom_ledger.json_io import load_json

with tempfile.TemporaryDirectory(prefix="chatroom-example-") as temporary:
    root = Path(temporary)
    service = ChatroomService(root / "rooms")
    chat = service.create_chat("Synthetic Review", participants=["Analyst", "Reviewer"])
    ref = chat["state"]["chat_id"]
    service.post_message(ref, "Analyst", "Synthetic observation: 18 checks passed.")
    service.post_message(ref, "Reviewer", "Synthetic review: inspect the two failures.")
    def unread(service, name):
        return sum(item.unread_count for item in service.scan_unread(name, root / (name + ".cursor.json")))
    before = {name: unread(service, name) for name in ("Analyst", "Reviewer")}
    service.mark_seen("Analyst", root / "Analyst.cursor.json", ref, message_id=2)
    service = ChatroomService(root / "rooms")
    after = {name: unread(service, name) for name in ("Analyst", "Reviewer")}
    service.exclude_messages(ref, [1])
    loaded = service.load_chat(ref)
    visible = load_json(loaded["visible_path"])
    assert before == {"Analyst": 2, "Reviewer": 2}
    assert after == {"Analyst": 0, "Reviewer": 2}
    verification = service.verify()
    assert verification["ok"]
    print(json.dumps({"unread_before": before, "unread_after_restart": after, "canonical_ids": [m["message_id"] for m in loaded["messages"]], "visible_ids_after_exclusion": [m["message_id"] for m in visible["messages"]], "verification": {key: verification[key] for key in ("ok", "error_count", "issues")}}, indent=2))
