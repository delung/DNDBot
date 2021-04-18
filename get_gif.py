import random
list_of_ree_gifs = [
	"https://tenor.com/view/reeeeee-pepe-gif-18507011",
	"https://tenor.com/view/ree-reee-reeee-reeeee-scree-gif-12568403",
	"https://tenor.com/view/reee-pepe-frog-angry-angery-gif-18421495",
	"https://tenor.com/view/reee-kid-tantrums-gif-15375793",
	"https://tenor.com/view/ree-pepe-triggered-angry-ahhhh-gif-13627544",
	"https://imgur.com/G832ZHj",
	"https://media.tenor.com/images/80a6e41400305502151dab93e7a417a1/tenor.gif",
	"https://i.kym-cdn.com/photos/images/newsfeed/001/297/231/637.gif",
	"https://i.kym-cdn.com/photos/images/newsfeed/001/140/498/4a4.gif",
	"https://media.tenor.com/images/d3f53f3e3ebed32594dc9260053f2059/tenor.gif",
	"https://media.tenor.com/images/b62e18b4e1d438823377f1702bf86cca/tenor.gif"
]

list_of_ricardo_gifs = [
	"https://tenor.com/view/gogo-dancer-dance-ricardo-milos-moves-gif-12970659",
	"https://tenor.com/view/ricardo-milos-ricardo-milos-gif-13248430",
	"https://tenor.com/view/pizza-ricardo-milos-flick-gif-14626147",
	"https://tenor.com/view/ricardo-milos-mijolnir-ricardomilos-mijolnir-ricardo-gif-14302852",
	"https://tenor.com/view/naruto-ricardo-kurama-milos-meme-gif-13427812",
	"https://tenor.com/view/ricardo-ricardo-milos-ricardo-memes-gif-14470596",
	"https://tenor.com/view/ricardo-milos-dancing-musical-gif-16819339",
	"https://thumbs.gfycat.com/MealyUniformGalapagosmockingbird-max-1mb.gif"
]

def get_ree_gif():
	return list_of_ree_gifs[random.randint(0, len(list_of_ree_gifs)-1)]

def get_ricardo_gif():
	return list_of_ricardo_gifs[random.randint(0, len(list_of_ricardo_gifs)-1)]
