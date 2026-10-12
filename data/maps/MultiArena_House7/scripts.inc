MultiArena_House7_MapScripts::
	.byte 0
MultiArena_House7_Welcome::
	lock
	faceplayer
	msgbox MultiArena_House7_Text, MSGBOX_DEFAULT
	release
	end
MultiArena_House7_Text::
	.string "Welcome to our ARENA town!$"
