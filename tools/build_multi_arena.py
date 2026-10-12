"""Deterministic, native-resolution arena layout and GBA tileset exporter.

Run from the ROM repository root using Python + Pillow. No art resampling.
Source layer recipe and validation report are exported alongside map.bin.
"""
from pathlib import Path
from PIL import Image, ImageDraw
import json, struct, collections

ROOT=Path(__file__).resolve().parents[1]
SECOND=ROOT/'data/tilesets/secondary/multi_arena'
PRIMARY=ROOT/'data/tilesets/primary/multi_arena'
PACK=SECOND/'source/asset_pack'
OUT=SECOND/'source/rebuilt'
OUT.mkdir(parents=True,exist_ok=True)
W,H=48,42
assets={}
def load(name,file,pal,folder='objects'):
    im=Image.open(PACK/folder/file).convert('RGBA')
    assert im.width%8==0 and im.height%8==0,(file,im.size)
    assets[name]=(im,pal)
for name,file,pal in [
 ('arena','arena_colosseum_192x112.png',3),
 ('blue','house_blue_80x80.png',4),('red','house_red_80x80.png',5),
 ('green','house_green_80x80.png',6),('yellow','house_yellow_80x80.png',7),
 ('rewards','shop_rewards_96x80.png',8),('fountain','fountain_base_48x64.png',2),
 ('bench','bench_32x16.png',9),('lamp','lamppost_16x32.png',9),
 ('statue','statue_32x48.png',9),('flowers','flowerbed_32x32.png',0)]:load(name,file,pal)
for f in sorted((PACK/'tiles').glob('*.png')):
    n=f.stem.replace('_16x16','')
    load(n,f.name,2 if n.startswith(('water','coast','cliff')) else 1 if n.startswith(('pavement','path','fence','stairs','wood')) else 0,'tiles')
# Native-pixel refinement of simplified pine silhouettes: layered crowns,
# individual branch highlights, dark outer edges and complete visible trunks.
for i in range(3):
    im=Image.open(PACK/'objects'/f'tree_pine_{i+1}_32x48.png').convert('RGBA')
    d=ImageDraw.Draw(im);dark=(29,66,36,255);mid=(49+5*i,106+4*i,43,255);light=(100+4*i,154,63,255)
    for cy,half in [(7,6),(15,9),(24,12),(33,14)]:
        d.polygon([(16,cy-6),(16-half,cy+7),(16+half,cy+7)],fill=dark)
        d.polygon([(16,cy-4),(18-half,cy+5),(14+half,cy+5)],fill=mid)
        for bx in range(17-half,16+half,5):d.line([(bx,cy+3),(bx+2,cy)],fill=light,width=1)
    d.rectangle((14,40,18,46),fill=(111,77,47,255));d.line((14,40,14,46),fill=(164,119,65,255))
    assets[f'tree{i}']=(im,0)
# Refined rocky shore, keeping each supplied 16px tile at native size.
for i in range(2):
    im=assets[f'cliff_{i}'][0].copy();d=ImageDraw.Draw(im)
    d.line([(0,1),(15,1)],fill=(172,143,99,255));d.line([(0,14),(15,14)],fill=(74,61,58,255))
    for x in range(i*3,16,6):
        d.line([(x,3),(x+2,7),(x,13)],fill=(102,79,62,255));d.line([(x+3,3),(x+4,8)],fill=(158,123,84,255))
    assets[f'cliff_{i}']=(im,2)
# Larger native-pixel bench/lamp/statue silhouettes, correcting padding in
# supplied PNGs without stretching them. These stay inside original canvases.
im=Image.new('RGBA',(32,16));d=ImageDraw.Draw(im)
d.rectangle((1,1,30,10),fill=(47,63,83));d.rectangle((3,2,28,8),fill=(165,112,61))
for y in [4,7]:d.line((3,y,28,y),fill=(97,67,45))
d.rectangle((3,11,5,15),fill=(47,63,83));d.rectangle((26,11,28,15),fill=(47,63,83));assets['bench']=(im,9)
im=Image.new('RGBA',(16,32));d=ImageDraw.Draw(im)
d.rectangle((6,8,9,29),fill=(39,66,106));d.rectangle((3,28,12,31),fill=(40,65,97))
d.polygon([(5,1),(10,1),(13,5),(12,12),(9,16),(6,16),(3,12),(2,5)],fill=(32,54,89))
d.rectangle((5,5,10,11),fill=(255,235,171));d.line((5,4,10,4),fill=(145,178,203));assets['lamp']=(im,9)
# Keep provided statue, but remove only aligned empty padding for its base.
stat=assets['statue'][0]; im=Image.new('RGBA',(32,48));im.alpha_composite(stat,(0,-8));d=ImageDraw.Draw(im)
d.rectangle((5,35,28,45),fill=(86,104,127));d.rectangle((7,36,26,42),fill=(151,164,176));d.line((5,45,28,45),fill=(51,68,90));assets['statue']=(im,9)
# Previously prepared native-sized reference crowns are more faithful than
# triangular placeholder pines. Reuse their pixels without resampling.
treeSource=SECOND/'source/reference/tree.png'
for i in range(3):
    im=Image.open(treeSource).convert('RGBA')
    im.putdata([(min(255,int(r*(1+i*.035))),min(255,int(g*(1+i*.025))),b,a) for r,g,b,a in im.getdata()])
    assets[f'tree{i}']=(im,0)
