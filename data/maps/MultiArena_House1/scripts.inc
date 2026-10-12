MultiArena_House1_MapScripts::
	.byte 0
MultiArena_House1_Welcome::
	lock
	faceplayer
	msgbox MultiArena_House1_Text, MSGBOX_DEFAULT
	release
	end
MultiArena_House1_Text::
	.string "Welcome to our ARENA town!$"
