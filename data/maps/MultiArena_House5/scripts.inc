MultiArena_House5_MapScripts::
	.byte 0
MultiArena_House5_Welcome::
	lock
	faceplayer
	msgbox MultiArena_House5_Text, MSGBOX_DEFAULT
	release
	end
MultiArena_House5_Text::
	.string "Welcome to our ARENA town!$"
