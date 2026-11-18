# Testimony collection

This is the shared testimony collection for the Atlas of Perdition and the Atlas of Eternal Life. It holds acquired accounts, recordings and transcriptions of reported visions, dreams, near-death experiences, and resurrections, along with source leads. A testimony involving several realms remains one collection of source versions, regardless of which Atlas later uses its observations.

## Person collections

The collection is organized by **person → distinct reported experience → textual or recorded account/version**. Multiple tellings or translations of one experience are source versions, not new experiences.

A source document can be acquired before its reported experiences are separated. In that case, its `experience_id` remains blank in the source-copy register until the mapping is established.

## Source discovery

- [Local source-copy register](source_copy_register.tsv): Acquired source documents in their available formats, with URLs, byte counts, and checksums.
- [Matching-edition source register](edition_match_register.md): Publication links corresponding to the collector's wording, with access and variant notes.
- [Consolidated source manifest](source_manifest.tsv): Source artifacts, including verbatim extracts from the collector's working compilation, with provenance and copy paths.
- [Compilation provenance and checksums](compilation_provenance.md): Exact extract boundaries, master-file hash, and per-file SHA-256 values.
- [Experience and source-work register](experience_register.tsv): Historical experience and work-level entries; the root POE register governs current review.
- [Source discovery register](source_discovery_register.tsv): The collector's original discovery list, including source leads still being checked.
- [Discovery notes and intake boundaries](source_discovery_notes.md): Sources located, unresolved names, attribution rules, and testimony extent.

## Tracking

The [testimony tracker](testimony_tracker.md) preserves earlier collection and screening notes. The root [POE register](../poe_register.tsv) holds current author review decisions.

Run `python poe_registry.py intake` from the repository root to check each POE against acquired source copies and the original collector-supplied compilation, verifying their checksums. `incomplete_no_document` means no testimony document is on hand. `compilation_only` means the collector's testimony excerpt is archived but no separate source copy has been acquired. Document possession does not establish whether a telling is complete; [source notes](source_manifest.tsv) retain edition and scope information.
