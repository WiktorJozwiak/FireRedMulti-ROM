# FireRed ROM integration pack – instrukcja

Ta paczka zawiera **rzeczywiste pliki binarne GBA 4bpp**, indeksowane PNG i palety BGR555 do importu. Nie jest to gotowy patch ROM-u ani gotowa mapa `.map`: bez repozytorium i wiedzy o silniku nie da się poprawnie dodać metatiles, kolizji, eventów i map connections.

## Zawartość
- `gfx/objects/`: budynki, fontanna, dekoracje – PNG P-indexed, `.4bpp` i `.gbapal`.
- `gfx/terrain/terrain_atlas_128x80.*`: 40 kafelków 16×16 jako referencyjny atlas do rozłożenia na 8×8.
- `gfx/reference/`: aktualna mapa i obraz docelowy.
- `data/manifest.json`: dokładne wymiary i pliki.
- `docs/CODEX_TASK.md`: zadanie do przekazania Codexowi.

**Ważne:** generator obrazów nie daje prawdziwego pixel-perfect 16×16 z założenia; tekstury zostały przeskalowane metodą nearest neighbour, skwantyzowane do maksymalnie 15 widocznych kolorów + przezroczystość, ale wymagana jest inspekcja artystyczna po imporcie. Fontanna ma wspólną geometrię we wszystkich 4 klatkach, a animacja jest prostą zmianą pikseli wody. Indywidualne palety trzeba scalić do banków docelowego silnika.
