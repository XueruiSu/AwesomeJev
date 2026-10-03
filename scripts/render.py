"""Render the English directory and BibTeX from data/resources.json (stdlib only)."""

import collections
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[1]
data = json.loads((ROOT / "data/resources.json").read_text())
resources = data["resources"]


def anchor(text):
    return re.sub(r"[^a-z0-9 -]", "", text.lower()).replace(" ", "-")


def link(label, url):
    return f"[{label}]({url})"


sections = collections.defaultdict(lambda: collections.defaultdict(list))
for resource in resources:
    sections[resource["section"]][resource["category"]].append(resource)

papers = [r for r in resources if "arxiv_id" in r]
post_launch = sum(r["date"] >= data["scope_start"] for r in papers)
earlier = len(papers) - post_launch
for section, categories in sections.items():
    if section.startswith("4."):
        for entries in categories.values():
            entries.sort(key=lambda r: (r["date"], r["arxiv_id"]))

lines = [
    "# AwesomeJev",
    "",
    "A curated, English-language directory of **TypeSafe AI’s Jev** and the emerging ecosystem of typed decision models: original releases, community discussions, open infrastructure, model weights, datasets, and research.",
    "",
    "**Start with the original announcement:** [Introducing System One Models & Jev — September 15, 2026](https://typesafe.ai/blog/introducing-system-one-models-and-jev).",
    "",
    f"**Last researched: {data['last_updated']}.** {len(resources)} catalog entries, including {post_launch} post-launch research preprints and {earlier} earlier papers cited in community debates. This is a source-backed, best-effort collection, not a claim to have indexed the entire internet.",
    "",
    "Jev evaluates supplied state against typed questions and returns choices, scores, or yes/no probabilities. Hosted Jev is proprietary; public SDKs and independent open-weight alternatives are different artifacts. No official downloadable Jev weights or architecture paper were located in this review. Schema validity does not establish factual correctness, calibration on every distribution, or immunity to prompt injection. See the [official documentation](https://docs.typesafe.ai/introduction), [model limitations](https://docs.typesafe.ai/model-jaggedness/jev-1.13), and research below.",
    "",
    "[Machine-readable catalog](data/resources.json) · [Paper citations](references.bib) · [Curation methodology](METHODOLOGY.md) · [Contributing](CONTRIBUTING.md)",
    "",
    "## Contents",
    "",
]
for section, categories in sections.items():
    lines.append(f"- [{section}](#{anchor(section)})")
    for category in categories:
        lines.append(f"  - [{category}](#{anchor(category)})")

for section, categories in sections.items():
    lines.extend(["", f"## {section}", ""])
    if section.startswith("2."):
        lines.extend([
            "Hacker News threads are ordered by observed points within the retrieved candidates. Counts are a **2026-10-03 snapshot**, not live metrics or a quality ranking. The [snapshot](data/attention-snapshot.json) records the source and method. Blogs and Reddit threads are selected for their relevance; no cross-platform popularity claim is made.",
            "",
        ])
    if section.startswith("3."):
        lines.extend([
            "Official clients, hosted access, independent weights, and local implementations are labeled separately. A compatible API does not imply the same architecture, training data, calibration, or capability as TypeSafe’s Jev. Model and data licenses remain those of their respective publishers.",
            "",
        ])
    if section.startswith("4."):
        lines.extend([
            "Grouped by research topic; chronological within each group. Dates are first arXiv submission dates, while descriptions reflect the version accessed during this review. **Preprint** does not imply peer review. Summaries describe the authors’ work, not independently reproduced findings. Code/model links are included where located; absence of a link means it was not located, not that no artifact exists.",
            "",
        ])
    for category, entries in categories.items():
        lines.extend([f"### {category}", ""])
        if category == "Popular Hacker News discussions":
            lines.extend(["| Discussion | Points / comments | What it covers |", "| --- | ---: | --- |"])
            for r in entries:
                a = r["attention"]
                refs = " · ".join(link(x["label"], x["url"]) for x in r["links"])
                lines.append(f"| **{r['title']}**<br>{refs} | {a['points']:,} / {a['comments']:,} | {r['description']} |")
        else:
            for r in entries:
                primary, *rest = r["links"]
                refs = " · ".join(link(x["label"], x["url"]) for x in rest)
                date = f" · {r['date']}" if r["date"] else ""
                suffix = f" {refs}." if refs else ""
                lines.append(f"- **{link(r['title'], primary['url'])}** — `{r['status']}{date}`. {r['description']}{suffix}")
        lines.append("")

(ROOT / "README.md").write_text("\n".join(lines).rstrip() + "\n")

bib = ["% Metadata checked against original arXiv records on " + data["last_updated"] + ".", ""]
for r in resources:
    if "arxiv_id" not in r:
        continue
    bib.extend([
        "@misc{arxiv" + r["arxiv_id"].replace(".", "") + ",",
        "  title = {{" + r["title"].replace("&", r"\&") + "}},",
        "  author = {" + " and ".join(r["authors"]) + "},",
        "  year = {" + r["date"][:4] + "},",
        "  eprint = {" + r["arxiv_id"] + "},",
        "  archivePrefix = {arXiv},",
        "  url = {https://arxiv.org/abs/" + r["arxiv_id"] + "}",
        "}",
        "",
    ])
(ROOT / "references.bib").write_text("\n".join(bib))
print(f"Rendered {len(resources)} entries and {sum('arxiv_id' in r for r in resources)} citations.")
