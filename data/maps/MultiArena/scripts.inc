MultiArena_MapScripts::
	.byte 0
MultiArena_Entrance::
	lock
	faceplayer
	msgbox MultiArena_EntranceText, MSGBOX_YESNO
	compare VAR_RESULT, NO
	goto_if_eq MultiArena_Done
	warp MAP_MULTI_ARENA, 255, 3, 24
	waitstate
	release
	end
MultiArena_Exit::
	lockall
	warp MAP_CERULEAN_CITY, 255, 44, 27
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
	msgbox MultiArena_VendorText, MSGBOX_YESNO
	compare VAR_RESULT, NO
	goto_if_eq MultiArena_Done
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
	.string "Welcome! Visit the MULTI\nARENA?\pBattles, healing and token\nrewards!$"
MultiArena_HealText::
	.string "Your POKEMON are fully\nhealed!$"
MultiArena_VendorText::
	.string "Exchange ARENA TOKENS for\nitems!\pBrowse the reward shop?\nPress B to leave the shop.$"
MultiArena_TrainerText::
	.string "Ready for a training battle?\nMy team scales with yours.\pWin EXP and an ARENA TOKEN!$"

MultiArena_LeaveColosseum::
	lockall
	warp MAP_MULTI_ARENA, 255, 20, 12
	waitstate
	releaseall
	end
MultiArena_Welcome::
	lock
	faceplayer
	msgbox MultiArena_WelcomeText, MSGBOX_DEFAULT
	release
	end
MultiArena_WelcomeText::
	.string "The COLOSSEUM is just ahead!\nTraining battles await inside.\pGood luck, challenger!$"
MultiArena_Lodge::
	msgbox MultiArena_LodgeText, MSGBOX_SIGN
	end
MultiArena_LodgeText::
	.string "ARENA LODGE\nA quiet place for visiting\ptrainers.$"
MultiArena_Chatter1::
	lock
	faceplayer
	msgbox MultiArena_Chatter1Text, MSGBOX_DEFAULT
	release
	end
MultiArena_Chatter1Text::
	.string "Tokens buy useful supplies.\nI am saving mine for a FIRE\pSTONE!$"
MultiArena_Chatter2::
	lock
	faceplayer
	msgbox MultiArena_Chatter2Text, MSGBOX_DEFAULT
	release
	end
MultiArena_Chatter2Text::
	.string "Winning feels great!\nEven the losing trainer earns\pa\ntoken after a proper PVP\pbattle.$"
MultiArena_Chatter3::
	lock
	faceplayer
	msgbox MultiArena_Chatter3Text, MSGBOX_DEFAULT
	release
	end
MultiArena_Chatter3Text::
	.string "I came here to cheer for my\nfriend.\pNext time, I will enter too!$"
MultiArena_Chatter4::
	lock
	faceplayer
	msgbox MultiArena_Chatter4Text, MSGBOX_DEFAULT
	release
	end
MultiArena_Chatter4Text::
	.string "The training teams match your\nlevel.\pStrategy matters more than\nsize!$"
MultiArena_Chatter5::
	lock
	faceplayer
	msgbox MultiArena_Chatter5Text, MSGBOX_DEFAULT
	release
	end
MultiArena_Chatter5Text::
	.string "The POKEMON CENTER is free.\nRest your team before the next\pmatch!$"

MultiArena_EnterSideGate::
	lockall
	warp MAP_MULTI_ARENA, 255, 3, 24
	waitstate
	releaseall
	end
MultiArena_GateSign::
	msgbox MultiArena_GateSignText, MSGBOX_SIGN
	end
MultiArena_GateSignText::
	.string "MULTI ARENA\nFollow the path east!$"

MultiArena_Fountain::
	lock
	faceplayer
	msgbox MultiArena_FountainText, MSGBOX_DEFAULT
	release
	end
MultiArena_FountainText::
	.string "I love resting by this fountain.\nThe arena can get so lively!$"
