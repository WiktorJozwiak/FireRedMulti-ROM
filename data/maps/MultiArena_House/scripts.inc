MultiArena_House_MapScripts::
	.byte 0
MultiArena_House_Welcome::
	lock
	faceplayer
	msgbox MultiArena_House_Text, MSGBOX_DEFAULT
	release
	end
MultiArena_House_Text::
	.string "A quiet place to rest before\n"
	.string "your next ARENA battle!$"
