# Atlas of Perdition — apparatus

## Working data

- `atlas_phenomena_seed.tsv`: curated, source-anchored observations with POE identifiers.
- `atlas_motif_families.tsv`: curated cross-witness motif assignments and notes.
- `Atlas_of_Perdition_Phenomena_Register.jsonl`: generated structured phenomena.
- `Atlas_of_Perdition_Second_Order_Index.tsv`: generated subclass assignments.
- `atlas_second_order.py`: curated subclass codebook and assignments.

The scene inventory, corpus survey, and evidence audits contain additional contextual findings. Retain them until their unique findings are incorporated and checked. The inclusion-criteria document records an earlier procedure; current POE decisions are held in the root `poe_register.tsv`.

## Regeneration

Run from this directory:

```sh
python atlas_sift.py
python build_phenomena_register.py
python atlas_second_order.py
```

The lexical CSV is produced on demand. Readable Markdown views are also optional:

```sh
python build_phenomena_register.py --views
python atlas_second_order.py --views
```

The original compilation is at `../testimonies/_intake/Experiences_1.txt`. Generation checks the source anchors and accepted POE status. The working observations, distinctions, and relationships remain subject to source-level verification.
