#ifndef GUARD_MULTI_ARENA_H
#define GUARD_MULTI_ARENA_H
struct MultiArenaChannel { u32 magic, seq; u16 event, outcome; u32 ack, result; };
extern struct MultiArenaChannel gMultiArena;
void FireRedMulti_ArenaRequest(void);
void FireRedMulti_ArenaBattle(void);
u8 FireRedMulti_ArenaParty(struct Pokemon *party);
#endif
