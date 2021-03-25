from rolling import Rolling

async def get_help(which_command):
	help_string = "Invalid command."
	if which_command == "rolls":
		help_string = Rolling.print_help()
	elif which_command == "":
		pass
	else:
		pass
	return help_string