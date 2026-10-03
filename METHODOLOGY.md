# Scope and curation method

## Coverage

This edition was researched on **2026-10-03**, covering the public ecosystem following TypeSafe AI's **2026-09-15** Jev launch. Two 2025 papers appear only in a clearly labeled historical-context subsection because they are cited in the community's prior-work discussion.

“Jev” means TypeSafe AI's decision model and resources directly discussing, evaluating, integrating, or independently implementing its decision-interface idea. Unrelated uses of the acronym, including Japanese encephalitis virus, are excluded. General AI papers are not included merely because they mention fast inference or System 1 thinking.

This is a curated directory, not an exhaustive census. Search indexing, login requirements, deleted posts, changing repositories, and incomplete release pages limit coverage. Larger community directories are linked for the long tail; their entire contents have not been imported or represented as independently verified.

## Discovery and source checks

- Start with the [official launch](https://typesafe.ai/blog/introducing-system-one-models-and-jev), [documentation index](https://docs.typesafe.ai/llms.txt), and [TypeSafe GitHub organization](https://github.com/typesafe-ai).
- Search combinations of `Jev`, `TypeSafe`, `System One`, `decision model`, `OpenJev`, `evaluation`, and named projects across web results, arXiv, GitHub, Hugging Face, Hacker News, and Reddit.
- Expand through references in the [early evidence audit](https://arxiv.org/abs/2609.32160), author articles, model cards, and community directories. The audit's 28-paper appendix provided discovery leads; the linked original paper records were then checked.
- Read original arXiv metadata and abstracts for paper descriptions. These entries are bibliographic summaries, not full-paper replication reviews. Where the currently served abstract differs from an indexed version, prefer the original page and avoid fragile headline numbers.
- Inspect original repositories and their README links for purpose, model availability, and links to checkpoints or data. Follow renamed repositories to the current canonical location.
- Check hosted integrations against the provider's documentation. Treat similarly named third-party “Jev” websites as independent unless official ownership is demonstrated.

Descriptions are original short summaries. External publications and software retain their own copyrights and licenses. Inclusion does not endorse a resource or validate its benchmark claims. No third-party code was installed or executed, and no model inference was needed to build this directory.

## Popularity

The Hacker News subsection is sorted by points among relevant candidates returned by the public [Algolia story search](https://hn.algolia.com/api/v1/search?query=jev&tags=story&hitsPerPage=50). The query is limited to 50 hits and is not a complete search of all submissions. Counts were retrieved on 2026-10-03; per-entry metrics, measurement dates, and source links are recorded in the [catalog](data/resources.json). Intermediate collection snapshots are kept locally.

Points and comments indicate attention, not technical merit. The list includes humorous demonstrations and criticism with explicit labels. Blog and Reddit entries are not numerically ranked against Hacker News; Reddit vote counts were not consistently available, so none were invented. HN submission dates refer to the submission, which may differ from the original article's publication date.

## Artifact and evidence labels

| Label | Meaning |
| --- | --- |
| Official | Published by TypeSafe AI. |
| Official open-source code | An official SDK or tool repository; does not imply open Jev weights. |
| Hosted integration | A documented access path through a provider; the underlying model remains hosted. |
| Open weights and code | An independent project publishes code and linked model weights; consult its licenses and model cards. |
| Open weights | A checkpoint is linked, without a claim that every training artifact is available. |
| Code available; weights pending | A pipeline is public, but the checked page still lists its trained weights as unreleased. |
| Discussion / Article | Commentary, author experiments, or debate, not necessarily peer-reviewed evidence. |
| Preprint | Public research on arXiv; no peer-review status is asserted. |
| Earlier preprint | Historical context predating Jev's release. |

Independent Jev-like implementations reproduce interface ideas or pursue related goals; they are not verified reconstructions of the proprietary Jev model. Distinguish valid output types from correct judgments, calibration from logical coherence, model performance from harness performance, and local timing from hosted API timing.

## Maintenance

`data/resources.json` is the catalog source of truth; `data/news.json` holds the selected news timeline. Run `python3 scripts/render.py` after editing either to regenerate `README.md` and `references.bib`. Entries have stable identifiers, category, status, a dated event and its type, source links, a topic icon, and a check date. The overview table is calculated from the catalog. The main README deliberately repeats some projects in discussion, implementation, and paper contexts; these represent different resource types rather than additional unique projects.

Check dates document source inspection, not a guarantee that every URL is reachable from every network. Access failures such as timeouts, rate limits, and bot challenges should be distinguished from confirmed missing pages. Automated reachability snapshots and intermediate verification records are kept locally and excluded from Git.

## Dates and news

Every catalog entry displays `[YYYY-MM-DD]` with an event label. `published` refers to a dated article or announcement; `submitted` refers to the first arXiv submission or the linked Hacker News submission. `repository_created` uses GitHub's UTC `created_at` metadata. It does **not** establish when a repository became public, when a model was trained, or when weights were released. `paper_submitted` dates a related paper rather than its model checkpoints. `cataloged` is the collection date used when the source's original date has not been verified.

The `date_source` field identifies the supporting page or API in the published catalog; intermediate timestamp excerpts are retained locally. News uses dated announcements, package release records, or original paper submissions. Laya's 2026-09-18 item is specifically the [PyPI 0.1.0 package release](https://pypi.org/project/laya/0.1.0/), verified against its [upload timestamps](https://pypi.org/pypi/laya/0.1.0/json); it is not a claim about the first checkpoint release. The timeline is selective and ordered newest first.

## Visual guide

The landscape illustrates selected ecosystem themes, not a technical dependency graph or an exhaustive chronology. The logo and landscape were created with the built-in image generation tool; artwork prompts and design notes are retained locally. Small SVG icons identify topics such as models, memory, vision, calibration, and security; they are independent directory artwork, not official project logos.
