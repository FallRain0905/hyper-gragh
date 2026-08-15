# Hyper-RAG runtime cache

The deployment bundle intentionally includes only `case1`, the small public demo cache.
Other local caches such as `hyper_base` and `hyper_chem` are not part of the deployable
working tree and are ignored by Git. Keep any private or experimental cache outside the
repository, or mount it explicitly in a private deployment.

`case1` is mounted read-only by the production Docker Compose configuration.
