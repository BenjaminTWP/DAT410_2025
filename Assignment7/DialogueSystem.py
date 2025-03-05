import os
import json
from nltk.tokenize import word_tokenize
from themes import *
#nltk.download("punkt") only necessary once to get the files

def load_data(filename="data.json"):
    # There was some trouble finiding the data.json file
    # even though the file was in the same path folder...
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, filename)

    with open(file_path, "r") as file:
        return json.load(file)

data = load_data()

def get_theme(input_list):
    # To extend the program, add the new class to this list of themes
    themes = [WeatherForecast(data), BusTram(data), FindRestaurant(data)]
    # we return the theme with the highest score given first input
    return max(themes, key=lambda theme: theme.calculate_score(input_list))

def dialogue_system():
    print("[Dialogue System] Good day, how could I be of help today?")
    context = {}
    while True:
        user_input = input("[You]: ")
        input_list = [s.lower() for s in word_tokenize(user_input)]
        context["last_input"] = input_list

        dialogue_theme = get_theme(input_list)
        dialogue_theme.context = context
        dialogue_theme.first(input_list)

        # Dialogue continues if not done after first input (can be)
        while not dialogue_theme.is_complete():
            follow_up = input("[You]: ")
            dialogue_theme.context["last_input"] = [s.lower() for s in word_tokenize(follow_up)]
            dialogue_theme.process_follow_up(follow_up)

if __name__ == "__main__":
    dialogue_system()