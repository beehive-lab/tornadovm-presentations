# Contributing

Thanks for adding a TornadoVM presentation. This guide describes where files go and how to name them.

## 1. Choose the path

Place the slide PDF directly under the year and venue:

```text
slides/<year>/<venue>/<talk-title>.pdf
```

- **Year**: four digits, e.g. `2024`, `2025`, `2026`.
- **Venue**: a lowercase, stable identifier reused across years, e.g. `hipeac`, `ppopp`, `vee`, `jprime`.
- **Talk title**: lowercase and hyphenated, descriptive but concise. Prefixing with the year and venue keeps files self-describing, e.g. `jprime2026-tornadovm-gpullama3.pdf`.

Avoid spaces, special characters, very long names, and ambiguous names such as `talk1`, `slides-final`, or `presentation`.

### Repeated venues across years

Reuse the same venue key every year so presentations can be tracked over time:

```text
slides/2023/hipeac/...
slides/2024/hipeac/...
slides/2025/hipeac/...
```

Multiple talks at the same venue in the same year just live side by side as separate PDFs.

## 2. Add the file

`slides.pdf` is the main public artifact — name it descriptively as above and drop it directly into the venue folder. That's the only required file.

## 3. Update metadata

Add an entry to [`metadata/events.yml`](metadata/events.yml) (see [`templates/metadata-template.yml`](templates/metadata-template.yml)). The `pdf` field points at the file you just added.

## 4. Update the index

Add a row to the appropriate year table in the root [`README.md`](README.md).

## Naming rules summary

- Years: `2024`, `2025`, `2026`
- Venues: lowercase stable identifiers (`hipeac`, `ppopp`, `vee`, `jprime`)
- Slide PDF: lowercase, hyphenated, descriptive (`jprime2026-tornadovm-gpullama3.pdf`)
