# Narrative Geopolitics Archive

`archive/` owns imported source truth for Narrative Geopolitics.

Sources are stored centrally because one transcript or source capture may involve more than one voice. Voice records should link into this archive instead of duplicating source text inside each voice folder.

## Boundary

```text
archive/ = source truth
voices/  = voice continuity and routing
channels/ = host, show, and channel conditioning
work/    = daily synthesis
public/  = published briefs
```

## Layout

```text
archive/
|-- README.md
|-- source-manifest.json
|-- voice-routing-audit.md
`-- sources/
    `-- YYYY-MM-DD/
        `-- source-*.md
```

## Manifest

[source-manifest.json](source-manifest.json) records each imported source with its local archive path, upstream source path, source class, modality, voice slugs, host slug when present, and import status.

Use `voice_slugs` for whole-source-person continuity. Use `host_slug` as the v1 routing key into [../channels/](../channels/README.md).

Use [voice-routing-audit.md](voice-routing-audit.md) when deciding whether a shared source should carry more than one `voice_slug`.

## Import Rule

Preserve source contents as imported. Add interpretation, routing, and synthesis in voice records, work runs, and public briefs.

## Phased Pape Parity

Pape has full-source parity in this archive: 75 imported sources routed through one complete voice record.

Other core voices can reach first-slice parity before full-source parity. First-slice parity means the voice has imported source evidence, manifest coverage, complete local routing for that slice, retrieval lenses, and channel-aware pressure separation. It does not mean the full upstream Statecraft corpus has been copied yet.
