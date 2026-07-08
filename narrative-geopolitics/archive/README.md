# Narrative Geopolitics Archive

`archive/` owns imported source truth for Narrative Geopolitics.

Sources are stored centrally because one transcript or source capture may involve more than one voice. Voice records should link into this archive instead of duplicating source text inside each voice folder.

## Boundary

```text
archive/ = source truth
voices/  = voice continuity and routing
work/    = daily synthesis
public/  = published briefs
```

## Layout

```text
archive/
|-- README.md
|-- source-manifest.json
`-- sources/
    `-- YYYY-MM-DD/
        `-- source-*.md
```

## Manifest

[source-manifest.json](source-manifest.json) records each imported source with its local archive path, upstream source path, source class, modality, voice slugs, host slug when present, and import status.

Use [voice-routing-audit.md](voice-routing-audit.md) when deciding whether a shared source should carry more than one `voice_slug`.

## Import Rule

Preserve source contents as imported. Add interpretation, routing, and synthesis in voice records, work runs, and public briefs.
