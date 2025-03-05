from nltk.tokenize import word_tokenize

class Theme:
    def __init__(self):
        self.context = {}
        
    def calculate_score(self, word_dict, input_list):

        return sum(word_dict.get(word, 0) for word in input_list)
    def first(self, input_list):
        pass
    def is_complete(self):
        pass
    def process_follow_up(self, user_input):
        pass

class WeatherForecast(Theme):
    def __init__(self, data):
        super().__init__()
        self.matching_words = {"weather": 1, "forecast": 1, "temperature": 0.9, "downfall": 0.9}
        self.data = data.get("weather", {})
        self.FRAME_day = None
        self.complete = False

    def calculate_score(self, input_list):
        return super().calculate_score(self.matching_words, input_list)

    def first(self, input_list):
        for word in input_list:
            if word in self.data:
                self.FRAME_day = word
                break
        if self.FRAME_day:
            print(f"[Dialogue System] The weather {self.FRAME_day} is {self.data.get(self.FRAME_day)}.")
            self.complete = True
        else:
            print("[Dialogue System] Which weekday did you need the weather forecast for?")

    def is_complete(self):
        return self.complete

    def process_follow_up(self, user_input):
        input_list = word_tokenize(user_input.lower())
        for word in input_list:
            if word in self.data:
                self.FRAME_day = word
                print(f"[Dialogue System] Okay well the weather at {self.FRAME_day} is {self.data.get(self.FRAME_day)}.")
                self.complete = True
                return
        print("[Dialogue System] I didn't quite catch the day. Could you clarify what weekday (monday-sunday) you meant?")

class FindRestaurant(Theme):
    def __init__(self, data):
        super().__init__()
        self.matching_words = {"restaurant": 1, "food": 0.9, "eat": 0.5, "booking": 0.5}
        self.data = data.get("restaurants", {})
        self.HISTORY_cheap = None
        self.FRAME_cuisine = None
        self.complete = False

    def calculate_score(self, input_list):
        return super().calculate_score(self.matching_words, input_list)

    def first(self, input_list):
        if "cheap" in input_list:
            self.HISTORY_cheap = True
        elif "expensive" in input_list:
            self.HISTORY_cheap = False
        for word in input_list:
            if word in self.data.keys():
                self.FRAME_cuisine = word
                break
        if self.FRAME_cuisine:
            self.recommend_restaurant()
        else:
            print("[Dialogue System] What type of cuisine are you interested in?")

    def is_complete(self):
        return self.complete

    def process_follow_up(self, user_input):
        input_list = word_tokenize(user_input.lower())
        for word in input_list:
            if word in self.data.keys():
                self.FRAME_cuisine = word
                self.recommend_restaurant()
                return
        print("[Dialogue System] I didn't catch the cuisine. Could you clarify what cuisine you are interested in?")

    def recommend_restaurant(self):
        restaurant_choice = self.data.get(self.FRAME_cuisine, None)
        if restaurant_choice:
            if self.HISTORY_cheap is not None:
                if self.HISTORY_cheap:
                    print(f"[Dialogue System] I recommend the budget-friendly {restaurant_choice}.")
                else:
                    print(f"[Dialogue System] I recommend {restaurant_choice}.")
            else:
                print(f"[Dialogue System] I recommend {restaurant_choice}.")
            self.complete = True
        else:
            print("[Dialogue System] I could not find a restaurant found for that cuisine.")

class BusTram(Theme):
    def __init__(self, data):
        super().__init__()
        self.matching_words = {"tram": 1, "bus": 1, "travel": 0.6, "stop": 0.5}
        self.data = data.get("bus_tram", {})
        self.FRAME_from = None
        self.FRAME_to = None
        self.FRAME_time = None  # "morning", "lunch", "afternoon"
        self.complete = False

        self.possible_stops = {"centralstationen", "chalmers", "korsvagen"}
        self.possible_times = {"morning", "lunch", "afternoon"}

    def calculate_score(self, input_list):
        return super().calculate_score(self.matching_words, input_list)

    def parse_tokens(self, tokens):
        # we find the time possible time slot
        for token in tokens:
            if token in self.possible_times:
                self.FRAME_time = token

        # we find the possible bus/tram stop
        found_stops = [token for token in tokens if token in self.possible_stops]
        if found_stops:
            if not self.FRAME_from:
                self.FRAME_from = found_stops[0]

            for stop in found_stops:
                if stop != self.FRAME_from:
                    self.FRAME_to = stop
                    break

    def first(self, input_list):
        self.parse_tokens(input_list)

        if not self.FRAME_from:
            print("[Dialogue System] Where are you traveling from?")
            return
        if not self.FRAME_to:
            print("[Dialogue System] Where are you traveling to?")
            return
        if not self.FRAME_time:
            print("[Dialogue System] When are you traveling? (morning, lunch, afternoon)")
            return

        schedule = self.data.get(self.FRAME_time, {}).get(self.FRAME_from, {}).get(self.FRAME_to)
        if schedule:
            print(f"[Dialogue System] The next {self.FRAME_time} tram/bus from {self.FRAME_from} to {self.FRAME_to} is at {schedule}.")
            self.complete = True
        else:
            print("[Dialogue System] I couldn't find a schedule for that route. Could you provide more details?")

    def is_complete(self):
        return self.complete

    def process_follow_up(self, user_input):
        tokens = [t.lower() for t in word_tokenize(user_input)]
        self.parse_tokens(tokens)

        if not self.FRAME_from:
            for token in tokens:
                if token in self.possible_stops:
                    self.FRAME_from = token
                    break
            if not self.FRAME_from:
                print("[Dialogue System] Where are you traveling from?")
                return

        if not self.FRAME_to:
            for token in tokens:
                if token in self.possible_stops and token != self.FRAME_from:
                    self.FRAME_to = token
                    break
            if not self.FRAME_to:
                print("[Dialogue System] Where are you traveling to?")
                return

        if not self.FRAME_time:
            for token in tokens:
                if token in self.possible_times:
                    self.FRAME_time = token
                    break
            if not self.FRAME_time:
                print("[Dialogue System] When are you traveling? (morning, lunch, afternoon)")
                return

        schedule = self.data.get(self.FRAME_time, {}).get(self.FRAME_from, {}).get(self.FRAME_to)
        if schedule:
            print(f"[Dialogue System] The next {self.FRAME_time} tram/bus from {self.FRAME_from} to {self.FRAME_to} is at {schedule}.")
            self.complete = True
        else:
            print("[Dialogue System] I couldn't find a matching schedule. Could you clarify the details?")