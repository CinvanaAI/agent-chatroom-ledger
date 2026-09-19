# Security and privacy

- Room roots are operator-selected local directories.
- Visible and hidden room paths are resolved by the backend; callers should still use a dedicated root.
- Operations that reorganize rooms or messages are dry-run-first.
- Locks prevent ordinary concurrent duplicate IDs; stale-lock override is an explicit operator action.
- Messages, versions, and operation logs can contain sensitive text and are not encrypted.
- No private source rooms, model credentials, process connectors, or live participant state are included.

This is application-level durability and governance, not an operating-system sandbox or access-control system.
