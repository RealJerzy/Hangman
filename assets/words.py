from random import choice

animals = ["puppy", "cat", "monkey", "giraffe", "rhino", "tiger", "bear", "swan", "gerbil", "leopard", "mouse", "squirrel", "bullfinch", "brown hare", "sheep", "hammerhead", "snail", "frog", "budgerigar", "chameleon"]
subjects = ["mathematics", "mother tongue", "chemistry", "physics", "domestic science", "social studies", "health education", "biology", "geography", "visual arts", "religious education", "psychology", "philosophy", "history", "ethics"]
kitchen = ["frying pan", "pot", "spatula", "microwave oven", "oven", "range hood", "coffee maker", "dining table", "toaster", "refrigerator", "plate", "fork", "knife", "spoon", "dishwasher", "potholder", "freezer", "kettle", "cruet", "blender"]
food = ["apple", "toast", "rye bread", "banana", "orange", "mandarin", "cheese", "margarine", "ham", "cucumber", "tomato", "grape", "bun", "macaroni", "pasta", "spaghetti", "yoghurt", "ketchup", "mustard", "whipped cream"]
drinks = ["water", "milk", "soda", "fizzy drink", "glogg", "juice soup", "beer", "coffee", "tea", "hot chocolate"]
stuff = ["candle", "painting", "pillow", "bed", "chair", "lawn", "television", "artwork", "carpet", "bookshelf", "computer", "desk lamp", "printer", "headphones", "mechanical pencil", "pencil", "pen", "balloon", "football", "basketball", "bowling ball", "hot air balloon", "system unit"]
categories = [animals, subjects, kitchen, food, drinks, stuff]

custom = []

def getWord(gamemode, category):
    if gamemode == 1:
        if category == 6:
            word = choice(choice([animals, subjects, kitchen, food, drinks, stuff]))

        else:
            word = choice(categories[category])

    else:
        word = choice(custom)
    
    return word 