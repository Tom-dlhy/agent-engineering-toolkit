# Python CLI and batch — safe side effects, reruns and recovery

**Read when:** implementing Python commands, scripts, ingestion,
batch jobs, filesystem changes or external process execution.

## Choose by lifetime and failure cost
One local data transform can remain a script with argparse and tests.
A repeatable production batch needs checkpointed progress, bounded
input/memory, idempotent updates, explicit error exit status and
partial-failure repair. Don't deploy a task broker just to parse one file.

## Atomic local write (illustrative)

~~~python
import json
import os
import tempfile
from pathlib import Path

def write_json_atomically(target: Path, value: dict[str, object]) -> None:
    data = json.dumps(value, ensure_ascii=False).encode("utf-8")
    fd, name = tempfile.mkstemp(dir=target.parent, prefix=".partial-")
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(name, target)
    finally:
        if os.path.exists(name):
            os.unlink(name)
~~~

Caller must authorize and constrain file path. This avoids partially
visible content on a compatible local filesystem, but doesn't solve
symlink attacks, multiwriter races, parent-directory durability or
object-storage replacement semantics. Use locks/ETags/DB transactions
when appropriate.

## Practical rules
- Validate encoding, timezone, schema and input size; stream large inputs.
- Persist checkpoints only after durable outcome, not after enqueue.
- Retries of state-changing calls need stable idempotency and reconciliation.
- Report error via nonzero exit status, not just a warning in stdout.
- Use subprocess argument lists, trusted executable paths, timeout
  and checked exit code, not concatenated untrusted shell strings.
- A dry-run is only safe if tests prove it causes no real mutations.
- Preserve audit metadata without logging credentials or customer records.

## Negative tests
Disk full, permissions, crash before replace, rerun same input,
bad UTF-8, oversized files, injected path, parallel writers and
downstream timeout after unknown commit.

Sources: https://docs.python.org/3/library/tempfile.html ,
https://docs.python.org/3/library/os.html#os.replace and
https://docs.python.org/3/library/argparse.html .
