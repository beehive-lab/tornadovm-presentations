# Contributing

Thanks for adding a TornadoVM presentation. This guide describes where files go and how to name them.

## 1. Choose the folder path

Use the layout:

```text
slides/<year>/<venue>/<event-or-talk-title>/
```

- **Year**: four digits, e.g. `2024`, `2025`, `2026`.
- **Venue**: a lowercase, stable identifier reused across years, e.g. `hipeac`, `ppopp`, `vee`, `supercomputing`. Register new venues in [`metadata/venues.yml`](metadata/venues.yml).
- **Event / talk title**: lowercase and hyphenated, descriptive but concise, e.g. `tornadovm-dynamic-reconfiguration`.

Avoid spaces, special characters, very long names, and ambiguous names such as `talk1`, `slides-final`, or `presentation`.

### Repeated venues across years

Reuse the same venue key every year so presentations can be tracked over time:

```text
slides/2023/hipeac/...
slides/2024/hipeac/...
slides/2025/hipeac/...
```

## 2. Add the files

Each event folder must contain at least:

```text
README.md
slides.pdf
```

`slides.pdf` is the main public artifact. Optional files:

```text
slides.pptx | slides.key | slides.odp   # editable source
abstract.md
citation.bib
assets/
├── figures/
└── images/
```

Use [`templates/event-README-template.md`](templates/event-README-template.md) for the event `README.md`.

## 3. Update metadata

Add an entry to [`metadata/events.yml`](metadata/events.yml) (see [`templates/metadata-template.yml`](templates/metadata-template.yml)). If the venue is new, add it to [`metadata/venues.yml`](metadata/venues.yml).

## 4. Update the index

Add a row to the appropriate year table in the root [`README.md`](README.md).

## Naming rules summary

- Years: `2024`, `2025`, `2026`
- Venues: lowercase stable identifiers (`hipeac`, `ppopp`, `vee`, `supercomputing`)
- Event folders: lowercase, hyphenated (`tornadovm-dynamic-reconfiguration`)
- Main PDF: `slides.pdf`
- Editable source: `slides.pptx`, `slides.key`, or `slides.odp`
- Event description: `README.md`
- Abstract: `abstract.md`
- BibTeX citation: `citation.bib`
