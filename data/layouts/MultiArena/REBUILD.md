# PvP town ROM-ready integration � 2026-10-12

Engine: pret/pokefirered. MAP_MULTI_ARENA, native 48x42 metatiles (16x16).
Primary gTileset_MultiArenaPrimary (640 tiles), secondary gTileset_MultiArena
(384 tiles). 4bpp graphics; two-layer 8-entry metatiles; 32-bit behavior attrs.
Native map.json events; 0x69 door behavior and elevation3 walkable approaches.

Rebuild: PYTHONUTF8=1 python tools/build_multi_arena.py (Pillow).
Import provenance: data/tilesets/secondary/multi_arena/source/rom_ready_kit.
The supplied PNGs are used, palette groups consolidated to 13 banks of 16.
979/1024 tiles, 355 metatiles. Raw kit formats validated (17 asset triplets).
Original raw sources retained; final graphics go through the native converters.

Imported colosseum, houses, reward shop, statue and fountain. Native FireRed
terrain, Mart and Pokemon Center preserved. Approved deeper flower borders and
full-size lamps/benches retained (kit props have excessive empty padding).
Added hedges in grass plots; broad fountain loops and three coastal piers.
Side terrace stairs remain removed at the owner's request. Colosseum front
steps retained. The reference is not flattened into a map background.

Fountain: dedicated 64-tile VRAM range, four frames every12 game frames.
Only blue water pixels change. Stone and alpha mask retain frame0 geometry;
blocking behavior is identical throughout. No shared scenery tiles animated.

All 11 building doors are walkable, 0x69 and have valid matching return warps.
Seven previously decorative residences now have distinct map identities,
shared native house layout and independently correct return destinations.
Main west Cerulean entrance preserved; south/east piers scenic, not new world
connections. All door approaches, NPCs and south pier reachable statically.

Source recipe and collision export: source_layers.json. Validation reports:
validation.json and integration-checks.json. Preview files1x/2x use nearest
neighbor only for display. Build verified by GitHub Actions. Emulator checks use a separate local QA save.

Green residence removed (7955b42); its old map ID stays reserved for save compatibility.
Overworld art uses COVERED layers (7c40fe0), keeping pavement below player/NPC sprites.
Emulator smoke test (7c40fe0): player/NPC visibility and movement PASS; House7 and House5 enter/return PASS. All11 door approaches and matching return warps PASS statically. Local isolated walkthrough: http://127.0.0.1:3113/walk (Z=A, X=B, arrows=movement).