assets['statue']=(Image.open(SECOND/'source/reference/statue.png').convert('RGBA'),9)
# Refine the fountain on its native 48x64 canvas: a broad octagonal basin,
# thick stable stone rim, central jet and discrete rings of water pixels.
im=Image.new('RGBA',(48,64));d=ImageDraw.Draw(im)
d.polygon([(11,23),(36,23),(47,33),(47,48),(36,61),(11,61),(0,48),(0,33)],fill=(49,68,96))
d.polygon([(11,24),(36,24),(46,34),(46,46),(35,57),(12,57),(1,46),(1,34)],fill=(205,198,164))
d.polygon([(12,28),(35,28),(42,35),(42,44),(34,52),(13,52),(5,44),(5,35)],fill=(29,112,209))
d.line([(12,30),(34,30),(40,36)],fill=(77,175,242))
for yy,xx in [(37,12),(43,10),(47,17)]:
    d.line([(xx,yy),(xx+4,yy+2),(43-xx,yy+2),(47-xx,yy)],fill=(162,228,250))
d.polygon([(20,36),(20,17),(22,17),(22,5),(24,1),(26,6),(26,19),(28,19),(28,36),(26,41),(22,41)],fill=(139,223,253))
d.line([(24,6),(24,34)],fill=(246,254,255),width=2);d.line([(17,39),(20,43),(28,43),(32,39)],fill=(222,250,255),width=2)
assets['fountain']=(im,2)
for i in range(2):
    im=assets[f'water_{i}'][0].copy();d=ImageDraw.Draw(im)
    for x,y in [(1,3),(8,10),(12,1)]:d.line([(x,y),(x+2,y+1),(x+4,y)],fill=(76,173,234))
    assets[f'water_{i}']=(im,2)
# Dense flower borders: preserve native 16px dimensions, add a continuous
# hedge outline and alternate red/white blossoms instead of sparse dots.
for name,(src,pal) in list(assets.items()):
    if name.startswith('flowerbed_'):
        im=assets['grass_0'][0].copy();d=ImageDraw.Draw(im)
        d.rectangle((1,1,14,14),fill=(42,99,45));d.line((2,1,13,1),fill=(107,161,70));d.line((1,2,1,13),fill=(107,161,70))
        for k,(x,y) in enumerate([(5,5),(11,10),(4,12)]):
            c=(240,74,47) if k!=1 else (247,241,205)
            d.rectangle((x-1,y-2,x+1,y+2),fill=c);d.rectangle((x-2,y-1,x+2,y+1),fill=c);d.point((x,y),fill=(250,209,78))
        assets[name]=(im,0)
# Rock faces and grass lips use the already prepared native 16px source.
shore=Image.open(SECOND/'source/reference/shore.png').convert('RGBA')
for i in range(2):
    im=shore.copy();d=ImageDraw.Draw(im);d.line((0,0,15,0),fill=(110,165,85));assets[f'cliff_{i}']=(im,2)
for direction in ['n','s','e','w','se','sw','ne','nw']:
    im=assets['water_0'][0].copy();d=ImageDraw.Draw(im)
    pts={'s':[(0,0),(15,0),(15,11),(0,11)],'n':[(0,5),(15,5),(15,15),(0,15)],'e':[(0,0),(10,0),(10,15),(0,15)],'w':[(5,0),(15,0),(15,15),(5,15)],'se':[(0,0),(9,0),(12,7),(8,12),(0,12)],'sw':[(6,0),(15,0),(15,12),(7,12),(3,7)],'ne':[(0,4),(8,4),(12,9),(9,15),(0,15)],'nw':[(7,4),(15,4),(15,15),(6,15),(3,9)]}[direction]
    d.polygon(pts,fill=(118,92,72));d.line(pts+[pts[0]],fill=(197,176,131),width=1)
    for xx,yy in [(3,5),(8,9),(12,4)]:
        if im.getpixel((xx,yy))[:3]==(118,92,72):d.line((xx,yy,xx,yy+3),fill=(84,69,61))
    if 's' in direction:d.line((0,0,15 if direction=='s' else 8,0),fill=(104,159,79),width=3)
    assets['shore_'+direction]=(im,2)
for i in range(3):
    im=Image.new('RGBA',(32,48));d=ImageDraw.Draw(im)
    d.rectangle((13,36,18,46),fill=(105,75,48));d.line((14,38,14,45),fill=(162,119,66))
    dark=(28,64,40);mid=(53+i*3,108+i*4,48);light=(98+i*3,151+i*3,65)
    outline=[(15,0),(20,5),(23,11),(28,17),(29,24),(31,31),(28,37),(22,41),(10,41),(3,37),(0,31),(2,23),(5,16),(9,11),(11,5)]
    d.polygon(outline,fill=dark)
    for cx,cy,rx,ry in [(15,12,8,10),(10,23,8,10),(21,23,8,10),(8,32,6,7),(16,32,8,8),(25,32,5,6)]:
        d.ellipse((cx-rx,cy-ry,cx+rx,cy+ry),fill=mid)
        d.arc((cx-rx+1,cy-ry+1,cx+rx-2,cy+ry-3),180,285,fill=light,width=2)
    for x,y in [(12,8),(17,16),(7,22),(21,26),(12,30),(20,35)]:
        d.line((x,y,x+2,y-2),fill=light);d.line((x,y+3,x+3,y+1),fill=dark)
    assets[f'tree{i}']=(im,0)
