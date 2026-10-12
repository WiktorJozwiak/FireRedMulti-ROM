MultiArena_House4_MapScripts::
	.byte 0
MultiArena_House4_Welcome::
	lock
	faceplayer
	msgbox MultiArena_House4_Text, MSGBOX_DEFAULT
	release
	end
MultiArena_House4_Text::
	.string "Welcome to our ARENA town!$"
