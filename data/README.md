# Data Layout

- `data/raw/parquet`: Bronze snapshots from source APIs
- `data/processed/parquet`: Silver/Gold exports
- `data/reference`: static mappings, factor tables, and metadata references

Standards:
- Partition by source/date where applicable.
- Preserve raw fields in Bronze before transformation.
- Track run metadata for traceability.