for i in range(4):
    im=assets[f'grass_{i}'][0].copy();d=ImageDraw.Draw(im)
    for x,y in [(3+i%2,4),(11,11-i%2)]:
        d.line([(x-2,y-2),(x,y),(x+2,y-2)],fill=(90,149,80));d.point((x+1,y+2),fill=(142,190,111))
    assets[f'grass_{i}']=(im,0)
for i in range(3):
    assets[f'tree{i}']=(Image.open(treeSource).convert('RGBA'),10)
for name,(im,pal) in list(assets.items()):
    if name.startswith('grass_'):assets[name]=(im,11)
    if name.startswith('water_'):assets[name]=(im,12)
native=SECOND/'source/native'
for i in range(3):assets[f'tree{i}']=(Image.open(native/'tree.png').convert('RGBA'),10)
for i in range(4):assets[f'grass_{i}']=(Image.open(native/'grass.png').convert('RGBA'),11)
for i in range(2):assets[f'water_{i}']=(Image.open(native/'water.png').convert('RGBA'),12)
im=Image.open(native/'mart.png').convert('RGBA');ImageDraw.Draw(im).rectangle((64,0,79,63),fill=(0,0,0,0));assets['mart']=(im,4)
assets['center']=(Image.open(native/'center.png').convert('RGBA'),8)
# Stage2: native-pixel material shading. Keep the approved FireRed terrain
# and native service buildings unchanged; refine only new artwork.
for name in ['blue','red','green','yellow','rewards','statue']:
    im,pal=assets[name];im=im.copy();src=im.copy()
    for y in range(im.height):
        for x in range(im.width):
            r,g,b,a=src.getpixel((x,y))
            if a<=128:continue
            light=1.07-.09*x/max(1,im.width-1)-.06*y/max(1,im.height-1)
            # Emphasize existing eave, sill and masonry shadows.
            if max(r,g,b)<115:light-=.06
            im.putpixel((x,y),(min(255,int(r*light)),min(255,int(g*light)),min(255,int(b*light)),a))
    assets[name]=(im,pal)
for i in range(3):
    im=assets[f'pavement_{i}'][0].copy();d=ImageDraw.Draw(im)
    d.line((1,1,7,1),fill=(222,213,187));d.line((1,2,1,7),fill=(219,209,181))
    d.line((1,7,7,7),fill=(194,188,165));d.line((7,2,7,7),fill=(198,191,166))
    d.line((9,9,15,9),fill=(221,211,184));d.line((9,15,15,15),fill=(194,188,165))
    for x,y in [[(4,4),(12,12)],[(5,3),(11,13)],[(3,5),(13,11)]][i]:
        d.point((x,y),fill=(198,190,163));d.point((x+1,y),fill=(222,211,181))
    assets[f'pavement_{i}']=(im,1)
for name,(original,pal) in list(assets.items()):
    if name.startswith('flowerbed_'):
        im=Image.new('RGBA',(16,16),(27,66,37,255));d=ImageDraw.Draw(im)
        # Overlapping leaf clusters: highlights top-left, shadows bottom-right.
        variant=sum(name.encode())%3
        for cx,cy in [(2,3),(9,1),(14,5),(6,7),(1,11),(12,12),(7,15)]:
            d.polygon([(cx-3,cy),(cx,cy-3),(cx+3,cy),(cx+1,cy+3)],fill=(50,107,46))
            d.line((cx-2,cy,cx,cy-2),fill=(106,154,62))
            d.line((cx+1,cy+1,cx+2,cy),fill=(35,83,39))
        for k,(x,y) in enumerate([(4+variant,5),(11,11-variant)]):
            # Contact shadow, curled shaded petals and a lit pollen center.
            d.ellipse((x-3,y-1,x+3,y+4),fill=(20,52,33))
            shade=(153,43,34) if k==0 else (151,167,139)
            base=(225,70,46) if k==0 else (230,236,198)
            light=(255,138,76) if k==0 else (255,252,224)
            d.polygon([(x-3,y-1),(x-1,y-2),(x,y-3),(x+2,y-2),(x+3,y),(x+2,y+2),(x,y+3),(x-2,y+2)],fill=shade)
            d.rectangle((x-2,y-1,x+2,y+1),fill=base);d.rectangle((x-1,y-2,x+1,y+2),fill=base)
            d.line((x-2,y-1,x-1,y-2),fill=light);d.point((x+1,y-2),fill=light)
            d.point((x,y),fill=(255,205,66));d.point((x+1,y+1),fill=(187,115,38))
        suffix=name.removeprefix('flowerbed_')
        if suffix in ['top','nw','ne']:d.line((0,0,15,0),fill=(106,154,62))
        if suffix in ['bottom','sw','se']:d.line((0,15,15,15),fill=(20,52,33))
        if suffix in ['right','ne','se']:d.line((15,0,15,15),fill=(20,52,33))
        # Round only the exterior corners, keeping adjacent cells seamless.
        corners={'nw':[(0,0),(1,0),(0,1)],'ne':[(15,0),(14,0),(15,1)],'sw':[(0,15),(1,15),(0,14)],'se':[(15,15),(14,15),(15,14)]}
        for p in corners.get(suffix,[]):im.putpixel(p,(0,0,0,0))
        assets[name]=(im,pal)
