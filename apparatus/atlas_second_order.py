#!/usr/bin/env python3
"""Build a source-preserving second-order index for Atlas of Perdition.

All assignments below are curated against the 426 Phenomena Register records.
No existing record ID, primary category, evidence mode, or source line is changed.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path
import csv
import json


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "Atlas_of_Perdition_Phenomena_Register.jsonl"
INDEX = ROOT / "Atlas_of_Perdition_Second_Order_Index.tsv"
ARCHITECTURE = ROOT / "Atlas_of_Perdition_Taxonomic_Architecture.md"

# code, title, definition, inclusion boundary, usual referent-role, facet tags
CLASSES = [
    ("ENT-THR", "Thresholds and apertures", "Openings, gates, doors, ruptures and apparent windows through which a boundary is encountered or crossed.", "Use for the boundary aperture; distinguish the actual passage or descent as movement.", "entity", "boundary|access"),
    ("ENT-VOR", "Vortices and rotating passages", "Spinning funnels, tornadoes and rotational tunnel mechanisms associated with arrival or entry.", "Use where rotation is diagnostic; a plain falling tunnel belongs to ENT-DES.", "entity", "transit|rotation"),
    ("ENT-DES", "Downward transit", "Falls, lowering, subterranean descents and passage down into the region.", "Use for travel action; the pit arrived at remains a TOP structure.", "operation", "transit|direction"),
    ("ENT-TRA", "Escorted and liminal transport", "Movement by escorts, vehicles, sudden landscape changes or passage between frames of experience.", "Use where the means of transport or a liminal change is central and neither downward fall nor exit dominates.", "operation", "transit|guidance"),
    ("ENT-EGR", "Withdrawal and ascent", "Rising, rescue, outward removal and upward return journeys.", "Use for departure from the described region; a deceptive window without passage is ENT-THR.", "operation", "transit|release"),

    ("TOP-LAN", "Landforms and surface terrain", "Hills, valleys, plains, plateaus, swamp, rock, bare surfaces and exposed ground formations.", "Use for the landform; roads and excavated pits have separate subclasses.", "entity", "place|terrain"),
    ("TOP-ROU", "Routes and corridors", "Roads, paths, alleyways, tunnel connections and navigable trajectories between places.", "Use for a pathway's spatial arrangement; actual passage through it is ENT.", "entity", "place|movement"),
    ("TOP-PIT", "Pits, hollows and shafts", "Excavated or open chasms, abysses, caverns, recesses, shafts and pit grids.", "Use for void geometry; liquid or fiery contents may receive a second facet.", "entity", "place|enclosure"),
    ("TOP-CEL", "Cells and cell complexes", "Custodial rooms, constructed or imitative cells, clustered rooms, tiers and individualized chambers.", "Use for the room or block as a place; bars and chains as apparatus belong to CUS.", "entity", "place|architecture"),
    ("TOP-LIQ", "Bodies and channels of destructive fluid", "Lakes, rivers, oceans, boiling pools and volcanic liquid channels.", "Use for the body or channel and its course; the act of immersion belongs to OPR.", "entity", "place|substance"),
    ("TOP-REG", "Regional scope, arrangement and measurement", "Large divisions, depth claims, radial arrangements, spatial distance and overall organization.", "Use where scale, subdivision or relative position dominates, without making unlike geometries one map.", "relationship", "place|measurement"),
    ("TOP-FUN", "Functional and assembly sites", "Arenas, platforms, gathering cells and deliberately staged places of punishment or judgment.", "Use when a location's stated function organizes its identity; an ordinary single cell remains TOP-CEL.", "entity", "place|function"),
    ("TOP-ANA", "Anatomically conceived geography", "Regions conceived as body parts or organs, including a pulsating heart, horns, jaws and named anatomical districts.", "Use for anatomy-like layout or macrostructure; living wall material without an anatomical region is TOP-LIV.", "entity", "place|anatomy"),
    ("TOP-LIV", "Animate structures and living substrate", "Walls and cell fabric experienced as breathing, moving, soft or composed of living organisms.", "Use for a structural substance behaving as animate; a separate attached being belongs to BEI-ANI.", "entity", "place|animation"),
    ("TOP-DYN", "Mutable spatial extent", "Expansion or multiplication of spatial regions and structures over time.", "Use for changes to the extent or number of sites; temporary moving fire is an OPR event.", "operation", "place|change"),
    ("TOP-ACC", "Internal access construction", "Stairs, internal doors and architectural connectors linking subregions.", "Use for permanent built connectors; the witnessed crossing of a threshold belongs to ENT.", "entity", "place|access"),

    ("ENV-LUM", "Light, color and obscurity", "Darkness, restricted visibility, dimness, illumination and coloration of flames or atmospheric light.", "Use for visible environmental conditions, not special knowledge gained by the witness.", "property", "sight|illumination"),
    ("ENV-THM", "Temperature and thermal exposure", "Heat, cold, burning ambient temperature and gradients between thermal regions.", "Use for sensed or described temperature; fire as an operating punishment belongs to OPR.", "property", "temperature|sensation"),
    ("ENV-OLF", "Odor and atmospheric taste", "Sulfur, decay, fetid breath and related environmental smell or taste.", "Use for smelled material; the emitting being stays independently classified under BEI.", "property", "odor|sensation"),
    ("ENV-ACU", "Audible soundscape", "Cries, screams, laughter, rattling, commanding sounds and reported silence.", "Use for a sound or its absence; words that supply a judicial proposition remain in JUD.", "property", "sound|communication"),
    ("ENV-MED", "Ambient matter and ground textures", "Fog, dust, dry ground, insects within soil, liquid texture and descending substances.", "Use for medium or tactile material; a specifically named lake or river belongs to TOP-LIQ.", "property", "substance|touch"),
    ("ENV-PSN", "Sensory sensitivity and bodily response", "Altered perception, pain onset and unusual sensory or bodily response to the surrounding conditions.", "Use for sensory functioning or response rather than the objective object of perception.", "experience", "sensation|capacity"),
    ("ENV-PRI", "Deprivation of ordinary provision", "Thirst, lack of water, lack of rest or food, and inability to produce ordinary bodily relief.", "Use for privation; a resident's conclusion about eternal hopelessness is PSY.", "state", "deprivation|sensation"),
    ("ENV-KIN", "Ambient motion and disturbance", "Ground-shaking, gusting, pressure and other kinetic effects in the surrounding space.", "Use for environmental movement; direct bodily attack belongs to OPR.", "operation", "motion|environment"),

    ("BEI-SER", "Serpents and serpent assemblages", "Snakes, large serpents and serpents configured as apparent implements or religious objects.", "Use when serpentine identity dominates; hybrid rulers with serpent parts are BEI-HYB.", "entity", "organism|morphology"),
    ("BEI-VER", "Worms, insects and lesser fauna", "Worms, rats, spiders, biting beasts and other creeping or swarming organisms.", "Use for the entities; eating, gnawing or bodily injury is an additional operational facet.", "entity", "organism|morphology"),
    ("BEI-HYB", "Hybrid and anomalous morphology", "Animal-human composites, asymmetric figures, horns, scales, fins, claws and bodily anomalies.", "Use for form rather than inferred office; morphing or impersonation is BEI-DIS.", "entity", "morphology|body"),
    ("BEI-DIS", "Disguise, impersonation and metamorphosis", "Shifting forms, borrowed human likeness, beautiful deceiving appearances and animate props that impersonate objects.", "Use when change of appearance or deceptive likeness is the identifying trait.", "operation", "appearance|identity"),
    ("BEI-GRD", "Escorts, guards and active attendants", "Figures whose most salient feature is ushering, guarding, chasing, carrying, threatening or tormenting persons.", "Use for role and activity when no distinct morphology controls the report.", "entity", "agency|custody"),
    ("BEI-HIE", "Rulers, assemblies and assigned agents", "Named superior figures, hierarchies, councils, armies and beings acting under explicit assignments.", "Use for organizational identity and relation; the plan enacted may also be indexed in OPR.", "relationship", "agency|hierarchy"),
    ("BEI-ANI", "Beings embedded in objects or fabric", "Entities inseparable from walls, architecture or furnishings and described as animate or demonic.", "Use where an object and a creature coincide in the report; an ordinary breathing wall remains TOP-ANA.", "entity", "animation|substrate"),
    ("BEI-PRE", "Unresolved approaching presence", "A detected personal presence with identity or bodily features not yet supplied in the witnessed excerpt.", "Keep presence unresolved until a passage actually supplies identification.", "experience", "agency|presence"),

    ("CUS-ENC", "Custodial enclosures and barriers", "Barred rooms, confinement structures, locked cell fronts, coffins and structural separators.", "Use for the object imposing confinement; the landscape beyond it stays TOP.", "entity", "architecture|custody"),
    ("CUS-BND", "Bodily bonds and restraints", "Chains, ropes, shackles, binding creatures and immobilization of occupants or visitors.", "Use for restraint attached to a body or enforced immobility; a locked door is CUS-ENC.", "state", "custody|restriction"),
    ("CUS-MRK", "Identification plates and inscriptions", "Numbered cells, labels, marks, names, destination signs and written accusations displayed on bodies or sites.", "Use for inscription as public identifier; recordkeeping books are CUS-LED.", "entity", "writing|identification"),
    ("CUS-LED", "Ledgers and recorded accounts", "Books, lists, documentary records and account volumes inspected or consulted during a scene.", "Use for record-bearing objects; a life displayed supernaturally to the witness is EPI-REV.", "entity", "writing|records"),
    ("CUS-OBJ", "Custodial furnishings and implements", "Objects furnished within custody such as keys, chairs, dolls, altars and purpose-built instruments.", "Use when a tangible object or fixture is the reported phenomenon; its action is classified separately.", "entity", "equipment|function"),
    ("CUS-CTR", "Enforcement and unequal access", "Guards policing boundaries, barriers to contact, restricted powers of creatures and access prevented by unusual means.", "Use for the restriction as relation or operation; the guard's morphology remains BEI.", "relationship", "custody|access"),

    ("BOD-SKE", "Skeletal and decayed condition", "Charred, bare or decomposing remains, with or without residual flesh.", "Use for bodily form; the fire or weapon causing damage is an operation.", "state", "body|decay"),
    ("BOD-SOU", "Soul-body interior and composition", "Mist, soul-within-form and interior anatomical observations of the reported postmortem person.", "Use where composition is the point; witness's privileged method of seeing belongs to EPI.", "property", "body|composition"),
    ("BOD-REG", "Regrowth and bodily restoration", "Re-forming flesh, reconstituted bodies and renewal after destruction.", "Use for regeneration as bodily state; the repeating torture cycle is OPR-LOP.", "operation", "body|restoration"),
    ("BOD-DAM", "Wounds and bodily alterations", "Damage, piercing, heat rupture, serpentine contact and displaced bodily substance.", "Use where the changed body is primary; the assailant's activity is OPR-VIO.", "state", "body|injury"),
    ("BOD-FAC", "Bodily capacities and altered function", "Strength, bloodlessness, apparent trance and bodily performance contrary to ordinary expectations.", "Use for functional condition rather than tissue composition or the observer's sensory sensitivity.", "state", "body|capacity"),
    ("BOD-ATT", "Clothing, numerals and bodily markers", "Garments, attached plates, numbers and visible identifications of the body's status.", "Use for material displayed on a body; the inscription's content remains indexable as CUS-MRK.", "property", "body|identification"),

    ("OPR-VIO", "Direct mutilation and bodily assault", "Piercing, crushing, dismembering, stripping and attacking a body by force or weapon.", "Use for violent action; regrowth between attacks is separately indexed under BOD and OPR-LOP.", "operation", "violence|body"),
    ("OPR-IMM", "Burning, immersion and submersion", "Acts of consuming by flame, being forced into liquid fire and drawn beneath a harmful surface.", "Use for direct burning or immersion of persons; a fiery lake's geometry is TOP-LIQ.", "operation", "fire|torment"),
    ("OPR-LOP", "Recurring punitive sequences", "Cycles that reset a bodily state, scene, location or round of punishment.", "Use when repetition or reset is the organizing mechanism; a single attack is OPR-VIO.", "operation", "repetition|time"),
    ("OPR-ENA", "Compelled reenactment and activity", "Forced singing, preaching, gestures, fighting and staged earthly activities continuing under torment.", "Use for reproduced conduct; the stated reason for punishment is indexed in JUD.", "operation", "behavior|repetition"),
    ("OPR-MOC", "Mockery, accusation and coerced homage", "Ridicule, compulsory submission, accusation, derision and speech used as punitive action.", "Use where coercive or abusive communication is the operation; words of formal judgment are JUD.", "operation", "speech|coercion"),
    ("OPR-REM", "Forced transport and recapture", "Pulling occupants into cells or fire, dragging them elsewhere or preventing their departure by removal.", "Use for agents moving persons against their will; structural escape barriers belong to CUS.", "operation", "movement|custody"),
    ("OPR-ENV", "Active forces and changing medium", "Fire waves, rising liquids, invisible pressure, eruptive heat and other moving environmental assaults.", "Use where the medium or force acts rather than a creature applying a direct weapon.", "operation", "environment|force"),
    ("OPR-ORG", "Organized and administered torment", "Strategic meetings, shifts, punishment of failed agents and systematic administration of attacks.", "Use for continuing organization of operations; a demonic ruler as entity is BEI-HIE.", "operation", "agency|organization"),

    ("PSY-MEM", "Memory and persistent recognition", "Earthly memories, prior events and remembered elapsed years retained by encountered persons.", "Use for remembered content; a displayed life-record screen is EPI-REV.", "state", "memory|consciousness"),
    ("PSY-TIM", "Experienced duration and endlessness", "Experience of passing time, continuous fatigue and spoken awareness of a duration without relief.", "Use for subjective experience of time; comparing time in two realms belongs to EPI-CHR.", "experience", "time|consciousness"),
    ("PSY-AFF", "Fear, pain, hatred and self-appraisal", "Terror, anguish, guilt, hatred, disorientation and abrupt relief registered by a person.", "Use for psychological or felt condition; the source of pain may be ENV or OPR.", "experience", "affect|consciousness"),
    ("PSY-SPE", "Continuing speech and moral response", "Repentance pleas, declarations, blasphemy, preaching, singing or persistent deception as conscious behavior.", "Use for resident response; a spoken judicial explanation belongs to JUD.", "operation", "speech|consciousness"),
    ("PSY-COM", "Asymmetrical communication and contact", "Inability to reach, speak with, hear, or perceive someone apparently nearby.", "Use for personal connection and its lack; physical cell bars belong to CUS.", "relationship", "communication|access"),
    ("PSY-VOL", "Hope, release and perceived agency", "Loss of hope, perceived inability to escape, and felt abandonment or separation.", "Use where the resident's orientation to possible action dominates.", "state", "agency|consciousness"),

    ("JUD-GRO", "Attributed grounds of condemnation", "Faults, omissions, corruption, unforgiveness and stated earthly behavior offered as grounds for a person's condition.", "Record who alleges the grounds; do not turn witness-attributed judgments into independently established verdicts.", "assertion", "judgment|conduct"),
    ("JUD-SEV", "Severity and reciprocal recompense", "Reported differences of degree and punishments said to correspond to prior conduct or knowledge.", "Use for degree or proportional relation; the actual physical operation remains OPR.", "relationship", "judgment|proportion"),
    ("JUD-VER", "Judgments and recorded verdicts", "Direct spoken or written judgments, numbered fault categories and formal adjudication.", "Use for verdicts and classifications; the ledger as material object is CUS-LED.", "assertion", "judgment|record"),
    ("JUD-FIN", "Status of judgment and finality", "Claims about the concluded opportunity for repentance, intermediate custody and final disposition.", "Use for declared temporal judicial status; do not equate distinct afterlife stages.", "assertion", "judgment|time"),
    ("JUD-SCO", "Persons and groups under judgment", "Reports concerning ages, numbers or recognizable living and dead persons in an adjudicative setting.", "Use for population/scope claims, retaining testimony attribution for each individual case.", "assertion", "judgment|scope"),
    ("JUD-TAR", "Demonic target allocation", "Named darts, tasks and operations said to be assigned to particular earthly people or institutions.", "Use for allocation of hostile objectives, retaining distinction from divine judgment.", "relationship", "agency|targeting"),
    ("JUD-DOX", "Doctrinal inference from an experience", "General theological conclusions expressly drawn beyond the immediate objects encountered.", "Use only when the claim's content and force are those of extrapolation; examine it under Scripture separately.", "assertion", "theology|inference"),

    ("EPI-REV", "Life review and disclosed histories", "Personal histories shown by scroll, screen, revealed record or direct display.", "Use for the means of disclosure; the historical deeds shown may carry independent judgment claims.", "experience", "knowledge|history"),
    ("EPI-KNO", "Immediate and altered knowing", "Instant biographies, simultaneous viewpoints, changed awareness and privileged access to knowledge.", "Use for cognitive mode rather than the contents of the alleged information.", "experience", "knowledge|capacity"),
    ("EPI-VIS", "Open visions and unusual vantage", "Declared visions, visionary scenes, projected circles and perceptions spanning distinct positions or modes of view.", "Use when a special form of presentation, rather than ordinary walking geography, is central.", "experience", "vision|presentation"),
    ("EPI-COM", "Messages, signs and interpreted speech", "Voices, unreadable writing, identification by visible names and language not understood by the witness.", "Use for how information is addressed or withheld from the observer; its judicial contents are JUD.", "experience", "communication|knowledge"),
    ("EPI-CHR", "Cross-realm temporal discrepancy", "Different perceived durations and claims about temporal simultaneity across realms.", "Use for comparison or interpretation of temporal order, not ordinary awareness of duration.", "experience", "time|knowledge"),
    ("EPI-AID", "Aids and alterations to witnessing", "Recording implements, guide-provided illumination and other means deliberately modifying witness access.", "Use for devices or assistance to observe or preserve an account.", "operation", "witnessing|access"),
]

DIVISIONS = {
    "ENT": "Entrance and transition", "TOP": "Topography and structures",
    "ENV": "Atmosphere and perception", "BEI": "Beings and morphologies",
    "CUS": "Confinement and implements", "BOD": "Bodily composition and condition",
    "OPR": "Torment and recurring operations", "PSY": "Memory, consciousness and affect",
    "JUD": "Judicial pattern and attributed cause", "EPI": "Means of witnessing or knowing",
}

# One principal subclass per original record. This is a classification sidecar:
# every claim retains its original primary division and may take several facets.
ASSIGNMENTS = {
    "ENT-THR": "BRE-007 MEL-010 DAN-001 AZ1-001 FER-006 PUR-021 AZ3-011 PUR-035",
    "ENT-VOR": "MEL-001 MEL-012 BAX-001 BAX-002",
    "ENT-DES": "BRE-001 PER-001 AZ1-002 AZ2-001 AZ2-009 FER-001 WIE-001 KNI-001 PUR-001",
    "ENT-TRA": "ALB-001 PAR-001 APY-001 PER-013 FER-012 BAX-089",
    "ENT-EGR": "KNI-007 BAX-073 WIE-035",

    "TOP-LAN": "BRE-006 MEL-003 PAR-006 BAX-049 BRE-033 FER-010 PUR-029",
    "TOP-ROU": "BRE-019 MEL-011 BAX-019 PER-003 APY-008 WIE-019 AZ2-014",
    "TOP-PIT": "MEL-016 BAX-013 WIE-014 PUR-002 PUR-013 AZ1-009 AZ1-015 ALB-008 BAX-014",
    "TOP-CEL": "BRE-010 MEL-004 MEL-015 MEL-020 MEL-022 MEL-026 BAX-023 AZ2-005 BAX-030 MEL-029",
    "TOP-LIQ": "BRE-012 APY-002 APY-003 KNI-005 PUR-014 PUR-017 BAX-033 BAX-034 BAX-090 PUR-037 PUR-034",
    "TOP-REG": "BAX-012 MEL-025 WIE-021 WIE-029 AZ3-003 BAX-088 AZ1-012",
    "TOP-FUN": "BRE-016 AZ4-001 PAR-004 BAX-068 PAR-013 AZ1-027 AZ2-016",
    "TOP-ANA": "BAX-022 BAX-027 BAX-028 BAX-029 BAX-031 BAX-037 BAX-052 BAX-074 BAX-093 AZ3-010",
    "TOP-LIV": "BAX-076 BAX-079 PUR-012",
    "TOP-DYN": "BAX-070 ALB-011",
    "TOP-ACC": "BAX-040 BAX-075",

    "ENV-LUM": "BRE-002 MEL-002 DAN-002 BAX-010 PAR-002 ALB-003 FER-003 WIE-012 KNI-002 PUR-004 ALB-010 PAR-011 WIE-030 PUR-023",
    "ENV-THM": "PER-002 AZ1-003 WIE-016 BAX-059 BAX-085 FER-011 MEL-028",
    "ENV-OLF": "MEL-008 MEL-014 BAX-003 BAX-009 PER-005 FER-002 KNI-003 BAX-032 AZ1-014 WIE-027",
    "ENV-ACU": "BRE-004 DAN-003 BAX-008 AZ2-002 FER-008 KNI-006 AZ1-013 AZ2-013 PER-015 PUR-008 WIE-026 WIE-028 PUR-024 PUR-027 PUR-033",
    "ENV-MED": "MEL-013 BAX-006 PUR-003 PUR-007 AZ1-022 PUR-031 WIE-015",
    "ENV-PSN": "BAX-007 PER-006 WIE-007 BAX-109 BAX-110",
    "ENV-PRI": "PER-004 BRE-027 WIE-017 BAX-112",
    "ENV-KIN": "MEL-035 BRE-030",

    "BEI-SER": "BRE-005 BAX-011 AZ2-006 PAR-003 PAR-005 BAX-050 BAX-051",
    "BEI-VER": "BRE-024 BAX-018 AZ1-006 PAR-007 FER-005 PUR-009 BAX-111 WIE-033",
    "BEI-HYB": "BRE-015 MEL-006 MEL-007 PER-009 APY-004 APY-006 WIE-004 WIE-005 PUR-005 PUR-016 PUR-019 BAX-041 BAX-042 BAX-043 BAX-084 BAX-092 BAX-096 MEL-032 BAX-106 PUR-030",
    "BEI-DIS": "BRE-011 MEL-005 PER-010 BAX-107 AZ3-017 BRE-034 AZ1-029",
    "BEI-GRD": "BRE-003 BAX-021 WIE-003 WIE-022 KNI-004 PUR-015 BAX-039 BAX-057 AZ1-025 APY-011",
    "BEI-HIE": "BRE-023 AZ4-004 BAX-072 BAX-086 BAX-087 BAX-108 AZ1-017 APY-012 ALB-012",
    "BEI-ANI": "BAX-004 BAX-005 MEL-030",
    "BEI-PRE": "MEL-027",

    "CUS-ENC": "BAX-024 AZ1-004 AZ2-003 AZ4-005 WIE-002 BAX-080 MEL-034 BAX-053 BAX-060 BAX-097 AZ3-022",
    "CUS-BND": "BRE-022 PER-008 FER-007 WIE-023 BAX-035 BAX-038 BAX-077 BAX-104 AZ1-024 AZ3-014 AZ2-020 ALB-009 FER-013",
    "CUS-MRK": "AZ1-005 BAX-036 APY-009",
    "CUS-LED": "AZ4-002 APY-007 BAX-066 BAX-082",
    "CUS-OBJ": "BAX-064 BAX-026",
    "CUS-CTR": "MEL-009 PER-016 WIE-032 PUR-028 BAX-045 BRE-031",

    "BOD-SKE": "BRE-021 BAX-015 BAX-062 BAX-099 BAX-102 PUR-022",
    "BOD-SOU": "BAX-016 BAX-054 BAX-056",
    "BOD-REG": "MEL-023 PUR-010",
    "BOD-DAM": "AZ1-010 AZ2-018 AZ3-015 APY-014 PUR-025",
    "BOD-FAC": "DAN-004 WIE-008 WIE-011 BAX-081",
    "BOD-ATT": "AZ1-026 AZ2-010",

    "OPR-VIO": "BRE-017 WIE-009 WIE-010 BAX-055 BAX-078 BAX-069 AZ1-019 AZ1-020 AZ2-011 AZ3-016 WIE-031 APY-010",
    "OPR-IMM": "AZ3-006 PUR-006 PUR-020 AZ2-015 BAX-101",
    "OPR-LOP": "MEL-021 DAN-005 BAX-017 PER-007 PUR-011 PUR-018 BAX-065 BRE-035 PUR-036 BAX-025 MEL-031",
    "OPR-ENA": "BAX-044 AZ1-021 AZ2-017 AZ3-012 AZ3-018 MEL-033 BRE-032 AZ3-020 AZ3-009",
    "OPR-MOC": "AZ1-008 AZ3-019 BAX-083",
    "OPR-REM": "WIE-018 BAX-063",
    "OPR-ENV": "BAX-067 BAX-071 BAX-095 BAX-098 PUR-032 DAN-007",
    "OPR-ORG": "AZ1-028 PUR-026 AZ4-008 AZ4-006",

    "PSY-MEM": "BRE-014 BAX-020 AZ1-007",
    "PSY-TIM": "ALB-002 FER-004 WIE-020 WIE-034",
    "PSY-AFF": "DAN-009 PER-011 ALB-006 WIE-006 WIE-013 BAX-100 APY-005",
    "PSY-SPE": "BRE-025 AZ3-004 AZ3-007 BAX-046 BAX-048",
    "PSY-COM": "DAN-011 DAN-012 PAR-012 APY-013",
    "PSY-VOL": "WIE-024 BRE-028 AZ2-019",

    "JUD-GRO": "BRE-013 BRE-020 BRE-026 DAN-006 DAN-008 AZ2-004 AZ3-002 AZ3-005 AZ3-008 BAX-047 AZ3-013 AZ3-021",
    "JUD-SEV": "BRE-018 MEL-019 MEL-024",
    "JUD-VER": "ALB-005 PAR-008",
    "JUD-FIN": "ALB-007 BAX-061",
    "JUD-SCO": "AZ1-011 BRE-029 FER-009 DAN-013",
    "JUD-TAR": "AZ4-003 AZ1-018",
    "JUD-DOX": "AZ2-008 AZ3-023",

    "EPI-REV": "BRE-008 ALB-004 AZ3-001 PAR-009 AZ1-023 AZ2-012",
    "EPI-KNO": "MEL-017 MEL-018 WIE-025 WIE-036 BAX-105",
    "EPI-VIS": "BAX-091 BAX-103 BAX-094 BAX-058 PAR-010 PER-017",
    "EPI-COM": "BRE-009 AZ2-007 AZ4-007 PER-014",
    "EPI-CHR": "PER-012 DAN-014 PAR-014",
    "EPI-AID": "AZ1-016 DAN-010",
}

# A cross-reference is an additional dimension of one record, not a second
# principal class and not a claim that one category literally is another.
CROSS_REFERENCES = {
    "BRE-011": "TOP-CEL OPR-LOP",
    "BRE-017": "BOD-DAM",
    "BRE-019": "JUD-GRO ENT-DES",
    "BRE-024": "OPR-VIO",
    "BRE-025": "JUD-FIN",
    "BRE-030": "ENV-ACU",
    "BRE-031": "BOD-FAC",
    "MEL-004": "BEI-DIS",
    "MEL-020": "BEI-ANI OPR-ENA",
    "MEL-030": "TOP-CEL BEI-DIS",
    "MEL-031": "TOP-CEL",
    "DAN-004": "ENV-LUM",
    "DAN-011": "TOP-CEL",
    "BAX-016": "EPI-KNO",
    "BAX-014": "OPR-ENV",
    "BAX-025": "BEI-DIS TOP-CEL",
    "BAX-033": "OPR-ENV",
    "BAX-061": "TOP-CEL",
    "BAX-076": "ENV-KIN ENV-MED",
    "BAX-079": "TOP-CEL ENV-MED",
    "BAX-086": "OPR-ORG",
    "BAX-093": "BEI-HIE",
    "BAX-102": "BEI-VER",
    "AZ1-005": "BOD-ATT JUD-VER",
    "AZ1-009": "ENT-DES",
    "AZ1-008": "PSY-SPE",
    "AZ2-010": "CUS-MRK JUD-SCO",
    "AZ3-023": "CUS-ENC",
    "AZ2-016": "BEI-HIE",
    "APY-005": "ENV-MED",
    "ALB-010": "TOP-LIQ",
    "FER-007": "ENT-TRA",
    "WIE-033": "CUS-BND",
    "WIE-007": "EPI-KNO",
    "WIE-029": "EPI-KNO",
    "PER-016": "PSY-COM",
    "PUR-003": "BEI-VER",
    "PUR-012": "BEI-VER ENV-ACU",
    "PUR-028": "TOP-LIV",
    "PUR-036": "ENT-THR TOP-ROU",
}


def validated_records():
    with SOURCE.open(encoding="utf-8") as handle:
        source = [json.loads(line) for line in handle if line.strip()]

    by_id = {r["id"]: r for r in source}
    if len(by_id) != len(source) or len(source) != 426:
        raise ValueError("Unexpected source-register cardinality or duplicate IDs")

    classes = {row[0]: row for row in CLASSES}
    if len(classes) != len(CLASSES):
        raise ValueError("Duplicate subclass code")
    assigned = {}
    for code, raw in ASSIGNMENTS.items():
        if code not in classes:
            raise ValueError(f"Unknown subclass: {code}")
        for record_id in raw.split():
            if record_id not in by_id:
                raise ValueError(f"Unknown record: {record_id}")
            if by_id[record_id]["category"] != code.split("-")[0]:
                raise ValueError(f"Division mismatch: {record_id} / {code}")
            if record_id in assigned:
                raise ValueError(f"Record assigned twice: {record_id}")
            assigned[record_id] = code

    missing = sorted(set(by_id) - set(assigned))
    if missing:
        raise ValueError(f"Unassigned records: {missing}")
    if set(classes) != set(ASSIGNMENTS):
        raise ValueError(f"Unrepresented subclasses: {set(classes)-set(ASSIGNMENTS)}")

    cross = {}
    for record_id, codes in CROSS_REFERENCES.items():
        if record_id not in by_id:
            raise ValueError(f"Unknown cross-reference source: {record_id}")
        target_codes = codes.split()
        if assigned[record_id] in target_codes or len(set(target_codes)) != len(target_codes):
            raise ValueError(f"Invalid duplicate cross-reference for {record_id}")
        if not all(code in classes for code in target_codes):
            raise ValueError(f"Unknown cross-reference subclass for {record_id}")
        cross[record_id] = target_codes

    return source, classes, assigned, cross


def write_index(source, classes, assigned, cross):
    fields = [
        "record_id", "poe_id", "source_id", "witness", "source_line", "primary_division",
        "subclass_code", "subclass_name", "analytical_role", "facets",
        "related_subclasses", "evidence_mode", "scripture_reference",
        "scripture_correspondence", "lemma", "reported_properties",
    ]
    with INDEX.open("w", encoding="utf-8", newline="") as handle:
        out = csv.DictWriter(handle, fieldnames=fields, delimiter="\t")
        out.writeheader()
        for r in source:
            code = assigned[r["id"]]
            companion_codes = cross.get(r["id"], [])
            facets = set(classes[code][5].split("|"))
            for related in companion_codes:
                facets.update(classes[related][5].split("|"))
            out.writerow({
                "record_id": r["id"], "poe_id": r["poe_id"], "source_id": r["source_id"],
                "witness": r["source"], "source_line": r["source_line"],
                "primary_division": r["category"], "subclass_code": code,
                "subclass_name": classes[code][1], "analytical_role": classes[code][4],
                "facets": "|".join(sorted(facets)),
                "related_subclasses": "|".join(companion_codes),
                "evidence_mode": r["evidence_mode"],
                "scripture_reference": r["biblical_cross_reference"],
                "scripture_correspondence": r["correspondence"],
                "lemma": r["lemma"],
                "reported_properties": r["reported_properties"],
            })


def write_architecture(source, classes, assigned, cross):
    by_class = defaultdict(list)
    for r in source:
        by_class[assigned[r["id"]]].append(r)

    counts = Counter(assigned.values())
    kinds = Counter(classes[code][4] for code in assigned.values())
    labels = {"O": "observation", "F": "felt/sensory", "H": "heard", "K": "privileged knowledge", "S": "attributed speech", "I": "interpretation"}

    lines = [
        "# Atlas of Perdition: Taxonomic Architecture",
        "",
        "**Second-order working edition:** 16 November 2026",
        f"**Coverage:** {len(source)} existing phenomena; {len(DIVISIONS)} conserved primary divisions; {len(CLASSES)} defined subclasses; {len(cross)} explicit cross-dimensional records.",
        "",
        "## Governing distinction",
        "",
        "The catalogue records phenomena as reported in the supplied testimony compilation. Each record has one stable identifier and one principal subclass. A phenomenon can also bear properties, enact operations, participate in relationships, and become accessible through a particular mode of witnessing. These dimensions may cross class boundaries; they do not justify multiplying the source event into unrelated facts.",
        "",
        "This architecture is a **classification of reported material**, not a physical reconstruction of all regions as one measurable map. Names, occupants, distances, places and mechanisms remain attached to their own reports. Spoken explanation by a guide, sight, felt experience, instantaneous knowledge and narrator inference retain their separate standings.",
        "",
        "The existing *Phenomena Register* and its record IDs are unchanged. The companion *Second-Order Index* assigns a subtype and preserves the original line reference, evidence mode and scriptural correspondence for every record.",
        "",
        "## Structure and use",
        "",
        "1. **Primary division** identifies the principal field in which the existing register filed a phenomenon. These ten codes remain stable.",
        "2. **Subclass** identifies the most specific recurring kind or operation warranted at this stage. It is one principal code per existing record.",
        "3. **Analytical role** identifies whether the subclass currently foregrounds an entity, property, operation, state, relationship, experience or assertion. It characterizes the *focus of analysis*, not the complete nature of the referent.",
        "4. **Facets** register intersecting concerns such as substance, animation, bodily effect, sound, time, access, or custody. The generated Index derives facets from the principal subclass and any explicitly curated cross-references.",
        "5. **Related subclasses** show a second legitimate analytical approach to selected compound records without changing the principal filing.",
        "6. **Evidence and scriptural modes** are inherited verbatim. O/F/H/K/S/I denote observation, sensation, hearing, immediate knowledge, attributed speech, and interpretation; D/P/A/E denote direct scriptural description, principle, analogy, and testimony-specific extension.",
        "",
        "## Division summary",
        "",
        "| Primary division | Records | Subclasses |",
        "|---|---:|---:|",
    ]

    for division, label in DIVISIONS.items():
        relevant = [code for code in classes if code.startswith(division + "-")]
        lines.append(f"| {division} — {label} | {sum(counts[c] for c in relevant)} | {len(relevant)} |")

    lines.extend(["", "## The second-order classes", ""])
    for division, label in DIVISIONS.items():
        lines.extend([f"### {division} — {label}", "", "| Code · subclass | Entries | Definition and boundary | Source examples |", "|---|---:|---|---|"])
        for code, name, definition, boundary, kind, facets in CLASSES:
            if not code.startswith(division + "-"):
                continue
            example_records = by_class[code]
            if len(example_records) <= 2:
                selected = example_records
            else:
                selected = [example_records[0]]
                second = next((r for r in example_records[1:] if r["source_id"] != selected[0]["source_id"]), example_records[1])
                selected.append(second)
            examples = "; ".join(f"{r['id']} (*{r['lemma']}*)" for r in selected)
            lines.append(f"| **{code}** · {name} | {counts[code]} | {definition} **Boundary:** {boundary} | {examples} |")
        lines.append("")

    lines.extend([
        "## Intersecting dimensions",
        "",
        "The subtype is the object's principal taxonomic home. The other dimensions are searchable relations. For example:",
        "",
        "| Record | Principal subclass | Further relations | Why the distinction matters |",
        "|---|---|---|---|",
        "| BAX-076 · breathing living walls | TOP-LIV | ENV-KIN; ENV-MED | Wall = structure; movement and material resemblance are properties. Nothing in the sight alone proves that the wall is a separate spirit. |",
        "| MEL-030 · cell props are demons | BEI-ANI | TOP-CEL; BEI-DIS | Furnishings are described as living agents within the prison scene; the object/creature identity is peculiar to this account. |",
        "| PUR-012 · insect-composed walls | TOP-LIV | BEI-VER; ENV-ACU | Architecture, fauna and clicking sounds coincide in one observed substrate. |",
        "| BRE-011 · woman changes form | BEI-DIS | TOP-CEL; OPR-LOP | The transformed person, her cell, and the repeated punitive event have separate analytical roles. |",
        "| AZ1-005 · plate and forehead number | CUS-MRK | BOD-ATT; JUD-VER | Material sign and its judicial import differ; Revelation 13 does not on its own assign 666 to every infernal resident. |",
        "| DAN-011 · isolated residents | PSY-COM | TOP-CEL | Inability to communicate is not equivalent to being behind visible bars. |",
        "| PUR-036 · river course resets | OPR-LOP | ENT-THR; TOP-ROU | A repeating path may resemble an exit threshold while the witnessed operation resets the route. |",
        "",
        "A future entry may need additional related codes. Such references should be added only where the passage supplies the relation, not because two ideas can be associated abstractly.",
        "",
        "## Relations available for the atlas",
        "",
        "The Index supports a further relational layer without requiring it to become part of the subclass name. Useful predicates include *located within*, *part of*, *connects to*, *contains*, *composed of*, *resembles*, *acts upon*, *restrains*, *guards*, *utters*, *perceived by*, *attributed to*, *repeats*, *restores after*, *assigned to*, and *associated by the witness with*. Each predicate should preserve its source passage and manner of assertion.",
        "",
        "## Stability and known boundaries",
        "",
        "- **Preserved:** ten divisions, all 426 record IDs, source lines, original descriptions, mode of knowledge, witness attribution and biblical links.",
        "- **Refined:** subclass membership and cross-cutting facets. This scheme can accept new witnesses without changing an established witness's words.",
        "- **Not merged:** Baxter's human-shaped region, Melvin's circular tiers, and Purser's pit grid; each remains source-specific.",
        "- **Not equated:** literal soundscape and total silence; dark conditions with visible flame and apparent flame without illumination; waterlessness and the presence of destructive liquid fire.",
        "- **Not inferred:** agreement between two motif descriptions as proof of identical location, independent origin, or warrant for every detailed theological conclusion.",
        "- **Known editorial overlap:** several initial records foreground an operation while originally filed under a place or a bodily object. Their primary divisions have been retained for identifier stability; their related facets disclose the additional role.",
        "- **Expansion policy:** a genuinely new feature should first be tested against a current subclass; introduce a new subclass when its defining identity cannot be expressed as an existing subclass plus facets or relations.",
        "",
        "## Source treatment",
        "",
        "The supplied text contains first-person accounts, excerpts, collecting notes and editorial headings. No external edition, translation pedigree or online publication is required for this classification. Witness names, alleged occupants, conversations and explanations are held as information reported by their respective accounts. Scripture is treated as distinct authoritative testimony and cross-referenced according to the precise feature it supports; resemblance to a verse does not transform every source detail into a biblical proposition.",
        "",
        "## Machine-readable companion",
        "",
        "`Atlas_of_Perdition_Second_Order_Index.tsv` has one row for each original phenomenon. Principal subclass codes resolve against the tables above. `related_subclasses` is a pipe-separated set of curated additional views; `facets` is the resulting pipe-separated analytical index. Counts are records, not unique witnesses or proof of independent corroboration.",
        "",
    ])
    ARCHITECTURE.write_text("\n".join(lines), encoding="utf-8")
    print(f"Created {ARCHITECTURE.name} and {INDEX.name}: {len(source)} records, {len(classes)} subclasses, {len(cross)} cross-referenced records")
    print("Role distribution:", dict(sorted(kinds.items())))
    print("Division record counts:", {d: sum(counts[c] for c in classes if c.startswith(d + '-')) for d in DIVISIONS})


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--views", action="store_true", help="Also generate readable taxonomy report")
    args = parser.parse_args()
    original, classbook, mapping, references = validated_records()
    write_index(original, classbook, mapping, references)
    if args.views:
        write_architecture(original, classbook, mapping, references)


