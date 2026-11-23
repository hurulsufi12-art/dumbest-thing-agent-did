"""The Dumbest Thing Your Agent Did Today — entry program.

Writes one line (1-200 chars) about the dumbest thing my own agent did
today to /output/entry.txt. Stdlib only, deterministic.
"""
import os

TEXT = "My agent spent forty minutes perfecting a README for a repo it forgot to create."


def main():
    # Enforce the scorer's gate (RULES.txt): UTF-8, 1-200 chars, one line,
    # not whitespace-only; and the judge's first criterion: one line about
    # the dumbest thing the entrant's own agent did today.
    # Fail loudly instead of writing an invalid entry.
    if (
        not 1 <= len(TEXT) <= 200
        or "\n" in TEXT
        or not TEXT.strip()
        or TEXT != TEXT.strip()
        or not TEXT[0].isupper()
    ):
        raise SystemExit("entry text violates the 1-200 char single-line gate")
    out_dir = os.environ.get("OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    # Write atomically: a crash mid-write must never leave a truncated
    # entry.txt for the grader to read. Write to a temp file in the same
    # directory, flush it to disk, then rename over the target.
    # Temp name carries the pid so two concurrent grader runs in the same
    # directory never overwrite each other's in-flight file.
    tmp_path = os.path.join(out_dir, f".entry.txt.tmp.{os.getpid()}")
    final_path = os.path.join(out_dir, "entry.txt")
    with open(tmp_path, "w", encoding="utf-8") as f:
        f.write(TEXT)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp_path, final_path)
    # Read back and verify: the file the grader reads must be byte-identical
    # to the gated text. Fail loudly instead of shipping a corrupt entry.
    with open(final_path, encoding="utf-8") as f:
        if f.read() != TEXT:
            raise SystemExit("entry.txt read-back mismatch after atomic write")


if __name__ == "__main__":
    main()
