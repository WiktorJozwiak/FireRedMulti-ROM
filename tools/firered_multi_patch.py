"""Build a BPS delta and ABI manifest; never publish a complete ROM."""
import json, pathlib, struct, sys, zlib

source=pathlib.Path(sys.argv[1]).read_bytes()
target=pathlib.Path(sys.argv[2]).read_bytes()
out=pathlib.Path(sys.argv[3]);out.mkdir(parents=True,exist_ok=True)
def number(value):
    result=bytearray()
    while True:
        part=value&127;value>>=7
        if value==0:
            result.append(part|128);return result
        result.append(part);value-=1
patch=bytearray(b'BPS1')+number(len(source))+number(len(target))+number(0)
at=0
while at<len(target):
    equal=at<len(source) and target[at]==source[at]
    end=at+1
    while end<len(target) and (end<len(source) and target[end]==source[end])==equal:end+=1
    patch+=number(((end-at-1)<<2)|(0 if equal else 1))
    if not equal:patch+=target[at:end]
    at=end
patch+=struct.pack('<II',zlib.crc32(source),zlib.crc32(target))
patch+=struct.pack('<I',zlib.crc32(patch))
(out/'FireRedMulti-PvP.bps').write_bytes(patch)
symbols={}
for line in pathlib.Path('pokefirered.sym').read_text().splitlines():
    parts=line.split()
    if len(parts)>=2:
        try:symbols[parts[-1]]=int(parts[0],16)
        except ValueError:pass
names=['gFireRedMulti','gPlayerParty','gPlayerPartyCount','gMain','CB2_Overworld','gSaveBlock1Ptr','gSaveBlock2Ptr','gPokemonStoragePtr']
manifest={'abi':1,'sourceCRC32':zlib.crc32(source),'targetCRC32':zlib.crc32(target),'symbols':{name:symbols[name] for name in names},'mailboxSize':1088}
(out/'FireRedMulti-PvP.json').write_text(json.dumps(manifest,indent=2))
print('BPS patch bytes:',len(patch))