im=assets['bench'][0].copy();d=ImageDraw.Draw(im)
d.line((3,2,28,2),fill=(222,171,103));d.line((3,8,28,8),fill=(89,58,38))
for x in [7,16,24]:d.line((x,5,x+2,5),fill=(125,79,44))
assets['bench']=(im,9)
# Road edges retain the same paving grid as the middle of each alley.
# Supplied edge tiles were flat color patches, producing apparent missing tiles.
for direction in ['n','s','e','w']:
    im=assets['pavement_0'][0].copy();grass=assets['grass_0'][0]
    for y in range(16):
        for x in range(16):
            edge={'n':y,'s':15-y,'w':x,'e':15-x}[direction]
            if edge<2:im.putpixel((x,y),grass.getpixel((x,y)))
            elif edge==2:im.putpixel((x,y),(160,158,137,255))
    assets['path_edge_'+direction]=(im,1)
# ROM-ready kit: preserve indexed native artwork and consolidate palettes
# through this engine's existing resource pipeline. Native terrain retained.
KIT=SECOND/'source/rom_ready_kit'
for name,file,pal in [
 ('arena','arena_192x112.png',3),('blue','house_2_80x80.png',4),
 ('red','house_1_80x80.png',5),('green','house_3_80x80.png',6),
 ('yellow','house_4_80x80.png',7),('rewards','reward_shop_96x80.png',8),
 ('statue','statue_32x48.png',9),('flowers','flowerbed_32x32.png',0),
 ('fountain','fountain_frame_1_48x64.png',2)]:
    assets[name]=(Image.open(KIT/'gfx/objects'/file).convert('RGBA'),pal)
# Eight-pixel padding centers the basin on the colosseum's visual axis.
im=Image.new('RGBA',(64,64));im.alpha_composite(assets['fountain'][0],(8,0));assets['fountain']=(im,2)
palettes={};indexed={}
for pal in range(13):
    group=[(n,im) for n,(im,p) in assets.items() if p==pal]
    samples=[im.getpixel((x,y))[:3] for _,im in group for y in range(im.height) for x in range(im.width) if im.getpixel((x,y))[3]>128]
    strip=Image.new('RGB',(len(samples),1));strip.putdata(samples)
    quant=strip.quantize(colors=15,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE)
    rawpal=quant.getpalette()
    colors=[(0,0,0)]+[tuple(rawpal[i*3:i*3+3]) if len(rawpal)>=i*3+3 else (0,0,0) for i in range(15)]
    palettes[pal]=colors
    for name,im in group:
        q=im.convert('RGB').quantize(palette=quant,dither=Image.Dither.NONE)
        out=Image.new('P',im.size);out.putpalette(sum(map(list,colors),[])+[0]*720)
        out.putdata([v+1 if a[3]>128 else 0 for v,a in zip(q.getdata(),im.getdata())]);out.info['transparency']=0
        indexed[name]=out;out.save(OUT/f'{name}.png')
tiles=[bytes(64)];lookup={tiles[0]:0};metas=[];attrs=[];definitions={}
def subtile(raw):
    raw=bytes(raw)
    # Flip reuse is native GBA functionality, not image scaling.
    for bits in [0,0x400,0x800,0xc00]:
        candidate=bytes(raw[(7-y if bits&0x800 else y)*8+(7-x if bits&0x400 else x)] for y in range(8) for x in range(8))
        if candidate in lookup:return lookup[candidate]|bits
    lookup[raw]=len(tiles);tiles.append(raw);return len(tiles)-1
