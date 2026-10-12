MultiArena_House2_MapScripts::
	.byte 0
MultiArena_House2_Welcome::
	lock
	faceplayer
	msgbox MultiArena_House2_Text, MSGBOX_DEFAULT
	release
	end
MultiArena_House2_Text::
	.string "Welcome to our ARENA town!$"
