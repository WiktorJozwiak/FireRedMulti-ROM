MultiArena_House6_MapScripts::
	.byte 0
MultiArena_House6_Welcome::
	lock
	faceplayer
	msgbox MultiArena_House6_Text, MSGBOX_DEFAULT
	release
	end
MultiArena_House6_Text::
	.string "Welcome to our ARENA town!$"
