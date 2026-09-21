# Public project site

Purpose: make the INR edition, historical findings and reproducible data understandable and discoverable from a public GitHub Pages site.

- Three static French pages: presentation with evidence-backed conclusions; complete benchmark tables; methodology and provenance.
- White (#ffffff), deep blue (#173d63), blue (#176b87), pale blue (#e9f3f8), amber (#8a5014), dark text (#182c3a). System Avenir/Segoe typography; left-aligned prose, wide plots and responsive tables. Conclusions lead; historical scope stays adjacent.
- Use existing generated CSV data to fill findings and tables, with no hand-maintained duplicate numbers. Small progressive JavaScript filters enhance results; all rows exist in HTML without JavaScript.
- Build with standard-library Python. No framework, remote font, tracker or mandatory browser dependency.
- Canonical metadata, descriptive titles, sitemap, Open Graph, SoftwareSourceCode and Dataset JSON-LD reflecting visible source attribution and download links. No unsupported promise of indexing or AI citations.
- GitHub Pages Actions deployment after test success. Test generated links, metadata/data consistency and no-JS content, then browser-check desktop/mobile interaction and verify the public URL after deployment.
