#!/usr/bin/env python3
"""Mechanical, full-file lexical reconnaissance for Atlas of Perdition.

This index locates candidates. It does not itself establish that a word denotes
an observed infernal feature: quotation, exposition, and editorial material can
also contain the same terms.
"""

import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT.parent / "testimonies" / "_intake" / "Experiences_1.txt"
OUTPUT = ROOT / "atlas_lexical_concordance.csv"

# Inclusive line spans in the attached compilation, from its dated sections.
SECTIONS = [
    ("IDX", "Opening name index", 1, 305),
    ("DAN", "Daniel Ekechukwu: long account", 306, 349),
    ("BAX", "Mary K. Baxter: A Divine Revelation of Hell", 350, 2008),
    ("MEL", "Bryan Melvin", 2009, 2042),
    ("PER", "Jennifer Perez", 2043, 2145),
    ("TAH", "Akef Tayem: biographical summary", 2146, 2177),
    ("ALS", "Aline Baxley: summary", 2178, 2225),
    ("ALB", "Aline Baxley: first-person text", 2226, 2281),
    ("AZS", "Angelica Zambrano: summaries", 2282, 2337),
    ("AZ1", "Angelica Zambrano: experience one", 2338, 2813),
    ("AZ2", "Angelica Zambrano: experience two", 2814, 3034),
    ("AZ3", "Angelica Zambrano: experience three", 3035, 3383),
    ("AZ4", "Angelica Zambrano: experience four", 3384, 3545),
    ("BRE", "Carmelo Brenes", 3546, 3617),
    ("PAR", "Young Moon Park", 3618, 3671),
    ("AP0", "Athet Pyan: heading only", 3672, 3675),
    ("APY", "Athet Pyan Shinthaw Paulu", 3676, 3775),
    ("BF0", "Bernarda Fernandez: heading only", 3776, 3779),
    ("FER", "Bernarda Fernandez", 3780, 3851),
    ("BW0", "Bill Wiese: heading only", 3852, 3855),
    ("WIE", "Bill Wiese", 3856, 4194),
    ("KNI", "Carl Knighton", 4195, 4248),
    ("DA2", "Daniel Ekechukwu: alternate summary", 4249, 4303),
    ("PUR", "Aaron Purser", 4304, 4474),
]

TAGS = {
    "entry.tunnel": r"\btunnels?\b",
    "entry.vortex": r"\b(?:vortex(?:es)?|funnels?|tornado(?:es)?|whirlwinds?)\b",
    "entry.gate": r"\b(?:gates?|doorways?|portals?)\b",
    "entry.descent": r"\b(?:descend(?:ed|ing)?|fell|falling|dropped|downward)\b",
    "terrain.cell": r"\b(?:cells?|chambers?|dungeons?|prison(?:s)?)\b",
    "terrain.pit": r"\b(?:pits?|abyss|bottomless|recess(?:es)?)\b",
    "terrain.cave": r"\b(?:caves?|caverns?)\b",
    "terrain.road": r"\b(?:roads?|streets?|paths?)\b",
    "terrain.waterway": r"\b(?:rivers?|lakes?|streams?|lagoon(?:s)?)\b",
    "terrain.mountain": r"\b(?:mountains?|volcano(?:es)?|valleys?|hills?)\b",
    "terrain.wall": r"\b(?:walls?|ledges?|bars?)\b",
    "terrain.level": r"\b(?:tiers?|levels?|regions?|sections?)\b",
    "sense.darkness": r"\b(?:dark(?:ness)?|black(?:ness)?|dim(?:ness)?)\b",
    "sense.heat": r"\b(?:hot|heat|burning|fire|flames?|lava|brimstone|sulfur|sulphur)\b",
    "sense.cold": r"\b(?:cold|freezing|icy)\b",
    "sense.dry": r"\b(?:dry|arid|thirst(?:y)?)\b",
    "sense.odor": r"\b(?:smells?|odor|odour|stench|stink|putrid|rotten)\b",
    "sense.sound": r"\b(?:screams?|shriek(?:s|ing)?|moans?|groans?|wailing|laughter|roar(?:ing)?)\b",
    "sense.heightened": r"\b(?:senses?|sensitive|keen(?:er)?)\b",
    "entity.demon": r"\b(?:demons?|devils?|evil spirits?|entities)\b",
    "entity.serpent": r"\b(?:serpents?|snakes?|reptil(?:e|ian)|lizards?)\b",
    "entity.insect": r"\b(?:worms?|spiders?|insects?|bugs?|beetles?|flies|cockroaches?|scorpions?)\b",
    "entity.hybrid": r"\b(?:hoofs?|hooves|horns?|claws?|fangs?|wings?|talons?)\b",
    "custody.chain": r"\b(?:chains?|shackles?|ropes?|tied|bound|locks?|keys?)\b",
    "custody.label": r"\b(?:plaques?|plates?|mark(?:ed)?|666|numbered|inscriptions?)\b",
    "body.bones": r"\b(?:skeletons?|bones?|skulls?|ribs?)\b",
    "body.flesh": r"\b(?:flesh|skin|blood|limbs?|eyes?|tongues?)\b",
    "body.mist": r"\b(?:mists?|vapors?|souls?)\b",
    "process.regrow": r"\b(?:regenerat(?:ion|e|es|ed|ing)|grew back|grow back|restor(?:e|ed)|all over again)\b",
    "process.violence": r"\b(?:stabb(?:ed|ing)?|pierc(?:e|ed|ing)|torn|tear|ripped|crush(?:ed|ing)?|tortur(?:e|ed|ing))\b",
    "process.deceive": r"\b(?:deceiv(?:e|ed|ing)|mirages?|illusions?|morph(?:ed|ing)?|change(?:d|s)? forms?)\b",
    "process.moral": r"\b(?:sin|transgression|judg(?:e|ment)|punish(?:ment)?|recompense|repay)\b",
    "affect.memory": r"\b(?:remember|memory|memories|regret|remorse|conscience)\b",
    "affect.hopeless": r"\b(?:hopeless|no hope|too late|no way out|forever|eternity)\b",
    "affect.mercy": r"\b(?:mercy|forgiv(?:e|eness)|repent(?:ance)?)\b",
}


def main():
    lines = SOURCE.read_text(encoding="utf-8-sig").splitlines()
    assert len(lines) == 4474, f"Input changed: {len(lines)} lines"
    patterns = {name: re.compile(pat, re.I) for name, pat in TAGS.items()}
    rows = []
    for sid, title, start, stop in SECTIONS:
        block = lines[start - 1 : stop]
        for tag, pattern in patterns.items():
            found = []
            for n, line in enumerate(block, start):
                hits = len(pattern.findall(line))
                if hits:
                    found.append((n, hits))
            if found:
                rows.append(
                    {
                        "source_id": sid,
                        "source": title,
                        "tag": tag,
                        "occurrences": sum(hit for _, hit in found),
                        "distinct_lines": len(found),
                        "line_numbers": ";".join(str(n) for n, _ in found),
                    }
                )
    with OUTPUT.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=["source_id", "source", "tag", "occurrences", "distinct_lines", "line_numbers"])
        writer.writeheader()
        writer.writerows(rows)
    print(f"Scanned every line: {len(lines)}; section spans: {len(SECTIONS)}; lexical index rows: {len(rows)}")
    print(f"Saved {OUTPUT}")


if __name__ == "__main__":
    main()
