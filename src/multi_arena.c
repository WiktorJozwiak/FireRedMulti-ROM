#include "global.h"
#include "multi_arena.h"
#include "battle.h"
#include "battle_setup.h"
#include "battle_main.h"
#include "battle_transition.h"
#include "overworld.h"
#include "main.h"
#include "pokemon.h"
#include "script.h"
#include "event_data.h"
#include "constants/species.h"
#include "constants/trainers.h"
#include "constants/battle.h"

void FireRedMulti_ArenaRequest(void)
{
    gMultiArena.magic = 0x414E5246;
    gMultiArena.event = gSpecialVar_0x8004;
    gMultiArena.outcome = 0;
    gMultiArena.seq++;
}

u8 FireRedMulti_ArenaParty(struct Pokemon *party)
{
    static const u16 species[][3] = {{SPECIES_PIDGEOT, SPECIES_GOLDUCK, SPECIES_RHYDON}, {SPECIES_RAICHU, SPECIES_PRIMEAPE, SPECIES_TANGELA}, {SPECIES_NINETALES, SPECIES_SANDSLASH, SPECIES_DEWGONG}};
    u16 total = 0;
    u8 levels[6] = {0}, count = 0, i, j, n, level, rotation;
    for (i = 0; i < gPlayerPartyCount; i++)
    {
        if (GetMonData(&gPlayerParty[i], MON_DATA_IS_EGG) || !GetMonData(&gPlayerParty[i], MON_DATA_SPECIES)) continue;
        levels[count++] = GetMonData(&gPlayerParty[i], MON_DATA_LEVEL);
    }
    for (i = 0; i < count; i++) for (j = i + 1; j < count; j++) if (levels[j] > levels[i]) { n = levels[i]; levels[i] = levels[j]; levels[j] = n; }
    n = count > 3 ? 3 : count;
    level = 0;
    for (i = 0; i < n; i++) total += levels[i];
    level = n ? total / n : 5;
    if (level < 5) level = 5;
    rotation = gMultiArena.seq % 3;
    ZeroEnemyPartyMons();
    for (i = 0; i < n; i++) CreateMon(&party[i], level < 20 ? (i == 0 ? SPECIES_PIDGEY : i == 1 ? SPECIES_PSYDUCK : SPECIES_SANDSHREW) : species[rotation][i], level, 15, FALSE, 0, OT_ID_RANDOM_NO_SHINY, 0);
    return n;
}
