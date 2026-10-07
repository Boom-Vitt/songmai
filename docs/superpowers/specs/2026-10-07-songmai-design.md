# Songmai design

## Outcome

A public MIT Thai-first handoff kit: a reusable agent Skill, editable Markdown template, create/resume prompts, a runnable Claude → Codex example, and a read-only file-reference checker. Users move work between agents/chats using explicit files instead of explaining it again. This is a file workflow, not automatic transfer of model memory or credentials.

## Interface

`python3 skills/songmai/scripts/check_handoff.py HANDOFF.md --root WORKSPACE` uses Python 3.9+ stdlib; root defaults to the handoff file's parent. Exit 0 means all declared references are existing files inside root, 1 means a handoff/file validation failure, 2 means invalid CLI usage. It prints paths and status, never file contents, and writes nothing.

References appear under the exact level-two heading `## ไฟล์อ้างอิง`, as one `- `backtick-quoted relative/path` — description` per line, until the next level-two heading. Paths use `/`, can contain Thai and spaces, and must be files. Reject missing/duplicate sections, empty/malformed sections, absolute/drive paths, parent traversal and symlinks outside root. Ignore headings inside fenced code. `- ไม่มีไฟล์อ้างอิง` explicitly represents a handoff with no files; do not silently accept an empty section. Do not mix that marker with files. Paths do not contain line/anchor suffixes; line details go in the description. Missing/unreadable/non-UTF-8 input must produce a controlled failure.

## Handoff content

Template records goal and completion criteria, scope/authorization, verified current state and local edits, completed work, decisions, reference files, exact checks with observed results, next actions and blockers. The creating agent reads actual files/git/check output, labels UNKNOWN/NOT_RUN, excludes secrets and preserves important exact names/URLs. The receiving agent checks files and workspace state, distinguishes old evidence from fresh results, and continues authorized work without redoing completed tasks. It asks only for information essential to correctness.

## Example and evidence

A tiny Python landing-page renderer has baseline and completed versions. A sample handoff describes the baseline with a real failing check, requires escaping text for HTML, and gives exact next commands. A deterministic resume exercise uses the same instructions to select the provided completed file and shows the check going red to green in an isolated temporary workspace. Clearly label it a simulated Claude → Codex handoff, not a live provider benchmark.

## Acceptance

Readme quick start works from an extracted ZIP, including a path with spaces. CLI behavior is tested with real temp files/subprocesses; missing/malformed references and outside-root links fail. Example baseline fails its security check and solution passes. Local links and Skill YAML frontmatter are inspected. Public GitHub main and CI on macOS/Ubuntu/Windows are verified, along with ZIP download contents. Publication is authorized by the user's request to make the selected giveaway repository; no social posts/messages are authorized.
