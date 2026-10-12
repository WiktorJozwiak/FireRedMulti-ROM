MultiArena_House3_MapScripts::
	.byte 0
MultiArena_House3_Welcome::
	lock
	faceplayer
	msgbox MultiArena_House3_Text, MSGBOX_DEFAULT
	release
	end
MultiArena_House3_Text::
	.string "Welcome to our ARENA town!$"