def define(name,ground=None):
    im=indexed[name];pal=assets[name][1];grid=[]
    for y in range(0,im.height,16):
        row=[]
        for x in range(0,im.width,16):
            fg=[]
            for q in range(4):fg.append(subtile(im.crop((x+q%2*8,y+q//2*8,x+q%2*8+8,y+q//2*8+8)).getdata())|pal<<12)
            bg=metas[definitions[ground][0][0]][4:] if ground else [0]*4
            row.append(len(metas));metas.append(bg+fg);attrs.append(0)
        grid.append(row)
    definitions[name]=grid
for n in ['grass_0','grass_1','grass_2','grass_3','pavement_0','pavement_1','pavement_2','water_0','water_1']:define(n)
for n in assets:
    if n not in definitions:define(n,'grass_0' if n.startswith(('tree','hedge','flowers','flowerbed')) or n in ['blue','red','green','yellow','rewards'] else 'pavement_0')
fountainTileStart=len(tiles)
fountainFrames=[]
base=assets['fountain'][0]
fixedPalette=Image.new('P',(1,1));fixedPalette.putpalette(sum(map(list,palettes[2]),[])+[0]*720)
for frame in range(1,5):
    candidate=Image.new('RGBA',(64,64))
    candidate.alpha_composite(Image.open(KIT/'gfx/objects'/f'fountain_frame_{frame}_48x64.png').convert('RGBA'),(8,0))
    im=base.copy()
    for y in range(64):
        for x in range(64):
            r,g,b,a=base.getpixel((x,y))
            # Only blue water changes; masonry and alpha remain frame0.
            if a>128 and b>r*1.2 and b>g*1.08:
                c=candidate.getpixel((x,y))
                if c[3]>128:im.putpixel((x,y),c)
    q=im.convert('RGB').quantize(palette=fixedPalette,dither=Image.Dither.NONE)
    raw=[v if rgba[3]>128 else 0 for v,rgba in zip(q.getdata(),im.getdata())]
    frameTiles=[bytes(raw[(ty+y)*64+tx+x] for y in range(8) for x in range(8)) for ty in range(0,64,8) for tx in range(0,64,8)]
    fountainFrames.append(frameTiles)
tiles.extend(fountainFrames[0])
for j,row in enumerate(definitions['fountain']):
    for i,mid in enumerate(row):
        metas[mid][4:]=[(fountainTileStart+(j*2+q//2)*8+i*2+q%2)|(2<<12) for q in range(4)]
anim=SECOND/'anim';anim.mkdir(exist_ok=True)
for i,frame in enumerate(fountainFrames):
    packed=bytes(t[k]|t[k+1]<<4 for t in frame for k in range(0,64,2))
    (anim/f'fountain_{i}.4bpp').write_bytes(packed)
assert len(tiles)<=1024,('GBA tile capacity exceeded',len(tiles))
assert len(metas)<640,('primary metatile capacity exceeded',len(metas))
layers={n:{} for n in ['ground','cliffs/water','buildings','decoration','above_player']}
collision={};placements=[];roads=set();land=set()
def put(layer,x,y,name,blocked=False):
    assert 0<=x<W and 0<=y<H,(name,x,y)
    layers[layer][(x,y)]=definitions[name][0][0];collision[(x,y)]=blocked
def rectroad(x,y,w,h):
    for j in range(y,y+h):
        for i in range(x,x+w):roads.add((i,j))
mask=Image.new('1',(W,H));ImageDraw.Draw(mask).polygon([(0,0),(47,0),(47,5),(44,7),(45,12),(43,16),(46,20),(44,23),(45,28),(42,34),(42,37),(37,39),(31,39),(27,40),(20,40),(16,39),(10,39),(5,37),(4,31),(2,29),(4,24),(3,20),(5,17),(3,13),(4,9),(1,7)],fill=1)
for y in range(H):
    for x in range(W):
        if mask.getpixel((x,y)):land.add((x,y));put('ground',x,y,f'grass_{(x*3+y*7)%4}')
        else:put('cliffs/water',x,y,f'water_{(x+y)%2}',True)
# Main avenues and four connected side loops.
rectroad(22,8,4,34);rectroad(5,19,38,2);rectroad(5,26,38,2)
rectroad(5,15,2,20);rectroad(40,15,3,20);rectroad(10,37,29,2)
rectroad(17,18,14,12)
rectroad(13,14,3,5);rectroad(32,16,3,3)
rectroad(0,12,7,2);rectroad(5,13,10,2);rectroad(5,13,2,6);rectroad(40,20,8,2)
rectroad(7,33,8,2);rectroad(13,33,2,5);rectroad(37,33,3,5)
for x,y in roads:put('ground',x,y,f'pavement_{(x+2*y)%3}')
# Native road edges. Corners use pavement; avoid ending a path in a building.
for x,y in list(roads):
    if (x,y) not in land:continue
    edges=[(dx,dy,n) for dx,dy,n in [(0,-1,'n'),(0,1,'s'),(-1,0,'w'),(1,0,'e')] if (x+dx,y+dy) in land and (x+dx,y+dy) not in roads]
    if len(edges)==1:put('ground',x,y,'path_edge_'+edges[0][2])
# Jagged shores with a consistent grass lip and water-facing stone face.
for x,y in sorted(land):
    if (x,y) in roads:continue
    exposed=''.join(n for dx,dy,n in [(0,-1,'n'),(0,1,'s'),(1,0,'e'),(-1,0,'w')] if (x+dx,y+dy) not in land and 0<=x+dx<W and 0<=y+dy<H)
    if exposed:
        key=next((n for n in ['se','sw','ne','nw'] if all(c in exposed for c in n)),exposed[0])
        put('cliffs/water',x,y,'shore_'+key,True)
# Continuous woodland cliffs; terrace stairs removed by the map owner.
for y in [4,8]:
    for x in list(range(0,18))+list(range(30,W)):
        put('cliffs/water',x,y,'cliff_'+str(x%2),True)
def place(name,x,y,layer='decoration',blocked=True,door=None,walkrows=()):
    im=indexed[name];grid=definitions[name];occupied=[]
    for j,row in enumerate(grid):
        for i,mid in enumerate(row):
            assert 0<=x+i<W and 0<=y+j<H,(name,x,y)
            box=im.crop((i*16,j*16,i*16+16,j*16+16))
            if not box.getbbox():continue
            layers[layer][(x+i,y+j)]=mid
            collision[(x+i,y+j)]=blocked and j not in walkrows and (i,j)!=door
            occupied.append([x+i,y+j])
            if (i,j)==door:attrs[mid]=0x69
    placements.append(dict(asset=name,x=x,y=y,layer=layer,occupied=occupied))
place('arena',18,1,'buildings',door=(6,4),walkrows=(5,6))
# Repeated native 80px houses establish one consistent scale.
place('mart',11,9,'buildings',door=(2,3))
place('rewards',30,11,'buildings',door=(3,4))
place('red',8,14,'buildings');place('yellow',39,10,'buildings')
place('red',9,21,'buildings');place('blue',35,21,'buildings')
place('center',7,28,'buildings',door=(2,4));place('yellow',35,28,'buildings')
place('green',32,31,'buildings',door=(2,4));place('red',16,32,'buildings');place('red',27,32,'buildings')
# Explicit pedestrian approaches in front of service doors.
for x,y,w,h in [(13,14,3,5),(32,16,3,3),(22,7,4,4),(8,33,4,2)]:
    rectroad(x,y,w,h)
    for yy in range(y,y+h):
        for xx in range(x,x+w):
            if (xx,yy) not in layers['buildings']:put('ground',xx,yy,'pavement_0')
# Symmetric meeting square, four structured beds and four inward benches.
def flowerbed(x,y,w,h):
    for j in range(h):
        for i in range(w):
            n='flowerbed_'+('nw' if i==0 and j==0 else 'ne' if i==w-1 and j==0 else 'sw' if i==0 and j==h-1 else 'se' if i==w-1 and j==h-1 else 'top' if j==0 else 'bottom' if j==h-1 else 'left' if i==0 else 'right' if i==w-1 else 'center')
            put('decoration',x+i,y+j,n,True)
# Meeting-square beds are grass islands, never flowers over paving.
for x,y,h in [(18,18,1),(27,18,1),(18,28,2),(27,28,2)]:
    for j in range(h):
        for i in range(3):
            roads.discard((x+i,y+j))
            put('ground',x+i,y+j,'grass_0')
    flowerbed(x,y,3,h)
for x,y in [(14,23),(31,23)]:flowerbed(x,y,3,3)
for x,y in [(20,21),(26,21),(20,25),(26,25)]:place('bench',x,y)
place('fountain',22,21)
# Colosseum forecourt: statues, bounded gardens and flank lamps.
for x in [19,27]:place('statue',x,8);flowerbed(x,11,2,1)
for x in range(22,27):put('decoration',x,8,'stairs')
for x,y in [(17,9),(29,9),(16,18),(30,18),(16,27),(30,27),(12,25),(34,26),(14,32),(39,33)]:
    cells={(x+i,y+j) for i in range(2) for j in range(3)}
    if not cells&roads and not cells&set(layers['buildings']):place('tree0',x,y,'above_player')
for x,y in [(16,17),(31,17),(16,28),(31,28),(7,16),(43,21)]:place('lamp',x,y)
def fencebox(x,y,w,h,gap=()):
    for j in range(h):
        for i in range(w):
            if (i,j) in gap or (i not in [0,w-1] and j not in [0,h-1]):continue
            n='fence_corner_'+('nw' if i==0 and j==0 else 'ne' if i==w-1 and j==0 else 'sw' if i==0 and j==h-1 else 'se' if i==w-1 and j==h-1 else '') if i in [0,w-1] and j in [0,h-1] else 'fence_horizontal' if j in [0,h-1] else 'fence_vertical'
            p=(x+i,y+j)
            if p not in roads and p not in layers['buildings']:put('decoration',*p,n,True)
for x,y,w,h in [(8,21,7,6),(34,22,8,6),(6,28,8,6),(33,29,8,6),(16,32,7,6),(24,32,7,6)]:fencebox(x,y,w,h,gap=[(i,h-1) for i in range(2,min(w-1,7))])
# Shrubs and flowering borders occupy grass pockets between houses/paths.
for x,y in [(15,23),(32,24),(5,23),(41,29),(14,30),(32,33),(29,36),(14,35),(6,19),(37,17)]:
    cells={(x+i,y+j) for i in range(2) for j in range(2)}
    if not cells&roads and not cells&set(layers['buildings']):flowerbed(x,y,2,2)
trees=[(1,0),(5,0),(9,0),(14,0),(32,0),(37,0),(42,0),(45,0),
 (2,5),(6,5),(14,5),(31,5),(39,5),(43,5),(4,9),(7,9),(15,9),(32,9),(39,9),(43,9),
 (3,15),(42,16),(2,21),(43,23),(4,26),(42,28),(3,30),(13,27),(31,27),
 (8,34),(13,34),(34,35),(39,33),(17,36)]
for k,(x,y) in enumerate(trees):
    cells={(x+i,y+j) for i in range(2) for j in range(3)}
    if not cells&roads and not cells&set(layers['buildings']):place(f'tree{k%3}',x,y,'above_player')
# Extra flowers only on unobstructed grass, with one cell of clearance
# from roads; never overwrite trees, fences, houses or cliff edges.
for x,y in [(9,10),(17,14),(37,10),(36,17),(8,18),(10,18),
            (17,16),(29,16),(8,25),(30,30),(15,29),(10,35),
            (15,36),(29,36),(38,36),(20,12),(28,12)]:
    cells={(x+i,y+j) for i in range(2) for j in range(2)}
    margin={(xx+dx,yy+dy) for xx,yy in cells for dx,dy in [(0,0),(1,0),(-1,0),(0,1),(0,-1)]}
    occupied=set().union(*(set(layers[n]) for n in ['buildings','decoration','above_player','cliffs/water']))
    if cells<=land and not margin&roads and not cells&occupied:
        flowerbed(x,y,2,2)
# Reference gardens: hedges sit within grass plots, clear of approaches.
for x,y,w in [(18,12,3),(26,12,3),(9,18,3),(35,17,3),
              (9,25,3),(35,25,3),(15,31,3),(27,31,3),
              (17,36,3),(27,36,3)]:
    for xx in range(x,x+w):
        p=(xx,y)
        occupied=set().union(*(set(layers[n]) for n in ['buildings','decoration','above_player','cliffs/water']))
        if p in land and p not in roads and p not in occupied:
            put('decoration',xx,y,'hedge_straight',True)
# Piers assembled from actual 16px wood tiles: no sideways stretched bridges.
for x,y in sorted(roads-land):put('cliffs/water',x,y,'wood_dock')
# Final map, collision and native events.
final={}
for layer in layers:
    for p,mid in layers[layer].items():final[p]=mid
data=[final[(x,y)]|(0x400 if collision.get((x,y)) else 0x3000) for y in range(H) for x in range(W)]
doors=[(9,32,'MAP_MULTI_ARENA_CENTER'),(33,15,'MAP_MULTI_ARENA_VENDOR'),(13,12,'MAP_MULTI_ARENA_MART'),(24,5,'MAP_MULTI_ARENA_COLOSSEUM'),(34,35,'MAP_MULTI_ARENA_HOUSE')]
# Every visible residence has a separate interior and a matching return warp.
houses=[(9,18),(40,14),(10,25),(37,25),(36,32),(17,36),(28,36)]
for i,(x,y) in enumerate(houses,1):
    doors.append((x,y,f'MAP_MULTI_ARENA_HOUSE{i}'))
    for yy in [y,y+1]:
        data[yy*W+x]=(data[yy*W+x]&1023)|0x3000
    if (x,y+1) not in roads:
        for xx in range(x,38):
            if (xx,y+1) in layers['buildings']:break
            data[(y+1)*W+xx]=definitions['pavement_0'][0][0]|0x3000
            if (xx,y+1) in roads:break
# Mart door is in the lower blue hall; clear its actual doorstep.
for x,y,dest in doors:
    data[y*W+x]=(data[y*W+x]&1023)|0x3000;attrs[data[y*W+x]&1023]=0x69
# A broad front walk links the green house to the southern promenade.
for yy in [36,37]:
    for xx in range(32,37):data[yy*W+xx]=definitions['pavement_0'][0][0]|0x3000
mapfile=ROOT/'data/maps/MultiArena/map.json';m=json.loads(mapfile.read_text())
m['warp_events']=[dict(x=x,y=y,elevation=3,dest_map=dest,dest_warp_id='0') for x,y,dest in doors]
# Interior warp indices retain Center=1, Mart=0 from the existing format.
m['warp_events']=[m['warp_events'][2],m['warp_events'][0],m['warp_events'][1],m['warp_events'][3],m['warp_events'][4]]+m['warp_events'][5:]
m['coord_events']=[dict(type='trigger',x=1,y=y,elevation=3,var='VAR_TEMP_0',var_value='0',script='MultiArena_Exit') for y in [12,13]]
groupsfile=ROOT/'data/maps/map_groups.json';groups=json.loads(groupsfile.read_text())
eventsfile=ROOT/'data/event_scripts.s';events=eventsfile.read_text()
for i,(x,y) in enumerate(houses,1):
    name=f'MultiArena_House{i}';folder=ROOT/'data/maps'/name;folder.mkdir(exist_ok=True)
    house=json.loads((ROOT/'data/maps/MultiArena_House/map.json').read_text())
    house.update(id=f'MAP_MULTI_ARENA_HOUSE{i}',name=name)
    for warp in house['warp_events']:warp['dest_warp_id']=str(4+i)
    for obj in house['object_events']:obj['script']=f'{name}_Welcome'
    (folder/'map.json').write_text(json.dumps(house,indent=2)+'\n')
    (folder/'scripts.inc').write_text(f'{name}_MapScripts::\n\t.byte 0\n{name}_Welcome::\n\tlock\n\tfaceplayer\n\tmsgbox {name}_Text, MSGBOX_DEFAULT\n\trelease\n\tend\n{name}_Text::\n\t.string "Welcome to our ARENA town!$"\n')
    if name not in groups['gMapGroup_SpecialArea']:groups['gMapGroup_SpecialArea'].append(name)
    line=f'\t.include "data/maps/{name}/scripts.inc"'
    if line not in events:events+='\n'+line+'\n'
groupsfile.write_text(json.dumps(groups,indent=2)+'\n');eventsfile.write_text(events)
npcs=[(24,12),(10,20),(36,19),(17,30),(29,16),(8,27),(23,26)]
for o,(x,y) in zip(m['object_events'],npcs):o.update(x=x,y=y)
blocked=set(npcs);start=(6,13)
buildingRoadConflicts=[(x,y) for x,y in layers['buildings'] if (x,y) in roads and collision.get((x,y))]
assert not buildingRoadConflicts,('building placed across road',buildingRoadConflicts)
def walk(p):
    x,y=p
    return 0<=x<W and 0<=y<H and not data[y*W+x]&0xc00 and p not in blocked
seen={start};queue=collections.deque([start])
while queue:
    x,y=queue.popleft()
    for p in [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]:
        if p not in seen and walk(p):seen.add(p);queue.append(p)
targets=[(x,y+1) for x,y,_ in doors]+[(1,13),(23,40)]
errors=[('unreachable entrance',p) for p in targets if p not in seen]
for x,y in npcs:
    if not any(p in seen for p in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]):errors.append(('unreachable NPC',(x,y)))
assert not errors,(errors,[(x,y,hex(data[y*W+x]),(x,y) in seen) for y in range(31,36) for x in range(8,12)])
# Seal unreachable grass pockets rather than leaving walkable isolated cells.
sealed=0
for y in range(H):
    for x in range(W):
        if walk((x,y)) and (x,y) not in seen:
            data[y*W+x]=(data[y*W+x]&1023)|0x400;sealed+=1
for folder in [PRIMARY,SECOND]:
    for pal in range(16):
        colors=palettes.get(pal,[(0,0,0)]*16)
        (folder/f'palettes/{pal:02}.pal').write_text('JASC-PAL\n0100\n16\n'+'\n'.join(' '.join(map(str,c)) for c in colors)+'\n')
for offset,count,folder in [(0,640,PRIMARY),(640,384,SECOND)]:
    im=Image.new('P',(128,count//16*8));im.putpalette(sum(map(list,palettes[0]),[])+[0]*720)
    for i in range(count):
        t=Image.new('P',(8,8));t.putdata(tiles[offset+i] if offset+i<len(tiles) else bytes(64));im.paste(t,(i%16*8,i//16*8))
    im.save(folder/'tiles.png')
(PRIMARY/'metatiles.bin').write_bytes(b''.join(struct.pack('<8H',*m) for m in metas))
(PRIMARY/'metatile_attributes.bin').write_bytes(struct.pack('<'+'I'*len(attrs),*attrs))
(SECOND/'metatiles.bin').write_bytes(bytes(16));(SECOND/'metatile_attributes.bin').write_bytes(bytes(4))
(ROOT/'data/layouts/MultiArena/map.bin').write_bytes(struct.pack('<'+'H'*len(data),*data))
(ROOT/'data/layouts/MultiArena/border.bin').write_bytes(struct.pack('<4H',*([definitions['water_0'][0][0]|0x400]*4)))
layoutfile=ROOT/'data/layouts/layouts.json';ls=json.loads(layoutfile.read_text());l=next(l for l in ls['layouts'] if l.get('id')=='LAYOUT_MULTI_ARENA');l.update(width=W,height=H)
layoutfile.write_text(json.dumps(ls,indent=2)+'\n');mapfile.write_text(json.dumps(m,indent=2)+'\n')
script=ROOT/'data/maps/MultiArena/scripts.inc';s=script.read_text().replace('255, 6, 12','255, 6, 13').replace('255, 24, 5','255, 24, 7');script.write_text(s)
# Water-only fountain cycle: four frames, one dedicated 64-tile VRAM range.
script=ROOT/'src/tileset_anims.c';s=script.read_text()
marker='static const u16 sMultiArenaFountain0' if 'static const u16 sMultiArenaFountain0' in s else 'void InitTilesetAnim_MultiArena(void) {'
s=s[:s.index(marker)]
for i in range(4):s+=f'static const u16 sMultiArenaFountain{i}[] = INCBIN_U16("data/tilesets/secondary/multi_arena/anim/fountain_{i}.4bpp");\n'
s+='static const u16 *const sMultiArenaFountainFrames[] = {sMultiArenaFountain0,sMultiArenaFountain1,sMultiArenaFountain2,sMultiArenaFountain3};\n'
s+=f'static void TilesetAnim_MultiArena(u16 timer) {{ if (timer % 12 == 0) AppendTilesetAnimToBuffer(sMultiArenaFountainFrames[(timer / 12) % 4], (u16 *)(BG_VRAM + TILE_OFFSET_4BPP({fountainTileStart})), 64 * TILE_SIZE_4BPP); }}\n'
s+='void InitTilesetAnim_MultiArena(void) { sSecondaryTilesetAnimCounter=0; sSecondaryTilesetAnimCounterMax=48; sSecondaryTilesetAnimCallback=TilesetAnim_MultiArena; }\n'
script.write_text(s)
recipe=dict(width=W,height=H,layers={n:[dict(x=x,y=y,metatile=v) for (x,y),v in cells.items()] for n,cells in layers.items()},finalBlocks=data,objects=placements,collision=[dict(x=x,y=y,blocked=bool(data[y*W+x]&0xc00)) for y in range(H) for x in range(W)],doors=doors,arrival=start)
(ROOT/'data/layouts/MultiArena/source_layers.json').write_text(json.dumps(recipe,indent=2)+'\n')
report=dict(tiles=len(tiles),tileLimit=1024,metatiles=len(metas),paletteBanks=len(palettes),colorsPerBank=16,reachableCells=len(seen),sealedIsolatedCells=sealed,doorApproaches=targets,allNPCsReachable=True,assets={n:dict(size=list(im.size),palette=p) for n,(im,p) in assets.items()})
(ROOT/'data/layouts/MultiArena/validation.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='assets'},indent=2))











