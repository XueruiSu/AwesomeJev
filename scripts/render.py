"""Render the English directory and BibTeX from data/resources.json (stdlib only)."""

import collections
import html
import json
import pathlib
import re
from urllib.parse import urlsplit

ROOT = pathlib.Path(__file__).resolve().parents[1]
data = json.loads((ROOT / "data/resources.json").read_text())
resources = data["resources"]
news = json.loads((ROOT / "data/news.json").read_text())["events"]


def anchor(text):
    return re.sub(r"[^a-z0-9 -]", "", text.lower()).replace(" ", "-")


def github_stars(url):
    parsed = urlsplit(url)
    parts = parsed.path.strip("/").split("/")
    if parsed.hostname not in {"github.com", "www.github.com"} or len(parts) < 2:
        return ""
    owner, repo = parts[:2]
    repo = repo.removesuffix(".git")
    if not re.fullmatch(r"[A-Za-z0-9-]+", owner) or not re.fullmatch(r"[A-Za-z0-9_.-]+", repo):
        return ""
    repository = f"{owner}/{repo}"
    badge = f"https://img.shields.io/github/stars/{repository}?style=flat-square&label=%E2%98%85"
    return f" [![GitHub stars]({badge})](https://github.com/{repository})"


def link(label, url, include_stars=True):
    return f"[{label}]({url})" + (github_stars(url) if include_stars else "")


def icon(name, alt=""):
    return f'<img src="assets/icons/{name}.svg" width="22" height="22" alt="{html.escape(alt)}">'


def stamp(resource):
    if resource["date_kind"] in {"unknown", "cataloged"} or not resource["date"]:
        raise ValueError(f"{resource['id']}: research an event date, estimate, or dated availability bound before publishing")
    labels = {
        "published": "Published", "submitted": "Submitted",
        "repository_created": "Repository created", "updated": "Page updated",
        "paper_submitted": "Paper submitted",
    }
    if resource["date_kind"] in {"estimated", "available_by"}:
        if not resource.get("date_source") or not resource.get("date_note"):
            raise ValueError(f"{resource['id']}: inferred dates require a source and rationale")
        return f"**[{resource['date']}]**"
    label = labels[resource["date_kind"]]
    return f"**[{resource['date']}]** · {label}"


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
    '<p align="center"><img src="assets/awesomejev-logo.png" width="160" alt="AwesomeJev robot and decision-crystal logo"></p>',
    "",
    "# AwesomeJev",
    "",
    "![Jev ecosystem landscape: TypeSafe and System One origins; Laya, Kev, Jeff and Jeeves; tools and agents; evaluation and debate.](assets/jev-landscape.png)",
    "",
    "A curated, English-language directory of **TypeSafe AI’s Jev** and the emerging ecosystem of typed decision models: original releases, community discussions, open infrastructure, model weights, datasets, and research.",
    "",
    "**Start with the original announcement:** [Introducing System One Models & Jev — September 15, 2026](https://typesafe.ai/blog/introducing-system-one-models-and-jev).",
    "",
    "## Big News",
    "",
]
for event in sorted(news, key=lambda e: e["date"], reverse=True):
    note = f" {event['note']}" if event.get("note") else ""
    lines.append(f"- {icon(event['icon'])} **[{event['date']}]** {event['headline']} {link(event['label'], event['url'])}.{note}")
