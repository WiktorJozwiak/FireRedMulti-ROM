# Reference arena district

The map now uses its own primary and secondary tilesets. Buildings, trees,
paving, fences, benches, lamps, statue, gardens, shoreline and bridge assets
were extracted from the owner's image `Symetryczne miasto areny nad wod�.png`.
Colosseum and fountain also use the separately supplied PNG artwork.
Original user files remain unchanged. Native-resolution indexed sources are
in `source/reference`. GBA transparent color is index zero.

1007 of 1024 background tile slots; 13 independent 15-color palettes.
Primary bank: 640 tiles; secondary bank: 384 slots. Native General/Cerulean
terrain is not used by this district. Other maps retain their own tilesets.
The fountain rim is stable; only its blue water pixels animate.

Map 48x36. Cerulean bridge arrival (6,12), exit x=1/y=11..12.
Doorways: supplies (14,14), center (33,14), rewards (37,25),
colosseum (24,4). Return from colosseum (24,5).

The earlier imagegen decorations in source/bench.png, lamp.png and statue.png
are retained as unused variants. The current map uses the reference crops.

Supplied sheets are preserved in source/supplied. Clean house sprites replace
red houses, the blue hall, green house and gold rewards vendor; grass and
paving are taken from the supplied terrain sheet. Other sheets are retained
for further refinement.

