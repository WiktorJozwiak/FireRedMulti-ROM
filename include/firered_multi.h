#ifndef GUARD_FIRERED_MULTI_H
#define GUARD_FIRERED_MULTI_H

#define FR_MULTI_PAYLOAD 512
#define FR_MULTI_MAGIC 0x50524D46

// ABI 1: host writes command/rx/ack/heartbeat; ROM writes state/tx/rxAck.
// Sequence counters make repeated CodeBreaker memory writes idempotent.
struct FireRedMultiMailbox
{
    u32 magic;
    u16 version;
    u16 state; // 0 idle, 1 ready, 2 battle, 3 finished, 4 aborted
    u32 commandSeq;
    u32 commandAck;
    u16 command; // 1 start, 2 cancel
    u16 playerId;
    u32 heartbeat;
    u32 txSeq;
    u32 txAck;
    u16 txSize;
    u16 outcome;
    u32 rxSeq;
    u32 rxAck;
    u16 rxSize;
    u16 error;
    u8 tx[FR_MULTI_PAYLOAD];
    u8 rx[FR_MULTI_PAYLOAD];
    u8 names[2][8];
};

extern struct FireRedMultiMailbox gFireRedMulti;
bool8 FireRedMulti_Active(void);
bool8 FireRedMulti_CanStart(void);
void FireRedMulti_Tick(void);
void FireRedMulti_StartBattle(void);
bool8 FireRedMulti_SendBlock(const void *src, u16 size);
bool8 FireRedMulti_SendFinished(void);
u8 FireRedMulti_Received(void);
void FireRedMulti_ResetReceived(u8 mask);

#endif