lines.extend([
    "",
    "Jev evaluates supplied state against typed questions and returns choices, scores, or yes/no probabilities. Hosted Jev is proprietary; public SDKs and independent open-weight alternatives are different artifacts. No official downloadable Jev weights or architecture paper were located in this review. Schema validity does not establish factual correctness, calibration on every distribution, or immunity to prompt injection. See the [official documentation](https://docs.typesafe.ai/introduction), [model limitations](https://docs.typesafe.ai/model-jaggedness/jev-1.13), and research below.",
    "",
    "[Machine-readable catalog](data/resources.json) · [Paper citations](references.bib) · [Curation methodology](METHODOLOGY.md) · [Contributing](CONTRIBUTING.md)",
    "",
    "| Explore | Entries | Subcategories | Coverage |",
    "| --- | ---: | ---: | --- |",
])
coverage = [
    ("rocket", "Original announcement, documentation, and first-party references"),
    ("chat", "Popular threads, technical articles, debates, and discovery directories"),
    ("chip", "SDKs, integrations, open models, runtimes, benchmarks, and applications"),
    ("book", f"{post_launch} post-launch preprints + {earlier} historical-context papers"),
]
for (section, categories), (symbol, description) in zip(sections.items(), coverage):
    count = sum(len(entries) for entries in categories.values())
    lines.append(f"| {icon(symbol)} [{section}](#{anchor(section)}) | **{count}** | {len(categories)} | {description} |")
lines.extend([
    f"| **Total** | **{len(resources)}** | **{sum(len(c) for c in sections.values())}** | Catalog entries; one project may appear in multiple resource types |",
    "",
    "## Hands-on tutorials",
    "",
    "**[2026-10-03]** [Jev beginner guide: typed decisions, support routing, and remote open-model experiments](tutorials/jev-hands-on/README.md). Includes a runnable official SDK example, offline policy/SDK tests, twelve synthetic tickets, and two measured Laya runs on one remote RTX 3090. See the [actual results and lessons](tutorials/jev-hands-on/RESULTS.md); official hosted Jev live results are pending API-key configuration.",
    "",
    "## Contents",
    "",
])
lines.append("- [Hands-on tutorials](#hands-on-tutorials)")
for section, categories in sections.items():
    lines.append(f"- [{section}](#{anchor(section)})")
    for category in categories:
        lines.append(f"  - [{category}](#{anchor(category)})")
lines.append("- [Citation](#citation)")

for section, categories in sections.items():
    lines.extend(["", f"## {section}", ""])
    if section.startswith("2."):
        lines.extend([
            "Hacker News threads are ordered by observed points within the retrieved candidates. Counts are a **2026-10-03 snapshot**, not live metrics or a quality ranking. The [catalog](data/resources.json) records per-entry attention metrics and sources; see the [methodology](METHODOLOGY.md#popularity) for the collection method. Blogs and Reddit threads are selected for their relevance; no cross-platform popularity claim is made.",
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
                lines.append(f"| {icon(r['icon'])} **{r['title']}**<br>{stamp(r)}<br>{refs} | {a['points']:,} / {a['comments']:,} | {r['description']} |")
        else:
            for r in entries:
                primary, *rest = r["links"]
                refs = " · ".join(link(x["label"], x["url"]) for x in rest)
                suffix = f" {refs}." if refs else ""
                title = f"**{link(r['title'], primary['url'], include_stars=False)}**{github_stars(primary['url'])}"
                lines.append(f"- {icon(r['icon'])} {stamp(r)} · {title} — `{r['status']}`. {r['description']}{suffix}")
        lines.append("")

lines.extend([
    "## Citation",
    "",
    "> [!NOTE]",
    "> 📚 If you find this resource useful, please cite and [⭐ star the repo](https://github.com/XueruiSu/AwesomeJev):",
    "",
    "```bibtex",
    "@misc{su2026awesomejev,",
    "  title        = {{AwesomeJev: A Curated Collection of Jev Resources}},",
    "  author       = {Xuerui Su},",
    "  year         = {2026},",
    "  howpublished = {GitHub repository},",
    "  url          = {https://github.com/XueruiSu/AwesomeJev}",
    "}",
    "```",
    "",
])

(ROOT / "README.md").write_text("\n".join(lines).rstrip() + "\n")

bib = ["% Catalog updated on " + data["last_updated"] + "; source-check dates are recorded per entry in data/resources.json.", ""]
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
