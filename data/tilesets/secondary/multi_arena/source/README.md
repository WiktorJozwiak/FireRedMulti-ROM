# Arena district art

Colosseum and fountain supplied by the project owner as PNG source artwork.
Normalized to native GBA resolution: colosseum 160x96, fountain 48x64.
Transparency is palette index zero. Original download files are unchanged.

Bench (32x16), lamp (16x48), statue (32x48) generated with built-in imagegen,
then converted to a shared 15-color palette for GBA tile encoding.
Prompt: Three isolated overworld pixel-art assets, Pokemon FireRed style:
wooden park bench, dark navy street lamp with cream glass, gray dragon statue
on stone pedestal. Transparent background, front three-quarter top-down view,
coarse readable pixels, no ground or text.

The packed secondary tileset uses 347 of 384 tile slots. Building art uses
palette 9, fountain palette 10, decorations palette 11. Native roofs use
palette 12 and their red variant palette 7. Fountain rim stays fixed; only
blue water pixels change across the four animation frames.

Main map: 56x48. Entry from Cerulean: (6,25), exit west: x=2,y=24..26.
Colosseum doorway: (28,7), return from colosseum: (28,8).
