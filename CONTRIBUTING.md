# Contributing to AwesomeJev

Additions, corrections, updated release links, and broken-link reports are welcome.

1. Check `data/resources.json` for an existing entry. Prefer a project's canonical URL over mirrors and reposts.
2. Add the resource under the appropriate section and category. Preserve the order: origins → community → infrastructure/models → research.
3. Write a concise English description explaining the actual connection to Jev. Include original blog, discussion, repository, model, dataset, and paper links where available.
4. Distinguish official resources, independent implementations, hosted integrations, open weights, and announced but unreleased artifacts. Do not call public code an open-weight release unless the weights are available.
5. For a paper, verify its full title, authors, first submission date, and arXiv ID against the original record. Use `Preprint` unless a publication venue has been verified. Do not infer a venue from a repository badge.
6. For reported performance, preserve the test conditions and attribution. Avoid unsupported claims such as “equivalent to Jev” or “guaranteed calibrated.”
7. Set `checked_on` to the date you checked the original source. Supply `date`, `date_kind`, and `date_source`. Use `published`, `submitted`, `repository_created`, or `paper_submitted` only when the source supports that event. If the original date is unknown, use the collection date with `date_kind: "cataloged"`; never invent a release date.
8. Run `python3 scripts/render.py` and include the updated README and BibTeX alongside the JSON change.

Choose an existing topic `icon` from `assets/icons/`, or add an original SVG pictogram in the same style. Keep filenames stable. Add significant dated announcements to `data/news.json`, including a source link and a precise description of the event. The renderer updates the overview counts automatically; do not edit those counts by hand.

Keep intermediate research snapshots, link-check reports, date-evidence extracts, artwork prompts, and design/change notes local. Respect `.gitignore` and never force-add these working files. Publish the catalog (`data/resources.json`), news (`data/news.json`), generated documentation, citations, renderer, and final visual assets. Public documentation must not link to ignored files.

The record `id` must be unique and stable. All `links` must have a descriptive `label` and an absolute HTTP(S) `url`. An `attention` object is optional and must identify the platform, measurement date, and source. Do not mix live counts with historical snapshots.

Open a pull request explaining what changed and which original sources support it. For small corrections, an issue with the exact URL and proposed replacement is sufficient. Please do not include credentials, private communications, copied full articles, or model files in a submission.
