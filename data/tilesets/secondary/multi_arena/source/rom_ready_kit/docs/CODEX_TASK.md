# CODEX: INTEGRATE FIRE RED PVP TOWN ASSETS

You are working inside the user's game repository. Inspect the project first. It may be pret/pokefirered or another engine. Never assume or overwrite existing map resources blindly.

1. Identify map engine, current town map ID, primary/secondary tilesets, palette allocation, metatile structures, movement collision/behaviors, warp/event formats, and build procedure.
2. Use `data/manifest.json` and `gfx/objects/*.png` (indexed) or `.4bpp` plus `.gbapal` raw files. For GBA raw 4bpp: 8×8 tiles, 32 bytes each, linear tile order, low nibble first, palettes 16 LE BGR555 entries (index 0 transparent).
3. Import the art into the engine using its standard resource pipeline. Consolidate object palettes to meet actual palette-bank and tile-count limits. Do not assume one independently loaded palette per building is possible.
4. Assemble **16×16 metatiles** with suitable layers, passability, priorities, shadow/roof occlusion, and entrance warps; choose correct collision footprints (front door walkable and warp trigger, building bases blocked).
5. Preserve current map geometry where practical, but follow `gfx/reference/target_concept.png` for layout: large arena north, monumental approach/statues, central fountain with 4 benches, colorful houses, flowerbeds and hedges around paths, clearly connected entrances, three coastal docks, shoreline and stairs.
6. Integrate the fountain's four 48×64 frames if the engine supports animated metatiles; otherwise use first frame and explain why. Animations must not change blocking behavior or stone silhouette.
7. Keep a broad unobstructed main north-south axis and walking loops around fountain. Do not cover a door with a fence or bed. Mark water and cliffs impassable unless explicitly surfable/climbable. Validate path connectivity from south entrance to arena, all shops and houses.
8. Run the project's existing asset converters/build, fix palette/tilecount errors and demonstrate game loads map. Never claim compile success without testing.
9. Provide file changes, screenshots of integrated map and an explicit remaining-work list; if repository or engine sources are missing, stop before pretending integration succeeded.

The reference PNG is a **visual goal only**, not a tilemap/ROM asset. Avoid flattening it and importing it as a giant background image.
