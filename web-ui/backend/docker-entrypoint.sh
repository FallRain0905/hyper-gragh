#!/bin/sh
set -eu

cache_seed_dir="${HYPERCHE_CACHE_SEED_DIR:-/app/cache_seed/case1}"
cache_runtime_dir="${HYPERCHE_CACHE_RUNTIME_DIR:-/app/hyperrag_cache/case1}"
required_cache_file="hypergraph_chunk_entity_relation.hgdb"

mkdir -p "$cache_runtime_dir"

if [ ! -f "$cache_runtime_dir/$required_cache_file" ]; then
    if [ ! -d "$cache_seed_dir" ] || [ ! -f "$cache_seed_dir/$required_cache_file" ]; then
        echo "[ERROR] HyperRAG case1 seed cache is missing from $cache_seed_dir" >&2
        exit 1
    fi

    echo "[INFO] Initializing writable HyperRAG case1 cache in $cache_runtime_dir"
    cp -a "$cache_seed_dir/." "$cache_runtime_dir/"
fi

exec "$@"
