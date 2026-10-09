#include "global.h"
#include "firered_multi.h"
#include "battle.h"
#include "battle_main.h"
#include "link.h"
#include "main.h"
#include "overworld.h"
#include "pokemon.h"
#include "script.h"
#include "script_pokemon_util.h"
#include "constants/trainers.h"

extern void (*gLinkCallback)(void);

__attribute__((section("multi_data"))) struct FireRedMultiMailbox gFireRedMulti = {0};
static __attribute__((section("multi_data"))) struct Pokemon sPartyBackup[PARTY_SIZE] = {0};
static __attribute__((section("multi_data"))) u8 sPartyCount = 0;
static __attribute__((section("multi_data"))) u8 sReceived = 0;
static __attribute__((section("multi_data"))) bool8 sActive = FALSE;
static __attribute__((section("multi_data"))) u32 sHeartbeat = 0;
static __attribute__((section("multi_data"))) u16 sWaitFrames = 0;

bool8 FireRedMulti_Active(void) { return sActive; }

static void FinishBattle(void)
{
    memcpy(gPlayerParty, sPartyBackup, sizeof(sPartyBackup));
    gPlayerPartyCount = sPartyCount;
    gFireRedMulti.outcome = gBattleOutcome;
    gFireRedMulti.state = gFireRedMulti.error ? 4 : 3;
    sActive = FALSE;
    gReceivedRemoteLinkPlayers = 0;
    gBattleTypeFlags = 0;
    gWirelessCommType = 0;
    gLinkCallback = NULL;
    UnlockPlayerFieldControls();
    SetMainCallback2(CB2_ReturnToField);
}

bool8 FireRedMulti_SendBlock(const void *src, u16 size)
{
    if (!FireRedMulti_SendFinished() || size == 0 || size > FR_MULTI_PAYLOAD)
        return FALSE;
    memcpy(gFireRedMulti.tx, src, size);
    memcpy(gBlockRecvBuffer[gFireRedMulti.playerId], src, size);
    sReceived |= 1 << gFireRedMulti.playerId;
    gFireRedMulti.txSize = size;
    gFireRedMulti.txSeq++;
    return TRUE;
}

bool8 FireRedMulti_SendFinished(void)
{
    return gFireRedMulti.txSeq == gFireRedMulti.txAck;
}

u8 FireRedMulti_Received(void) { return sReceived; }
void FireRedMulti_ResetReceived(u8 mask) { sReceived &= ~mask; }

void FireRedMulti_Tick(void)
{
    u8 i;
    if (gFireRedMulti.magic != FR_MULTI_MAGIC)
    {
        memset(&gFireRedMulti, 0, sizeof(gFireRedMulti));
        gFireRedMulti.magic = FR_MULTI_MAGIC;
        gFireRedMulti.version = 1;
    }
    if (gFireRedMulti.commandSeq != gFireRedMulti.commandAck)
    {
        gFireRedMulti.commandAck = gFireRedMulti.commandSeq;
        if (gFireRedMulti.command == 1 && !sActive && FireRedMulti_CanStart() && gPlayerPartyCount > 0 && gFireRedMulti.playerId < 2)
        {
            memcpy(sPartyBackup, gPlayerParty, sizeof(sPartyBackup));
            sPartyCount = gPlayerPartyCount;
            HealPlayerParty();
            gFireRedMulti.error = 0;
            gFireRedMulti.outcome = 0;
            gFireRedMulti.txSeq = 0;
            gFireRedMulti.rxAck = 0;
            sReceived = 0;
            sActive = TRUE;
            sHeartbeat = gFireRedMulti.heartbeat;
            sWaitFrames = 0;
            gWirelessCommType = 0;
            gReceivedRemoteLinkPlayers = 1;
            gLinkCallback = NULL;
            gLinkType = 0x2211;
            gLinkStatus = 0x48 | (gFireRedMulti.playerId == 0 ? 0x20 : 0) | gFireRedMulti.playerId;
            memset(gLinkPlayers, 0, sizeof(gLinkPlayers));
            for (i = 0; i < 2; i++)
            {
                gLinkPlayers[i].version = 4; // VERSION_FIRE_RED
                gLinkPlayers[i].id = i;
                gLinkPlayers[i].language = 2;
                gLinkPlayers[i].linkType = 0x2211;
                gLinkPlayers[i].trainerId = i + 1;
                memcpy(gLinkPlayers[i].name, gFireRedMulti.names[i], 8);
            }
            gLocalLinkPlayerId = gFireRedMulti.playerId;
            gTrainerBattleOpponent_A = TRAINER_LINK_OPPONENT;
            gBattleTypeFlags = BATTLE_TYPE_LINK | BATTLE_TYPE_TRAINER;
            gMain.savedCallback = FinishBattle;
            gFireRedMulti.state = 2;
            FireRedMulti_StartBattle();
        }
        else if (gFireRedMulti.command == 2 && sActive)
            gFireRedMulti.error = 1;
        else if (gFireRedMulti.command == 1)
            gFireRedMulti.error = 2;
    }
    if (!sActive)
    {
        if (gFireRedMulti.state < 2)
            gFireRedMulti.state = FireRedMulti_CanStart() && gPlayerPartyCount > 0 ? 1 : 0;
        return;
    }
    if (gFireRedMulti.rxSeq != gFireRedMulti.rxAck && !(sReceived & (1 << (gFireRedMulti.playerId ^ 1))))
    {
        if (gFireRedMulti.rxSeq != gFireRedMulti.rxAck + 1 || !gFireRedMulti.rxSize || gFireRedMulti.rxSize > FR_MULTI_PAYLOAD)
            gFireRedMulti.error = 3;
        else
        {
            memcpy(gBlockRecvBuffer[gFireRedMulti.playerId ^ 1], gFireRedMulti.rx, gFireRedMulti.rxSize);
            sReceived |= 1 << (gFireRedMulti.playerId ^ 1);
            gFireRedMulti.rxAck = gFireRedMulti.rxSeq;
        }
    }
    if (sHeartbeat != gFireRedMulti.heartbeat)
    {
        sHeartbeat = gFireRedMulti.heartbeat;
        sWaitFrames = 0;
    }
    else if (++sWaitFrames >= 3600)
        gFireRedMulti.error = 4;
    // Browser restores a dedicated pre-battle recovery state on cancellation.
    // Stop processing callbacks, rather than freeing partially initialized
    // battle resources or writing damaged battle state into the save.
}
