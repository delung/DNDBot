import random
list_of_ree_gifs = [
	"https://tenor.com/view/reeeeee-pepe-gif-18507011",
	"https://tenor.com/view/ree-reee-reeee-reeeee-scree-gif-12568403",
	"https://tenor.com/view/reee-pepe-frog-angry-angery-gif-18421495",
	"https://tenor.com/view/reee-kid-tantrums-gif-15375793",
	"https://tenor.com/view/ree-pepe-triggered-angry-ahhhh-gif-13627544"
]

list_of_ricardo_gifs = [
	"https://tenor.com/view/gogo-dancer-dance-ricardo-milos-moves-gif-12970659",
	"https://tenor.com/view/ricardo-milos-ricardo-milos-gif-13248430",
	"https://tenor.com/view/pizza-ricardo-milos-flick-gif-14626147",
	"https://tenor.com/view/ricardo-milos-mijolnir-ricardomilos-mijolnir-ricardo-gif-14302852"
]

def get_ree_gif():
	return list_of_ree_gifs[random.randint(0, len(list_of_ree_gifs)-1)]

def get_ricardo_gif():
	return list_of_ricardo_gifs[random.randint(0, len(list_of_ricardo_gifs)-1)]