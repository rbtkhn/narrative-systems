# narrative-systems

A small research workbench for turning narrative-system ideas into runnable, testable structures.

This repository starts with a minimal Python package, a few working concepts, and space for notes. The goal is to keep theory and code close enough that terms can be tested, revised, and reused without needing a full application too early.

## Layout

```text
.
├── docs/                  Concept notes and working vocabulary
├── examples/              Small runnable demonstrations
├── src/narrative_systems/ Python package code
└── tests/                 Focused tests for the package surface
```

## Development

Create a local environment, install the package with test tooling, then run the checks:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[test]"
python -m pytest
python examples/basic_system.py
```

For a plain import check:

```powershell
python -c "import narrative_systems; print(narrative_systems.__version__)"
```

## First Concepts

The initial model is intentionally small:

- `NarrativeUnit` names a unit of meaning or event.
- `NarrativeRelation` links two units with a typed relationship.
- `NarrativeSystem` collects units and relations and can summarize its contents.

These names are working handles, not final theory. They give the repo enough structure to grow by experiment.

## First Research Target

The first narrative system under study is [`rbtkhn/predictive-history`](https://github.com/rbtkhn/predictive-history), treated as a public namespace catalog and source-lattice reading system. See [docs/research-targets/predictive-history.md](docs/research-targets/predictive-history.md).
