import json
import os

class JsonManagement:
    def __init__(self):
        try:
            try:
                with open(os.path.join(os.getcwd(), "assets/chats.json"), "r",
                        encoding='UTF-8') as chat_json:
                    self.chats = json.loads(chat_json.read())
                with open(os.path.join(os.getcwd(), "assets/player_data.json"), "r",
                        encoding='UTF-8') as player_data_json:
                    self.player_data = json.loads(player_data_json.read())
                self.categories = []
                for file in os.listdir(os.path.join(os.getcwd(), "assets/categories")):
                    if file.lower().endswith(".json"):
                        with open(os.path.join(os.getcwd(), "assets/categories", file), "r",
                                encoding='UTF-8') as categories_json:
                            this_load = json.loads(categories_json.read())

                        if ("name" and "words") in this_load:
                            if (len(this_load["name"]) or len(this_load["words"])) != 0:
                                self.categories.append(this_load)

                if len(self.categories) == 0:
                    os.system("cls")
                    print("ERROR: No categories found in \"assets/categories\"")
                    input()
                    exit()

            #If any JSON file is empty:
            except json.JSONDecodeError as failed:
                os.system("cls")
                print("ERROR: Failed to decode file \"" + failed + "\"")
                input()
                exit()

        #If any JSON file cannot be found:
        except FileNotFoundError as missing:
            os.system("cls")
            print("ERROR: File \"" + missing.filename.split("/")[1] + "\" not found")
            input()
            exit()


    def write_json(self, data):
        with open(os.path.join(os.getcwd(), "assets/player_data.json"), "w",
                encoding='UTF-8') as file:
            json.dump(data, file, indent=4)
