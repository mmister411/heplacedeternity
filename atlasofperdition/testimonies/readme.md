# Testimonies

This area will collect files and maybe folders regarding collection of visions, dreams, near-death-events (NDE), resurrections (whether by ministry miracle or the Lord independently operating).  Some will be accounts, others artist depictions, and others still as indexes of links. The section of the project that this collection supports focuses on perdition.  Some testimonies contain strictly perdition but there are others such as Mary K. Baxter that spend time seeing the land of the upright.  There will be a collection elsewhere for that as well so some testimonies may be duplicated for data fidelity.  

## Person collections

The collection is organized by **person → distinct reported experience → textual or recorded account/version**. Multiple tellings or translations of one experience are source versions, not new experiences.

A source document can be acquired before its reported experiences are separated. In that case, its `experience_id` remains blank in the source-copy register until the mapping is established.

## Source discovery

- [Local source-copy register](source_copy_register.tsv): Retrieved PDFs and Markdown conversions, with URLs, byte counts, and checksums.
- [Matching-edition source register](edition_match_register.md): Publication links corresponding to the collector's wording, with access and variant notes.
- [Consolidated source manifest](source_manifest.tsv): Source artifacts, including 21 verbatim extracts from the collector's compilation for the 16 previously processed units, with provenance and copy paths.
- [Compilation provenance and checksums](compilation_provenance.md): Exact extract boundaries, master-file hash, and per-file SHA-256 values.
- [Experience and source-work register](experience_register.tsv): 17 records across 13 witnesses (Mary K. Baxter is counted as a book-level work; Bernarda Fernández's journeys are separate).
- [Source discovery register](source_discovery_register.tsv): 59 names from the collector's list, with up to two source leads per entry (101 distinct URLs). Source identification and topic categories are still being checked.
- [Discovery notes and intake boundaries](source_discovery_notes.md): Sources located, unresolved names, attribution rules, and conditions for collecting full testimony texts.

## Tracking

The [testimony tracker](testimony_tracker.md) records collected material, previously processed corpus units, author permissions for further processing, and later Atlas decisions.

Run `python poe_registry.py intake` from the repository root to check each POE against acquired source copies and the original collector-supplied compilation, verifying their checksums. `incomplete_no_document` means no testimony document is on hand. `compilation_only` means the collector's testimony excerpt is archived but no separate source copy has been acquired. Document possession does not establish whether a telling is complete; [source notes](source_manifest.tsv) retain edition and scope information.
