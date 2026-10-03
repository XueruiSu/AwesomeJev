# AwesomeJev

A curated, English-language directory of **TypeSafe AI’s Jev** and the emerging ecosystem of typed decision models: original releases, community discussions, open infrastructure, model weights, datasets, and research.

**Start with the original announcement:** [Introducing System One Models & Jev — September 15, 2026](https://typesafe.ai/blog/introducing-system-one-models-and-jev).

**Last researched: 2026-10-03.** 127 catalog entries, including 34 post-launch research preprints and 2 earlier papers cited in community debates. This is a source-backed, best-effort collection, not a claim to have indexed the entire internet.

Jev evaluates supplied state against typed questions and returns choices, scores, or yes/no probabilities. Hosted Jev is proprietary; public SDKs and independent open-weight alternatives are different artifacts. No official downloadable Jev weights or architecture paper were located in this review. Schema validity does not establish factual correctness, calibration on every distribution, or immunity to prompt injection. See the [official documentation](https://docs.typesafe.ai/introduction), [model limitations](https://docs.typesafe.ai/model-jaggedness/jev-1.13), and research below.

[Machine-readable catalog](data/resources.json) · [Paper citations](references.bib) · [Curation methodology](METHODOLOGY.md) · [Contributing](CONTRIBUTING.md)

## Contents

- [1. Origins and official resources](#1-origins-and-official-resources)
  - [Launch and first-party references](#launch-and-first-party-references)
- [2. Community discussion and writing](#2-community-discussion-and-writing)
  - [Popular Hacker News discussions](#popular-hacker-news-discussions)
  - [Technical blogs and tutorials](#technical-blogs-and-tutorials)
  - [Reddit debates](#reddit-debates)
  - [Discovery directories](#discovery-directories)
- [3. Infrastructure, models, and applications](#3-infrastructure-models-and-applications)
  - [Official SDKs and tools](#official-sdks-and-tools)
  - [Hosted access and framework guides](#hosted-access-and-framework-guides)
  - [Browser and agent infrastructure](#browser-and-agent-infrastructure)
  - [Language clients and data systems](#language-clients-and-data-systems)
  - [Open-weight decision models](#open-weight-decision-models)
  - [Training pipelines and announced releases](#training-pipelines-and-announced-releases)
  - [Local runtimes and alternative implementations](#local-runtimes-and-alternative-implementations)
  - [Benchmarks, calibration, and datasets](#benchmarks-calibration-and-datasets)
  - [Examples, games, and learning projects](#examples-games-and-learning-projects)
- [4. Research papers](#4-research-papers)
  - [Surveys and broad evaluations](#surveys-and-broad-evaluations)
  - [Judging, calibration, and reliability](#judging-calibration-and-reliability)
  - [Robustness and security](#robustness-and-security)
  - [Agent memory, routing, and control](#agent-memory-routing-and-control)
  - [Open and alternative decision-model methods](#open-and-alternative-decision-model-methods)
  - [Networking and edge systems](#networking-and-edge-systems)
  - [Domain applications and multilingual models](#domain-applications-and-multilingual-models)
  - [Historical context cited in community debate](#historical-context-cited-in-community-debate)

## 1. Origins and official resources

### Launch and first-party references

- **[Introducing System One Models & Jev](https://typesafe.ai/blog/introducing-system-one-models-and-jev)** — `Official · 2026-09-15`. Diogo Almeida introduces Jev, the System One framing, RLCD, launch demonstrations, and the qualifications behind the reported performance gains. The starting point for this collection.
- **[TypeSafe manifesto](https://typesafe.ai/manifesto)** — `Official`. The company’s argument for models designed to make decisions inside software.
- **[The Bitterest Lesson](https://typesafe.ai/blog/bitterest-lesson)** — `Official`. Founder’s research perspective on the objectives and data used to train useful models. Background to the Jev launch.
- **[AI: too good to be true, too bad to be useful](https://typesafe.ai/blog/ai-too-good-to-be-true-too-bad-to-be-useful-typesafe-ai)** — `Official`. TypeSafe’s argument about the gap between conversational ability and dependable automation.
- **[Introduction and quick start](https://docs.typesafe.ai/introduction)** — `Official`. The official entry point for sending state and typed questions to Jev.
- **[Choice, Score, and Noul](https://docs.typesafe.ai/primitives)** — `Official`. Definitions of the three output primitives, including probability distributions and answer shapes.
- **[Confidence](https://docs.typesafe.ai/confidence)** — `Official`. How TypeSafe distinguishes answer probability from confidence and uses them in workflows.
- **[Model reference](https://docs.typesafe.ai/models)** — `Official`. Version identifiers, supported inputs, limits, and current service specifications.
- **[Jev 1.13 jaggedness](https://docs.typesafe.ai/model-jaggedness/jev-1.13)** — `Official`. First-party documentation of uneven capabilities and known weak spots. Essential context for evaluating launch claims.
- **[Patterns and cookbooks](https://docs.typesafe.ai/cookbooks)** — `Official`. Implementation guides for routing, scoring, fan-out, classification, search, and other bounded decisions.
- **[Workflow evaluations](https://evals.typesafe.ai/)** — `Official`. Vendor-run workflow comparisons, examples, and methodology; reference-model agreement is not the same as human ground truth.
- **[Documentation index](https://docs.typesafe.ai/llms.txt)** — `Official`. Machine-readable index of official documentation for deeper exploration.


## 2. Community discussion and writing

Hacker News threads are ordered by observed points within the retrieved candidates. Counts are a **2026-10-03 snapshot**, not live metrics or a quality ranking. The [snapshot](data/attention-snapshot.json) records the source and method. Blogs and Reddit threads are selected for their relevance; no cross-platform popularity claim is made.

### Popular Hacker News discussions

| Discussion | Points / comments | What it covers |
| --- | ---: | --- |
| **Introducing System One Models and Jev**<br>[Discussion](https://news.ycombinator.com/item?id=49717558) · [Original](https://typesafe.ai/blog/introducing-system-one-models-and-jev) | 1,989 / 520 | Launch discussion with founder participation, questions about the API, architecture disclosure, calibration, and evaluation. |
| **Jev in 25 Lines of Python**<br>[Discussion](https://news.ycombinator.com/item?id=49812769) · [Original](https://www.nobodywho.ai/posts/jev-in-25-lines/) | 691 / 212 | A deliberately minimal, explicitly satirical local implementation using option-token probabilities; the discussion probes what this does and does not reproduce. |
| **Ollaya – Ollama for open-source, Jev-style decision models**<br>[Discussion](https://news.ycombinator.com/item?id=49848269) · [Original](https://ollaya.dev/) | 617 / 145 | Discussion of a local runtime for open decision models and compatibility with the TypeSafe interface. |
| **Jeff – Jev-compatible 0.8B decision models, trained at home, ~30 ms**<br>[Discussion](https://news.ycombinator.com/item?id=49883844) · [Original](https://github.com/firelex/jeff) | 574 / 225 | Release discussion for Jeff’s small decision models, local inference, and training approach. |
| **Kev: Tiny Jev-like family of decision models built on top of Qwen3.5**<br>[Discussion](https://news.ycombinator.com/item?id=49783999) · [Original](https://github.com/jaredpalmer/kev/tree/main) | 462 / 211 | Kev release discussion covering open weights, implementation choices, comparisons, and model size. |
| **OpenAI is well positioned to fast-follow Jev**<br>[Discussion](https://news.ycombinator.com/item?id=49802161) · [Original](https://arcturus-labs.com/blog/2026/09/21/will-openai-eat-jevs-lunch/) | 328 / 233 | Debate about incumbent model providers, product differentiation, and Jev-style interfaces; market predictions are opinions. |
| **Show HN: Jev Plays Pokémon Red**<br>[Discussion](https://news.ycombinator.com/item?id=49845172) · [Original](https://jev-pokemon.vercel.app/) | 282 / 124 | A Pokémon Red demonstration and discussion of the role of game state, legal actions, and the surrounding agent harness. |
| **Jeeves. Reasoning improves Jev-like decision models**<br>[Discussion](https://news.ycombinator.com/item?id=49891290) · [Original](https://github.com/PostHog/jeeves) | 242 / 95 | Jeeves release discussion about adding reasoning to Jev-style classifiers. |
| **Jev-Leftpad**<br>[Discussion](https://news.ycombinator.com/item?id=49784706) · [Original](https://github.com/f/jev-leftpad) | 234 / 87 | A humorous left-padding package powered by model decisions; useful as community history, not an infrastructure recommendation. |
| **Language models for text classification: From bag-of-words to Jev**<br>[Discussion](https://news.ycombinator.com/item?id=49891203) · [Original](https://magazine.sebastianraschka.com/p/classifier-history-and-jev) | 213 / 10 | Discussion of Sebastian Raschka’s history of text classification and explanation of Jev-style decision interfaces. |
| **I turned Jev into a (lousy) chatbot**<br>[Discussion](https://news.ycombinator.com/item?id=49778162) · [Original](https://github.com/kyle-pena-nlp/jevchat/) | 177 / 50 | An experiment generating text through repeated character choices, illustrating the limits of using Jev as a chatbot. |
| **Reverse-engineered Jev-like model**<br>[Discussion](https://news.ycombinator.com/item?id=49731282) · [Original](https://github.com/vinnylarouge/jevlike) | 169 / 24 | Early independently built Jev-like option scorer; “reverse-engineered” in the thread title does not establish access to TypeSafe’s architecture. |
| **Show HN: JevBench, a reproducible benchmark for typed decision models**<br>[Discussion](https://news.ycombinator.com/item?id=49800574) · [Original](https://benchmarkheaven.com/jev-models) | 153 / 39 | Discussion of JevBench, its evaluation design, and cross-model comparisons. |
| **Jev Can't Be Calibrated**<br>[Discussion](https://news.ycombinator.com/item?id=49816899) · [Original](https://www.alexmolas.com/2026/09/23/jev-cant-be-calibrated.html) | 65 / 61 | Debate about distribution-dependent calibration and what a probability returned by Jev means. |

### Technical blogs and tutorials

- **[Jev introduces a new shape of LLM—System One, aka Decision Models](https://simonwillison.net/2026/Sep/21/jev/)** — `Article · 2026-09-21`. Simon Willison explains the interface, experiments, open recreations, and the difficulty of inspecting a numeric decision.
- **[Language Models for Text Classification: From Bag-of-Words to Jev](https://magazine.sebastianraschka.com/p/classifier-history-and-jev)** — `Article · 2026-09-29`. Sebastian Raschka places Jev in the history of classifiers, readout methods, and calibration; proposed internals are explicitly inferential.
- **[Building a Harness with Jev](https://www.langchain.com/blog/building-a-harness-with-jev)** — `Article · 2026-09-17`. LangChain’s tutorial on integrating bounded decisions into an agent loop, including routing and evaluation.
- **[Building Prod with Jev and LangGraph](https://www.langchain.com/blog/building-prod-with-jev-and-langgraph)** — `Article · 2026-09-25`. LangChain’s worked document-review workflow combines Jev classifications, graph orchestration, and escalation.
- **[What is Jev? — Browserbase](https://www.browserbase.com/blog/what-is-jev)** — `Article`. Browserbase explains how Stagehand can use Jev for bounded browser actions and fall back to an LLM.
- **[You could have built Jev](https://sgnt.ai/p/jev/)** — `Article`. Pete Sergeant explains option scoring and compares independent implementations; reproducing an interface does not prove model equivalence.
- **[Jev can’t be calibrated](https://www.alexmolas.com/2026/09/23/jev-cant-be-calibrated.html)** — `Article · 2026-09-23`. Alex Molas argues that calibration must be checked against the deployment distribution rather than assumed from a model-wide claim.
- **[Jev or a fine-tuned small model?](https://www.distillabs.ai/blog/jev-or-a-fine-tuned-small-model-we-built-a-pipeline-with-both-to-see-the-real-difference/)** — `Article · 2026-09-22`. Distil Labs reports a pipeline experiment comparing Jev and task-specific models on triage and invoice decisions. Results describe that vendor’s setup.

### Reddit debates

- **[Laya author’s prior-work discussion](https://www.reddit.com/r/LocalLLaMA/comments/1wihgum/i_literally_built_the_jev_architecture_one_year/)** — `Discussion`. First-person account linking earlier sales-prediction and confidence-routing work. Architectural equivalence and priority claims are disputed and are not established by this thread.
- **[Is Jev a new model class or a classifier?](https://www.reddit.com/r/LocalLLaMA/comments/1woe70t/jev_isnt_new_tech_its_marketing_targets_people/)** — `Discussion`. Community debate about novelty, zero-shot classification, and the difference between a useful product and a new architecture.

### Discovery directories

- **[Awesome Jev / TypeSafe — AbdelStark](https://github.com/AbdelStark/awesome-typesafe-jev)** — `Directory`. Broad community directory of integrations, demos, and independent tests. Used for discovery; listed projects should be checked at their original sources.
- **[Awesome Jev — heyjunpenn](https://github.com/heyjunpenn/awesome-jev)** — `Directory`. Larger community project catalog useful for discovering the long tail of Jev applications.
- **[Awesome Jev — Amal-David](https://github.com/Amal-David/awesome-jev)** — `Directory`. Community collection with projects, skills, demonstrations, and a curated social-post gallery.


## 3. Infrastructure, models, and applications

Official clients, hosted access, independent weights, and local implementations are labeled separately. A compatible API does not imply the same architecture, training data, calibration, or capability as TypeSafe’s Jev. Model and data licenses remain those of their respective publishers.

### Official SDKs and tools

- **[TypeSafe Python SDK](https://github.com/typesafe-ai/typesafe-sdk-python)** — `Official open-source code`. Official synchronous and asynchronous Python client for Jev.
- **[TypeSafe JavaScript / TypeScript SDK](https://github.com/typesafe-ai/typesafe-sdk-js)** — `Official open-source code`. Official client with inferred answer types and typed question helpers.
- **[TypeSafe Agent Skills](https://github.com/typesafe-ai/skills)** — `Official open-source code`. Official integration guidance for coding agents and skill-compatible tools.
- **[System One Adapter](https://github.com/typesafe-ai/system-one-adapter-python)** — `Official open-source code`. Official adapter that runs the decision interface over other LLM APIs for comparisons; it does not expose Jev weights.
- **[WorkflowEvals](https://github.com/typesafe-ai/WorkflowEvals)** — `Official open-source code`. Source code for TypeSafe’s workflow evaluations. Its reference answers come from other models.
- **[TypeSafe n8n nodes](https://github.com/typesafe-ai/n8n-nodes-typesafe-ai)** — `Official open-source code`. Official repository for connecting the TypeSafe API to n8n workflows.

### Hosted access and framework guides

- **[Vercel AI Gateway](https://vercel.com/changelog/typesafe-ai-jev-now-available-on-ai-gateway)** — `Hosted integration`. Provider announcement and usage examples for accessing Jev through AI Gateway.
- **[Cloudflare Workers AI](https://developers.cloudflare.com/ai/models/typesafe/jev/)** — `Hosted integration`. Provider-maintained Jev model page and structured evaluation examples.
- **[OpenRouter Jev playground](https://openrouter.ai/labs/jev/compile)** — `Hosted integration`. Provider playground for turning a task into typed Jev questions.
- **[Netlify AI Gateway](https://docs.netlify.com/build/ai-gateway/overview/)** — `Hosted integration`. Provider documentation covering gateway configuration and TypeSafe integration.

### Browser and agent infrastructure

- **[Jev Ultrafast](https://github.com/browser-use/jev-ultrafast)** — `Open-source code`. Browser Use’s agent represents available browser actions as candidates and uses Jev to select operations and targets.
- **[Jev Browser](https://github.com/jkudish/jev-browser)** — `Open-source code`. Playwright navigation exposed as a library, CLI, and MCP server, with bounded action selection.
- **[Jev MCP — Python](https://github.com/blakestone-x/jev-mcp)** — `Open-source code`. MCP server exposing classification, scoring, checking, matching, and screening through Jev.
- **[Jev MCP — Node](https://github.com/jkudish/jev-mcp)** — `Open-source code`. MCP tools for evidence checks, ranking, candidate selection, extraction, and patch review.
- **[Jev-Mem](https://github.com/libingzheren/Jev-Mem)** — `Open-source code`. Agent memory architecture using fast decisions for organization and retrieval, with a separate model for answer synthesis. [Paper](https://arxiv.org/abs/2609.23986).

### Language clients and data systems

- **[DuckDB Jev](https://github.com/prasanthj/duckdb-jev)** — `Open-source code`. DuckDB extension for Jev-backed predicates, classification, and scores over rows.
- **[pg-jev](https://github.com/realZachi/pg-jev)** — `Open-source code`. PostgreSQL extension for typed judgments and probability predicates over table rows.
- **[jev — CLI and skill](https://github.com/okooo5km/jev)** — `Open-source code`. Community command-line wrapper supporting direct TypeSafe and OpenRouter backends.
- **[Jev Java](https://github.com/jevkit/jev-java)** — `Open-source code`. Community Java client with typed questions and configurable retries.
- **[jev — Haskell](https://github.com/realbogart/jev)** — `Open-source code`. Community Haskell client with composable typed questions and probability-preserving responses.

### Open-weight decision models

- **[Laya](https://github.com/NandhaKishorM/laya)** — `Open weights and code`. Independent encoder-based decision models with English, multilingual, and workflow-specialist checkpoints; includes training and local serving. [English weights](https://huggingface.co/convaiinnovations/laya) · [Multilingual weights](https://huggingface.co/convaiinnovations/laya-multilingual) · [Demo](https://huggingface.co/spaces/convaiinnovations/laya-demo).
- **[Kev](https://github.com/jaredpalmer/kev)** — `Open weights and code`. Qwen-based family with released decision checkpoints, training code, evaluation suites, and TypeSafe-compatible serving. [0.8B](https://huggingface.co/jaredpalmer/kev-0.8b) · [4B](https://huggingface.co/jaredpalmer/kev-4b) · [9B](https://huggingface.co/jaredpalmer/kev-9b) · [27B](https://huggingface.co/jaredpalmer/kev-27b) · [Demo](https://huggingface.co/spaces/jaredpalmer/kev).
- **[Bespoke Nimble](https://github.com/bespokelabsai/nimble)** — `Open weights and code`. Independent decision model with a contrastive data-curation recipe and public benchmark comparisons. Its authors state it was not distilled from Jev. [Weights](https://huggingface.co/bespokelabs/Bespoke-Nimble-9B).
- **[Jeff — firelex](https://github.com/firelex/jeff)** — `Open weights and code`. Small decision models with local inference and domain adapters; distinct from other projects also called Jeff. [Weights](https://huggingface.co/mstrasser/Jeff-Qwen3.5-0.8B).
- **[Jeeves](https://github.com/PostHog/jeeves)** — `Open weights and code`. PostHog’s reasoning decision model, adding a diffusion drafter to a Qwen-based classifier; not a strictly one-pass decision model. [Weights](https://huggingface.co/PostHog/jeeves) · [FP8 weights](https://huggingface.co/PostHog/jeeves-fp8).
- **[Contrastive Language Models](https://github.com/Contrastive-LM/CLM)** — `Open weights and code`. Contrastive state/action modeling with a TypeSafe-compatible API and an independently released 8B model. [Weights](https://huggingface.co/Contrastive-LM/CLM-v0.1-8B).
- **[Vev](https://github.com/Xiaooolong/vev)** — `Open weights and code`. Independent visual and textual decision models based on Qwen3.5, with 4B and 9B releases. [4B weights](https://huggingface.co/CountingSheep/vev-4b) · [9B weights](https://huggingface.co/CountingSheep/vev-9b).
- **[WebJev](https://github.com/lexmount/WebJev)** — `Open weights and code`. Decision-model fine-tune specialized for browser actions; includes live-web data and evaluation harnesses. [Weights](https://huggingface.co/Lexmount/WebJev-35B-A3B) · [Dataset](https://huggingface.co/datasets/Lexmount/WebJev).
- **[NanoJev](https://github.com/TianyuCodings/NanoJev)** — `Open weights and code`. Compact 0.6B model and training pipeline for parallel decisions in game environments; its scope is narrower than general hosted Jev. [Weights](https://huggingface.co/C-Tianyu/NanoJev) · [Dataset](https://huggingface.co/datasets/C-Tianyu/NanoJev-Data).
- **[this-that-model-1.0](https://huggingface.co/flock-io/this-that-model-1.0)** — `Open weights`. A 2B typed-decision model with a research preprint. Reported speed and cost depend on its hardware and evaluation setup. [Paper](https://arxiv.org/abs/2609.23886).

### Training pipelines and announced releases

- **[Chinese-Jev](https://github.com/gulucaptain/Chinese-Jev)** — `Code available; weights pending`. Chinese decision-model training, calibration, and evaluation code. The project lists trained Chinese-Jev weights as planned, so this entry is not a downloadable-weight release. [Project](https://gulucaptain.github.io/Chinese-Jev/) · [Paper](https://arxiv.org/abs/2609.36965) · [CJ-Bench](https://huggingface.co/datasets/bbldCVer-hf/CJ-Bench) · [CJ-Dataset](https://huggingface.co/datasets/bbldCVer-hf/CJ-Dataset).

### Local runtimes and alternative implementations

- **[Ollaya](https://github.com/ollaya-dev/ollaya)** — `Open-source code`. Local runtime for pulling and serving multiple decision-model families behind a TypeSafe-compatible API. Independent of Ollama and TypeSafe.
- **[AnyJev](https://github.com/nokia-applied-research/AnyJev)** — `Open-source code`. Nokia Applied Research’s library for typed readouts from open LLMs, including option-bias correction and calibration modes.
- **[SemIf-OpenJev](https://github.com/TheoLeeCJ/SemIf-OpenJev)** — `Open-source code`. Open-model option scoring and semantic conditionals; formerly named OpenJev and SemIf. This is an independent implementation.
- **[OpenJev SGLang](https://github.com/ekzhang/openjev-sglang)** — `Open-source code`. Prefill-only decision serving over open models using SGLang.
- **[OpenJev — DiffusionGemma](https://github.com/razorback16/openjev)** — `Open-source code`. Independent TypeSafe-compatible server reading typed decisions from DiffusionGemma, with NVIDIA and Apple silicon paths.
- **[open-jev — daseinlabs](https://github.com/daseinlabs/open-jev)** — `Open-source code`. Local Gemma option scorer using shared context and candidate sequence likelihoods.
- **[Jevlike](https://github.com/vinnylarouge/jevlike)** — `Open-source code`. Independent model and training starter that scores a changing set of candidate options in one pass.

### Benchmarks, calibration, and datasets

- **[JevBench](https://github.com/fstandhartinger/jevbench)** — `Open-source code`. Independent multi-model benchmark with versioned scoring and results. Composite rankings depend on the published accuracy, calibration, latency, and cost methodology. [Leaderboard](https://www.benchmarkheaven.com/jev-models).
- **[Jevals](https://github.com/Jevals/jevals-data)** — `Open-source code`. Public benchmark suites and per-decision results for hosted Jev and comparator models. [Results](https://jevals.com/) · [Methodology](https://jevals.com/methodology/).
- **[Jev Decision Index](https://huggingface.co/spaces/multimodalart/jev-decision-index)** — `Benchmark`. Interactive community comparison of decision-model systems hosted as a Hugging Face Space.
- **[Janus](https://github.com/FirasSX914/Janus)** — `Open-source code`. Calibration and cascade experiments using Jev and a larger fallback model on labeled classification tasks.
- **[jev-certify](https://github.com/nikkoxgonzales/jev-certify)** — `Open-source code`. Conformal routing and auditing toolkit with a CLINC150 study; its guarantees depend on calibration and deployment assumptions.
- **[Jev benchmarking — AppliedMachineLearning-Lab](https://github.com/AppliedMachineLearning-Lab/jev-benchmarking)** — `Open-source code`. Code accompanying the 37-dataset Jev evaluation; keep model versions and request templates fixed when reproducing it. [Paper](https://arxiv.org/abs/2609.37647).
- **[RLCDAlignBench](https://github.com/sumleo/RLCDAlignBench)** — `Open-source code`. Benchmark of typed decisions for detecting alignment failures, with code and data linked from its paper. [Paper](https://arxiv.org/abs/2609.29429).
- **[JevOut](https://github.com/xzx34/JevOut)** — `Open-source code`. Research code for testing whether natural-looking context changes can redirect a decision model. [Paper](https://arxiv.org/abs/2609.30243) · [Project](https://xzx34.github.io/jevout/).

### Examples, games, and learning projects

- **[Jev Cookbook](https://github.com/nexibeo/jev-cookbook)** — `Open-source code`. Runnable recipes for support triage, classification, search, data cleanup, and browser actions.
- **[Jev Explained](https://github.com/davila7/jev-explained)** — `Open-source code`. Interactive educational playground for observing typed decisions and probabilities.
- **[Jev Showcase](https://github.com/cobusgreyling/Jev)** — `Open-source code`. Unofficial operator lab, smart-home examples, and a TypeScript harness.
- **[JEV-Star](https://github.com/sc2musa/Jev_Star)** — `Open-source code`. Research implementation combining Jev action selection with longer-horizon StarCraft II planning.
- **[Jev chat](https://github.com/kyle-pena-nlp/jevchat)** — `Open-source code`. Character-by-character generation experiment built on a decision interface; deliberately illustrates an awkward use case.
- **[Jev Leftpad](https://github.com/f/jev-leftpad)** — `Open-source code`. Satirical package that uses model decisions for string padding.


## 4. Research papers

Grouped by research topic; chronological within each group. Dates are first arXiv submission dates, while descriptions reflect the version accessed during this review. **Preprint** does not imply peer review. Summaries describe the authors’ work, not independently reproduced findings. Code/model links are included where located; absence of a link means it was not located, not that no artifact exists.

### Surveys and broad evaluations

- **[Evaluating Decision Models for Text Annotation in Computational Social Science](https://arxiv.org/abs/2609.24574)** — `Preprint · 2026-09-21`. Studies computational social-science annotation, comparing accuracy, confidence, and the economics of escalation to LLMs. [PDF](https://arxiv.org/pdf/2609.24574).
- **[Jev in the Wild: A Data-Driven Analysis of the Jev Model's Functionality, Applications and Ecosystem](https://arxiv.org/abs/2609.30216)** — `Preprint · 2026-09-24`. Analyzes 2,170 public Jev-related GitHub projects, distinguishing ecosystem activity from concentrated public attention. [PDF](https://arxiv.org/pdf/2609.30216).
- **[Typed Decision Models: An Early Evidence Audit and Evaluation Checklist](https://arxiv.org/abs/2609.32160)** — `Preprint · 2026-09-26`. Reviews 28 early papers and derives an evaluation checklist. An early evidence map, not a settled verdict on the model class. [PDF](https://arxiv.org/pdf/2609.32160).
- **[Evaluating and Benchmarking the System One Model Jev](https://arxiv.org/abs/2609.37647)** — `Preprint · 2026-09-29`. Evaluates Jev on 37 datasets with frozen prompts and full evaluation splits. Covers calibration, multilingual behavior, and sensitivity to answer formats. [PDF](https://arxiv.org/pdf/2609.37647) · [GitHub](https://github.com/AppliedMachineLearning-Lab/jev-benchmarking).

### Judging, calibration, and reliability

- **[JEV-as-a-Judge: Accept When Confident, Escalate When Unsure](https://arxiv.org/abs/2609.26550)** — `Preprint · 2026-09-22`. Tests Jev as a first-stage evaluator and routes uncertain decisions to a stronger judge. Benefits vary with workload and reasoning demands. [PDF](https://arxiv.org/pdf/2609.26550).
- **[Type-Safe Is Not Error-Free: A Constrained Decision Head Follows the Option Name, Not the Rubric Bound to It](https://arxiv.org/abs/2609.26758)** — `Preprint · 2026-09-22`. Changes option names while preserving their rubrics to expose semantic label bias despite valid output types. [PDF](https://arxiv.org/pdf/2609.26758).
- **[Just Ask Jev: Reinforcement Learning for Calibrated Decisions as a Zero-Shot Detector of AI Alignment Failures](https://arxiv.org/abs/2609.29429)** — `Preprint · 2026-09-24`. Introduces RLCDAlignBench to study zero-shot detection of alignment failures, including the influence of wording and supplied context. [PDF](https://arxiv.org/pdf/2609.29429) · [GitHub](https://github.com/sumleo/RLCDAlignBench).
- **[JEV vs. LLMs as Rubric Judges: Cheaper, Faster, and Wrong in the Same Places](https://arxiv.org/abs/2609.29769)** — `Preprint · 2026-09-24`. Compares rubric judges and shows why correlated errors can limit the accuracy gains of a confidence-based cascade. [PDF](https://arxiv.org/pdf/2609.29769).
- **[Beyond Calibration: Do a Typed-Decision Model's Probabilities Obey the Probability Axioms?](https://arxiv.org/abs/2609.33209)** — `Preprint · 2026-09-27`. Checks logical consistency across related probability questions, distinguishing probability coherence from accuracy and calibration. [PDF](https://arxiv.org/pdf/2609.33209).

### Robustness and security

- **[Decision Hijacking: Prompt Injection Attacks on Jev's Typed Probabilistic Decisions](https://arxiv.org/abs/2609.28613)** — `Preprint · 2026-09-23`. Measures prompt-injection effects on allowed action probabilities and selections; schema constraints do not eliminate decision manipulation. [PDF](https://arxiv.org/pdf/2609.28613).
- **[Calibrated Decision Models for Autonomous Penetration-Testing Harnesses: JEV and Laya as System One Decision Layers for LLM-Driven Pentest Agents](https://arxiv.org/abs/2609.28940)** — `Preprint · 2026-09-24`. Explores Jev and Laya as decision layers in penetration-testing agents. The reported two-run case study is exploratory, not strong causal evidence. [PDF](https://arxiv.org/pdf/2609.28940).
- **[JevOut: Natural Context Can Flip Decision Models](https://arxiv.org/abs/2609.30243)** — `Preprint · 2026-09-24`. Optimizes ordinary-looking context additions that flip initially correct decisions toward a fixed wrong option. [PDF](https://arxiv.org/pdf/2609.30243) · [GitHub](https://github.com/xzx34/JevOut) · [Project](https://xzx34.github.io/jevout/).

### Agent memory, routing, and control

- **[Jev-Mem: System-One-Controlled Agentic Memory for Efficient AI Agents](https://arxiv.org/abs/2609.23986)** — `Preprint · 2026-09-21`. Separates memory-management decisions from answer generation using a System One controller and a multi-relational memory graph. [PDF](https://arxiv.org/pdf/2609.23986) · [GitHub](https://github.com/libingzheren/Jev-Mem).
- **[REFLEX with Jev for Efficient Selective Control in LLM Agents](https://arxiv.org/abs/2609.26532)** — `Preprint · 2026-09-22`. Studies a Jev-first agent controller with stronger-model fallback and examines when it improves on inexpensive generative cascades. [PDF](https://arxiv.org/pdf/2609.26532).
- **[JEV-Star: Fast, Low-Cost StarCraft II Control with Language-Model Planning](https://arxiv.org/abs/2609.27331)** — `Preprint · 2026-09-23`. Combines fast Jev actions with persistent LLM planning for StarCraft II; the comparison does not isolate planning from all harness changes. [PDF](https://arxiv.org/pdf/2609.27331) · [GitHub](https://github.com/sc2musa/Jev_Star).
- **[Harness Tokenomics: A Router for the Enterprise Agentic Control Plane](https://arxiv.org/abs/2609.28919)** — `Preprint · 2026-09-24`. Examines model routing while accounting for prompt-cache ownership and session boundaries. Savings are based on the paper’s workload and pricing assumptions. [PDF](https://arxiv.org/pdf/2609.28919).
- **[Jev-Mobile: Jev as an Executor for Mobile GUI Agents](https://arxiv.org/abs/2609.30186)** — `Preprint · 2026-09-24`. Uses occasional VLM planning with Jev choosing actions from an Android accessibility-tree action space. [PDF](https://arxiv.org/pdf/2609.30186).
- **[JevSpawn: Adaptive Agentic Inference through Compositional Action Spaces](https://arxiv.org/abs/2610.00437)** — `Preprint · 2026-09-30`. Builds and revises compositional action spaces to connect natural-language tasks with finite probabilistic exploration. [PDF](https://arxiv.org/pdf/2610.00437).

### Open and alternative decision-model methods

- **[this-that-model-1.0: A typed decision model that decides in 30 ms, for a millionth of a cent](https://arxiv.org/abs/2609.23886)** — `Preprint · 2026-09-20`. Presents a 2B model with a direct typed readout. Includes released weights and discusses weaknesses on multi-step arithmetic. [PDF](https://arxiv.org/pdf/2609.23886) · [Model](https://huggingface.co/flock-io/this-that-model-1.0).
- **[Universal Fractal Natural Language Decision Map: Real-Time Edge Triage Across Heterogeneous Domains](https://arxiv.org/abs/2609.25498)** — `Preprint · 2026-09-21`. Proposes a fractal computation approach to typed edge decisions and reports JevBench results. Its unusual claims remain author-reported and require independent validation. [PDF](https://arxiv.org/pdf/2609.25498).
- **[Visual Jev: Accurate and Efficient Decisions from Shared Visual Context](https://arxiv.org/abs/2609.25845)** — `Preprint · 2026-09-22`. Shares visual context across independent questions and separates quality gains from post-training from speed gains due to shared execution. [PDF](https://arxiv.org/pdf/2609.25845) · [GitHub](https://github.com/guanxuyu-sv/Visual-Jev).
- **[NumericJev: Jev-like LLM Numerical Decoding with Multiway Decision Trees](https://arxiv.org/abs/2609.28587)** — `Preprint · 2026-09-23`. Uses multiway decision trees to obtain numerical outputs at a chosen resolution from structured-choice models without additional training. [PDF](https://arxiv.org/pdf/2609.28587) · [GitHub](https://github.com/Bring-AI/jev-numeric).
- **[From Text Decisions to Pixels: An Study of Jev-Style Visual Choice Model](https://arxiv.org/abs/2609.29283)** — `Preprint · 2026-09-24`. Introduces PixelJev for decisions over images and supplied candidates, studying adaptation, calibration, and transfer across visual tasks. [PDF](https://arxiv.org/pdf/2609.29283).

### Networking and edge systems

- **[Replacing Large Language Models with Jev Decision Models for Low-Latency Edge Service Orchestration](https://arxiv.org/abs/2609.22753)** — `Preprint · 2026-09-19`. Evaluates bounded intent interpretation with shared admission and scheduling logic, measuring decision overhead and timely service completion. [PDF](https://arxiv.org/pdf/2609.22753).
- **[Fast Intent-Driven Service Orchestration with Jev for 6G Edge Networks](https://arxiv.org/abs/2609.23136)** — `Preprint · 2026-09-19`. Studies Jev-based intent activation for 6G edge services using network simulation, shared queues, and a real image-reading service. [PDF](https://arxiv.org/pdf/2609.23136).
- **[Type-Safe Decision Frameworks for Agentic 5G Control: A Theory-Driven Testbed Characterization of Where They Can Be Applied](https://arxiv.org/abs/2609.33689)** — `Preprint · 2026-09-27`. Compares hosted Jev, a typed encoder, and an LLM retrofit on a 5G control testbed, examining deadlines, question sensitivity, and escalation. [PDF](https://arxiv.org/pdf/2609.33689).

### Domain applications and multilingual models

- **[Open-Jev Judgments on CallScreenBench: Calibrated One-Pass Scam Screening with a Small Language Model](https://arxiv.org/abs/2609.23959)** — `Preprint · 2026-09-21`. Studies JevLite for per-turn scam-call screening. Synthetic calls and test-set exposure limit the scope of the reported results. [PDF](https://arxiv.org/pdf/2609.23959).
- **[Calibrated Decisions at Scale: Converting Police Crash Narratives into Probabilistic Crash Variables with a System One Model (Jev)](https://arxiv.org/abs/2609.24052)** — `Preprint · 2026-09-21`. Converts crash narratives into probabilistic variables with a typed schema and audits decisions against human judgments and coded records. [PDF](https://arxiv.org/pdf/2609.24052).
- **[JEVQA - Video Quality from Metadata, Bitstream, and Pixel Features with a General-Purpose Decision Model](https://arxiv.org/abs/2609.24395)** — `Preprint · 2026-09-21`. Predicts video quality from supplied metadata and derived features; this is not native video understanding by hosted Jev. [PDF](https://arxiv.org/pdf/2609.24395).
- **[Jev for Scientific Decisions: Evaluating Semantic Choices and Their Consequences](https://arxiv.org/abs/2609.24965)** — `Preprint · 2026-09-21`. Tests semantic choices that feed scientific calculations and distinguishes correct final labels from correct intermediate relations. [PDF](https://arxiv.org/pdf/2609.24965).
- **[KITE: Scaling Jev Population Experiments with Sparse Flagship Calibration](https://arxiv.org/abs/2609.27535)** — `Preprint · 2026-09-23`. Caches decision kernels over unique states for population simulations and uses sparse stronger-model anchors with explicit uncertainty accounting. [PDF](https://arxiv.org/pdf/2609.27535) · [GitHub](https://github.com/HengyuLi-Ozaki-lab/kite_population_simulator).
- **[Can Jev Judge Radiology Reports? Evaluating a System One Model for Clinical Factuality](https://arxiv.org/abs/2609.27607)** — `Preprint · 2026-09-23`. Tests Jev as a reference-based judge of radiology-report factuality. Report agreement and clinical error detection are evaluated separately. [PDF](https://arxiv.org/pdf/2609.27607).
- **[Same Scores, Different Decisions: Evaluating JEV and Language Models for Legal Document Understanding](https://arxiv.org/abs/2609.27678)** — `Preprint · 2026-09-23`. Evaluates contract inference under repeated and changed request conditions, showing why aggregate accuracy can hide unstable individual decisions. [PDF](https://arxiv.org/pdf/2609.27678) · [GitHub](https://github.com/ZF-Utokyo/Jev-Benchmark).
- **[Chinese-Jev: Bringing System One Model to Chinese-Language Tasks](https://arxiv.org/abs/2609.36965)** — `Preprint · 2026-09-29`. Introduces Chinese-language decision training and CJ-Bench, including domain specialists and on-device experiments. Weights were still pending in the checked repository. [PDF](https://arxiv.org/pdf/2609.36965) · [GitHub](https://github.com/gulucaptain/Chinese-Jev) · [Project](https://gulucaptain.github.io/Chinese-Jev/).

### Historical context cited in community debate

- **[SalesRLAgent: A Reinforcement Learning Approach for Real-Time Sales Conversion Prediction and Optimization](https://arxiv.org/abs/2503.23303)** — `Earlier preprint · 2025-03-30`. Earlier domain-specific reinforcement-learning probability prediction cited in the Laya author’s discussion. It predates Jev and does not document Jev’s proprietary architecture. [PDF](https://arxiv.org/pdf/2503.23303).
- **[Confidence-Aware Routing for Large Language Model Reliability Enhancement: A Multi-Signal Approach to Pre-Generation Hallucination Mitigation](https://arxiv.org/abs/2510.01237)** — `Earlier preprint · 2025-09-23`. Earlier confidence-based routing work cited in the community debate. Included as historical context, not as a Jev evaluation or evidence of architectural identity. [PDF](https://arxiv.org/pdf/2510.01237).
