# HyperChE

HyperChE is a domain-adaptive hypergraph RAG platform for chemical engineering literature. It is built on top of the original [Hyper-RAG](https://github.com/iMoonLab/Hyper-RAG) project and extends it toward chemical knowledge modeling, domain-specific extraction, Web deployment, public demos, multi-provider API management, conservative entity normalization, and benchmark evaluation.

The central idea is that chemical literature often contains facts that are not naturally pairwise. A conclusion may depend on a joint combination of system type, material, active species, operating condition, performance metric, and mechanistic evidence. HyperChE preserves these higher-order experimental facts as hyperedges, so retrieval can return a more complete context than plain vector RAG or pairwise Graph-RAG.

## Relationship To The Original Hyper-RAG

This repository is a derivative research and application project based on the original Hyper-RAG framework.

Original Hyper-RAG provides:

- Hypergraph-driven retrieval augmented generation.
- Low-order and high-order relation modeling.
- Hypergraph storage, entity/relation vector indexes, and RAG query logic.
- Baseline Hyper-RAG, Graph-RAG, and naive RAG query modes.

HyperChE adds:

- Chemical-engineering-oriented domain adaptation.
- JSON-based structured extraction for entities, low-order relations, and high-order hyperedges.
- Domain prompt packs for flow batteries and PFAS piezocatalysis.
- A conservative chemical entity normalization module.
- Measurement and condition instance nodes for numeric experimental facts.
- Stable real-paper corpus tracking with `doc_id`, `chunk_id`, source file metadata, manifests, and resumable build logs.
- Surface/canonical-aware embedding text templates for new experiment caches.
- Experiment modes for main experiments and ablation studies.
- Fact Coverage@k and QA evaluation CLIs.
- A React + FastAPI Web application branded as HyperChE.
- Login/register, admin settings, user API key management, trial quotas, and public demo pages.
- Multi-provider LLM and embedding API key pooling.
- Public demo streaming responses through SSE.
- Two curated case databases for paper experiments and platform demonstration.

## Current Case Databases

Only two curated case databases are kept in this formal repository:

| Case | Path | Domain | Description |
| --- | --- | --- | --- |
| Case 1 | `web-ui/backend/hyperrag_cache/case1` | `flow_battery_streamline` | Flow battery literature, including VRFB, ICRFB, membrane materials, electrode modification, additives, conditions, metrics, and degradation mechanisms. |
| Case 2 | `web-ui/backend/hyperrag_cache/case2` | `pfas_piezocatalysis` | PFAS/PFOA/PFOS/GenX removal, enrichment, degradation, defluorination, mineralization, piezocatalysis, contact-electro-catalysis, and mechanism evidence. |

The case databases contain large vector files. They are tracked with Git LFS. Before cloning or pushing this repository, install Git LFS:

```bash
git lfs install
```

## Project Structure

```text
Hyper-RAG/
|-- hyperrag/                         # Core Hyper-RAG library and domain prompt loader
|   |-- domains/
|   |   |-- default/
|   |   |-- flow_battery/
|   |   |-- flow_battery_streamline/
|   |   |-- pfas_piezocatalysis/
|   |   `-- generic_json/              # Legacy generic JSON profile, not the main baseline
|   `-- experiment.py                  # Experiment mode resolver
|-- hyperche/
|   `-- normalization/                 # Conservative chemical entity normalization
|-- configs/
|   |-- experiments/                   # Mode, cache-map, and QA-map examples
|   `-- normalization/                 # Alias registry, negative rules, equivalence maps
|-- scripts/
|   |-- build_experiment_cache.py      # Build benchmark caches by experiment mode
|   |-- evaluate_fact_coverage.py      # Fact Coverage@k evaluator
|   |-- evaluate_qa_answers.py         # Legacy seven-dimension QA answer evaluator
|   |-- run_qa_smoke_llm.py            # Current LLM QA benchmark runner
|   |-- generate_qa40_with_llm.py      # Generate QA questions separately from answering
|   |-- normalize_hypergraph.py        # Offline normalization audit tool
|   `-- report_normalization.py        # Normalization report helper
|-- web-ui/
|   |-- backend/                       # FastAPI backend
|   |   `-- hyperrag_cache/
|   |       |-- case1/                  # Curated flow-battery case database
|   |       `-- case2/                  # Curated PFAS case database
|   `-- frontend/                      # React frontend
|-- deploy/
|   `-- nginx.hyperche.conf            # Container Nginx config
|-- docker-compose.hyperche.yml        # Production-style Docker Compose stack
`-- .env.hyperche.example             # Deployment environment example
```

## Main Features

- Literature upload and knowledge-base management.
- Domain selection for chemical subfields.
- LLM-based structured extraction of entities and hyperedges.
- Hypergraph construction and visualization.
- Hyper-RAG, Graph-RAG, and naive RAG query modes.
- Conservative entity normalization with exact aliases, fuzzy candidates, negative rules, and optional LLM judgment.
- Numeric measurement/condition instance nodes, such as `measurement:ee_80_9_percent` and `condition:current_density_100_ma_cm2`.
- Resumable experiment-cache construction for large paper corpora.
- Collapsible retrieval graph in answers to avoid heavy rendering.
- Public demo page with streaming Hyper-RAG answers.
- Admin-managed global API providers and user-managed personal API keys.
- PostgreSQL-backed login/register and quota management for public testing.

## Domain Adaptation

HyperChE currently includes two chemical domain prompt packs and one generic JSON prompt profile.

### Flow Battery

Representative entity types include:

- `ACTIVE_SPECIES`
- `MEMBRANE`
- `ELECTRODE`
- `CONDITION`
- `METRIC`
- `DEGRADATION`
- `SYSTEM`

Representative relation / hyperedge types include:

- `COMPOSITION`
- `OPERATION`
- `DEGRADATION`
- `COMPARISON`

### PFAS Piezocatalysis

Representative entity types include:

- `PFAS_TARGET`
- `CATALYST_MATERIAL`
- `MATERIAL_FEATURE`
- `PIEZO_PROPERTY`
- `PROCESS_STRATEGY`
- `CONDITION`
- `METRIC`
- `ACTIVE_SPECIES`
- `MECHANISM_EVIDENCE`
- `WATER_MATRIX`

Representative relation / hyperedge types include:

- `MATERIAL_DESIGN`
- `OPERATION_PERFORMANCE`
- `MECHANISM_PATHWAY`
- `ADSORPTION_ORIENTATION`
- `CHARGE_TRANSFER`
- `COUPLING_STRATEGY`
- `MATRIX_APPLICATION`
- `COMPARISON`

### Generic JSON

`hyperrag/domains/generic_json/` keeps the same JSON output schema as the chemical prompts but uses generic entity and relation labels. It was introduced for an early prompt-profile ablation. The main benchmark baseline now uses the original Hyper-RAG delimiter-based `default` prompt, so `hyper_base` reflects the upstream-style extraction pipeline rather than a newly designed JSON baseline.

## Current Experiment Scope

The current paper-experiment track is intentionally simplified. The active QA comparison uses four groups:

| Group | Meaning |
| --- | --- |
| `hybrid_text` | Strong text retrieval baseline over the same cache chunks. |
| `chem_prompt_graph` | Chemical prompt extraction, evaluated as a pairwise graph view. |
| `chem_prompt_hypergraph` | Chemical prompt extraction, evaluated as a hypergraph view. |
| `norm_hg_reranker` | Normalized hypergraph with retrieval reranking enabled. |

Atomic evidence cards were used only in an earlier QA debugging branch. They are not part of the current main experiment. Do not pass `--chem-norm-evidence-v2` unless you intentionally want to reproduce that old ablation.

## Experiment Modes

Experiment modes are configured in `configs/experiments/modes.yaml`.

| Mode | Query View | Prompt Profile | Normalization | Measurement Instances | EFU Repair | Hybrid Rerank |
| --- | --- | --- | --- | --- | --- | --- |
| `graph_final` | graph | chemistry | on | on | on | on |
| `hyper_base` | hyper | default | off | off | off | off |
| `hyper_chem_prompt` | hyper | chemistry | off | off | off | off |
| `hyper_norm` | hyper | chemistry | on | off | off | off |
| `hyper_final` | hyper | chemistry | on | on | on | on |
| `final_no_measurement` | hyper | chemistry | on | off | on | on |
| `final_no_repair` | hyper | chemistry | on | on | off | on |
| `final_no_rerank` | hyper | chemistry | on | on | on | off |
| `final_full` | hyper | chemistry | on | on | on | on |

Each built cache writes a `run_config.json` file into the cache directory. The evaluator reads this metadata to decide graph/hyper view and reranking behavior.

## CLI Usage

### 1. Build An Experiment Cache

Set OpenAI-compatible LLM and embedding providers through environment variables:

```powershell
$env:LLM_API_KEY="sk-..."
$env:LLM_BASE_URL="https://api.deepseek.com"
$env:LLM_MODEL="deepseek-v4-flash"
$env:EMB_API_KEY="sk-..."
$env:EMB_BASE_URL="https://api.siliconflow.cn/v1"
$env:EMB_MODEL="Qwen/Qwen3-Embedding-4B"
$env:EMB_DIM="2560"
```

Build a cache for one mode:

```powershell
python scripts\build_experiment_cache.py `
  --input C:\Users\surface\Downloads\flow_battery_embedding_corpus.md `
  --cache-dir web-ui\backend\hyperrag_cache\flow_benchmark_hyper_final `
  --mode hyper_final `
  --domain flow_battery
```

Useful options:

```powershell
--chunk-size 1000
--chunk-overlap 100
--max-entities-per-chunk 40
--llm-timeout 600
--embedding-timeout 120
--llm-max-async 4
--embedding-max-async 4
--embedding-batch-num 8
```

For large real-paper corpora, use stable document IDs and resumable logs:

```powershell
$env:LLM_API_KEY="key1;key2;key3"
$env:LLM_BASE_URL="https://api.siliconflow.cn/v1"
$env:LLM_MODEL="deepseek-ai/DeepSeek-V4-Flash"
$env:EMB_API_KEY="key1;key2;key3"
$env:EMB_BASE_URL="https://api.siliconflow.cn/v1"
$env:EMB_MODEL="Qwen/Qwen3-Embedding-4B"
$env:EMB_DIM="2560"
$env:ENTITY_EXTRACT_MAX_GLEANING="0"

python scripts\build_experiment_cache.py `
  --input C:\Users\surface\OneDrive\Desktop\case1\mineru_output\all_markdown `
  --cache-dir web-ui\backend\hyperrag_cache\real_flow_80_fast_v3\hyper_base `
  --mode hyper_base `
  --domain flow_battery `
  --doc-id-prefix RFB `
  --doc-start 1 `
  --doc-end 15 `
  --resume `
  --chunk-size 1000 `
  --max-entities-per-chunk 40 `
  --llm-max-async 6 `
  --embedding-max-async 10 `
  --embedding-batch-num 16
```

Each cache directory records:

```text
run_config.json
corpus_manifest.jsonl
build_progress.jsonl
kv_store_full_docs.json
kv_store_text_chunks.json
kv_store_community_reports.json
vdb_entities.json
vdb_relationships.json
```

Operational notes:

- `build_progress.jsonl` is an audit log, not the only source of truth. Treat a document as completed only when it is also present in persisted cache storage.
- Do not run multiple builders against the same cache directory at the same time.
- Parallel builds are allowed only when each process writes to a separate cache directory.
- `hyper_base` uses the original/default prompt and does not use one-pass JSON extraction or normalization.
- `hyper_chem_prompt` uses the chemistry JSON prompt and one-pass extraction, but no normalization.
- The current fast build phase does not run `hyper_final` normalization.

### 2. Configure A Multi-Mode Cache Map

Copy the example:

```powershell
Copy-Item configs\experiments\cache_map.example.yaml configs\experiments\cache_map.yaml
```

Then edit `configs/experiments/cache_map.yaml` so each mode points to its own cache directory.

### 3. Run Fact Coverage@k Evaluation

Single-cache legacy style:

```powershell
python scripts\evaluate_fact_coverage.py `
  --gold C:\Users\surface\Downloads\flow_battery_longdoc_gold_efu_facts_v03.json `
  --cache-dir web-ui\backend\hyperrag_cache\flow_benchmark_hyper_final `
  --k 1,3,5,10 `
  --judge-mode heuristic `
  --output web-ui\backend\hyperrag_cache\flow_benchmark_hyper_final\fact_coverage_report.json
```

Multi-mode, multi-judge style:

```powershell
$env:DEEPSEEK_API_KEY="sk-..."
$env:KIMI_API_KEY="sk-..."
$env:QWEN_API_KEY="sk-..."

python scripts\evaluate_fact_coverage.py `
  --gold C:\Users\surface\Downloads\flow_battery_longdoc_gold_efu_facts_v03.json `
  --modes graph_final hyper_base hyper_chem_prompt hyper_norm hyper_final `
  --cache-map configs\experiments\cache_map.yaml `
  --k-values 1 3 5 10 `
  --judge-mode llm `
  --judge-models kimi deepseek qwen `
  --output-dir outputs\fact_coverage\flow_v03_main
```

Fact Coverage outputs:

```text
outputs/fact_coverage/{run_id}/
|-- run_config.json
|-- fact_coverage_summary.csv
|-- fact_coverage_summary.json
|-- fact_coverage_full_judgments.json
|-- fact_coverage_llm_judgments.jsonl
|-- fact_coverage_heuristic_diagnostics.json
|-- evidence_contexts.jsonl
|-- model_raw_outputs.jsonl
|-- errors.jsonl
`-- run.log
```

### 4. Run Current QA Benchmark

The current LLM QA benchmark runner is `scripts/run_qa_smoke_llm.py`. It separates question files from answer generation and judging, supports resume through existing records, and writes raw records rather than summary-only outputs.

Example for the current four-group QA benchmark:

```powershell
$env:DEEPSEEK_API_KEY="key1;key2"
$env:SILICONFLOW_API_KEY="key1;key2"
$env:SILICONFLOW_BASE_URL="https://api.siliconflow.cn/v1"
$env:SILICONFLOW_MODEL="Qwen/Qwen3.5-122B-A10B"

python scripts\run_qa_smoke_llm.py `
  --benchmark-dir test-materials\hyperche_benchmark_v2 `
  --cache-root web-ui\backend\hyperrag_cache\real_flow_80_fast_v3 `
  --qa-mode full `
  --provider siliconflow `
  --judge-provider deepseek `
  --output-dir outputs\qa_eval\four_groups_40qa_current `
  --output-prefix qa_40 `
  --parallel-workers 4
```

Main QA outputs:

```text
outputs/qa_eval/{run_id}/
|-- qa_40_questions.json
|-- qa_40_records.jsonl
|-- qa_40_raw.json
|-- qa_40_summary.csv
|-- qa_40_summary.json
|-- qa_40_debug_failures.md
`-- errors.json
```

Do not pass `--chem-norm-evidence-v2` for the current experiment. That flag is deprecated and only preserves compatibility with the old atomic-card ablation.

### 5. Legacy QA Answer Evaluation

Create a QA answer map from the example:

```powershell
Copy-Item configs\experiments\qa_answer_map.example.yaml configs\experiments\qa_answer_map.yaml
```

Then run:

```powershell
python scripts\evaluate_qa_answers.py `
  --answer-map configs\experiments\qa_answer_map.yaml `
  --modes graph_final hyper_base hyper_chem_prompt hyper_norm hyper_final `
  --judge-models kimi deepseek qwen `
  --output-dir outputs\qa_eval\flow_v03_main
```

The QA evaluator scores each answer on seven dimensions:

- factual correctness
- condition completeness
- numerical accuracy
- mechanistic support
- comparative clarity
- source grounding
- readability

QA outputs:

```text
outputs/qa_eval/{run_id}/
|-- run_config.json
|-- qa_score_summary.csv
|-- qa_score_summary.json
|-- qa_full_judgments.json
|-- qa_llm_judgments.jsonl
|-- model_raw_outputs.jsonl
|-- errors.jsonl
`-- run.log
```

## Local Development

### Backend

```bash
cd web-ui/backend
python -m venv .venv
.venv/Scripts/activate  # Windows
pip install -r requirements.txt
python main.py
```

### Frontend

```bash
cd web-ui/frontend
npm install
npm run dev
```

The frontend uses `VITE_SERVER_URL` to locate the backend. In local development, the default backend URL is usually `http://localhost:8000`.

## Docker Deployment

Copy the environment example and edit secrets:

```bash
cp .env.hyperche.example .env
```

Start the stack:

```bash
docker compose -f docker-compose.hyperche.yml --env-file .env up -d --build
```

The stack includes:

- PostgreSQL
- Redis
- FastAPI backend
- React frontend
- Nginx reverse proxy

For public demo queries, set:

```env
HYPERCHE_PUBLIC_DEMO_DATABASE=case1
```

or:

```env
HYPERCHE_PUBLIC_DEMO_DATABASE=case2
```

## API Configuration

Global platform API providers are configured by the admin user in the Web settings page. Personal user API keys can also be added in the settings page and will take priority for that user's requests.

The backend supports OpenAI-compatible providers for both LLM and embedding calls. Multiple keys and multiple providers can be configured to improve throughput and failover.

## Notes For Repository Maintenance

- Do not commit local upload folders, user databases, SQLite files, logs, raw literature PDFs, or temporary files.
- Only the curated `case1` and `case2` HyperRAG databases are allowed under `web-ui/backend/hyperrag_cache/`.
- Large database files must remain under Git LFS.
- Local conversation examples are intentionally cleared from the public demo data.
- Keep experiment outputs under `outputs/`; commit only selected summaries when they are intended as paper artifacts.

## License And Attribution

This project is based on the original Hyper-RAG project by iMoonLab. Please cite and acknowledge the original Hyper-RAG work when using HyperChE in academic or derivative projects.
