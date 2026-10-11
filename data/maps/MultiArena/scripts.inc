MultiArena_MapScripts::
	.byte 0
MultiArena_Entrance::
	lock
	faceplayer
	msgbox MultiArena_EntranceText, MSGBOX_YESNO
	compare VAR_RESULT, NO
	goto_if_eq MultiArena_Done
	warp MAP_MULTI_ARENA, 255, 20, 31
	waitstate
	release
	end
MultiArena_Exit::
	lockall
	warp MAP_CERULEAN_CITY, 255, 11, 24
	waitstate
	releaseall
	end
MultiArena_Heal::
	lock
	faceplayer
	special HealPlayerParty
	msgbox MultiArena_HealText, MSGBOX_DEFAULT
MultiArena_Done::
	release
	end
MultiArena_Mart::
	lock
	faceplayer
	pokemart MultiArena_Items
	release
	end
	.align 2
MultiArena_Items::
	.2byte ITEM_POKE_BALL, ITEM_POTION, ITEM_SUPER_POTION, ITEM_ANTIDOTE, ITEM_NONE
MultiArena_Vendor::
	lock
	faceplayer
	msgbox MultiArena_VendorText, MSGBOX_DEFAULT
	setvar VAR_0x8004, 1
	special FireRedMulti_ArenaRequest
	waitstate
	release
	end
MultiArena_Trainer::
	lock
	faceplayer
	specialvar VAR_RESULT, CountPartyNonEggMons
	compare VAR_RESULT, 0
	goto_if_eq MultiArena_Done
	msgbox MultiArena_TrainerText, MSGBOX_YESNO
	compare VAR_RESULT, NO
	goto_if_eq MultiArena_Done
	setvar VAR_0x8004, 2
	special FireRedMulti_ArenaRequest
	waitstate
	compare VAR_RESULT, 1
	goto_if_ne MultiArena_Done
	special FireRedMulti_ArenaBattle
	waitstate
	release
	end
MultiArena_EntranceText::
	.string "Welcome! Visit the MULTI ARENA?\pBattles, healing and token rewards!$"
MultiArena_HealText::
	.string "Your POKEMON are fully healed!$"
MultiArena_VendorText::
	.string "Exchange ARENA TOKENS for items!\pThe reward shop opens above the game.$"
MultiArena_TrainerText::
	.string "Ready for a training battle?\pMy team scales with yours.\nWin EXP and an ARENA TOKEN!$"
