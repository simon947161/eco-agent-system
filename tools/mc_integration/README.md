# MC-INTEGRATION-001 minimal adapter

This adapter proves one bounded path only:

```text
GitHub Issue #126 -> KITTY invocation identity -> ephemeral read-only Codex CLI
  -> durable local receipt -> GitHub Issue comment
```

It reuses the installed Codex CLI and GitHub CLI connection. It does not add a
service, scheduler, provider, public listener, secret store, push, merge,
deployment, or Council integration.

The checked-in policy is intentionally narrow: only
`simon947161/eco-agent-system#126` is accepted. The KITTY-side host adapter
reads `README.md` and the current Git HEAD, hashes the file, then supplies only
that bounded evidence to Codex. Codex is instructed not to invoke a shell or
tools. This avoids weakening the sandbox when Windows cannot launch a read-only
sandbox child. Results, checks and exact failures are saved under the
caller-selected evidence directory.
The default model is the installed CLI's advertised API-capable
`codex-auto-review`; callers may supply `--model` only when another model is
confirmed available on that CLI account.

Example (host paths are supplied by the operator/runtime, not stored here):

```powershell
node tools/mc_integration/mc-integration-runner.mjs `
  --workspace <isolated-eco-agent-system-worktree> `
  --evidence-dir <local-private-evidence-directory> `
  --writeback
```

The command is suitable for the existing KITTY/Mission Control task manager to
invoke after its normal authorization decision. It does not widen KITTY's
standing authorization.
