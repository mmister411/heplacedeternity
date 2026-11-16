# Atlas of Perdition — Research Apparatus

This directory contains the working source-anchored survey, scene inventory, classification system, and cross-witness comparison for *Atlas of Perdition*. It supports the manuscript; it is not itself the finished book.

## Narrative and reference documents

- `Atlas_of_Perdition_Corpus_Survey.md` — overview of the collected witness accounts and scope.
- `Atlas_of_Perdition_Scene_Inventory.md` — testimony units and scene sequence.
- `Atlas_of_Perdition_Phenomena_Register.md` — 426 source-anchored phenomenon records.
- `Atlas_of_Perdition_Cross_Witness_Concordance.md` — 43 recurring motif families, with differences retained.
- `Atlas_of_Perdition_Cells_Chambers_Evidence_Audit.md` — first close-reading audit, comparing seven testimony units and recording one corrected cross-witness motif assignment.
- `Atlas_of_Perdition_Pits_Shafts_Recesses_Evidence_Audit.md` — second close-reading audit of seven testimony units, with source-level distinctions and pit-motif corrections.
- `Atlas_of_Perdition_Roads_Descent_Thresholds_Evidence_Audit.md` — third close-reading audit of four route-and-threshold motifs, with boundary and transit distinctions.
- `Atlas_of_Perdition_Torment_Recurring_Operations_Evidence_Audit.md` — fourth close-reading audit of six torment motifs, with eight mapping corrections and two source-description corrections.
- `Atlas_of_Perdition_Taxonomic_Architecture.md` — 10 primary divisions and 71 second-order subclasses, with definitions, boundaries, and examples.

## Structured indexes and working data

- `Atlas_of_Perdition_Phenomena_Register.jsonl` — structured form of the phenomena register.
- `Atlas_of_Perdition_Second_Order_Index.tsv` — one subclass assignment for each phenomenon; 40 records carry additional curated cross-references.
- `atlas_phenomena_seed.tsv` — curated descriptions and evidence anchors used to build the register.
- `atlas_motif_families.tsv` — hand-curated cross-witness motif definitions and mappings.
- `atlas_lexical_concordance.csv` — working lexical concordance.

## Build scripts

- `atlas_sift.py` — source section definitions and lexical concordance extraction.
- `build_phenomena_register.py` — register and motif concordance validation and generation.
- `atlas_second_order.py` — second-order codebook, assignments, validation, and output generation.

The scripts retain their existing relative-path conventions, which is why the working files are kept together in this directory. Regenerating the source-linked register requires the underlying testimony compilation at `upload/Pasted text(20261116-025409).txt` relative to this directory. That source compilation is not included here. `atlas_second_order.py` can regenerate its two outputs from the included JSONL register alone.

## Reading discipline

The records report what each witness says they encountered. A phenomenon, a statement attributed to a spiritual being, a narrator's inference, and a scriptural parallel remain distinguishable. Similarities among witnesses do not establish identical geography or the transmission history of their accounts. The supplied testimony compilation remains the source of line references.
