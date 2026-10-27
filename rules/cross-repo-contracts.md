# Cross-repo contracts

Applies when two or more repos share a stable interface (encoding, protocol, schema, or ABI).

## Contract-first discipline

A **shared contract** is any interface both sides compile against or any data format both sides read/write:

- Card/token encoding conventions
- Public API headers
- Tensor layout + version tag
- Label schema (field names, value ranges)
- Wire format
- Version headers

**Rule:** a contract change lands in the *providing* repo first, bumps the version, and is recorded in the contract doc. The *consuming* repo pins a version and upgrades deliberately. Never edit both sides of a contract in the same uncoordinated commit.

## Version bump policy

`MAJOR` bump = breaking change (encoding reorder, field removal, renamed type, tensor shape change). `MINOR` bump = backward-compatible addition. Record every bump in the providing repo's version-pin doc and update any cross-repo round-trip fixtures.

## Cross-repo change checklist

Before landing a contract change:

1. Update the providing repo and bump version.
2. Update the version-pin doc.
3. Update any cross-repo round-trip fixtures (committed fixtures in both repos; CI on each side runs its own half).
4. Open a corresponding update task in the consuming repo before closing the change.
5. Tag the consuming-repo task with the providing-repo version number so it's traceable.

Import this rule from any project's `CLAUDE.md`:

```
@../devkit/rules/cross-repo-contracts.md
```
