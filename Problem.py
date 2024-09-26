import datetime
from collections import defaultdict

class Person:
    def __init__(self, card_id):
        self.card_id = card_id 
        self.entry_time = None
        self.current_machine = None  
    
    def check_in(self):
        self.entry_time = datetime.datetime.now() 

    def check_out(self):
        time_spent = datetime.datetime.now() - self.entry_time 
        return time_spent

class Machine:
    def __init__(self, machine_id, muscle_group):
        self.machine_id = machine_id 
        self.muscle_group = muscle_group

class GymSystem:
    def __init__(self):
        self.active_people = {} 
        self.muscle_group_usage = defaultdict(int) 
        self.peak_usage = {"max_people": 0, "min_people": float('inf'), "time_max": None, "time_min": None} 
    def person_check_in(self, person):
        person.check_in()
        self.active_people[person.card_id] = person
        self.update_peak_usage()

    def person_check_out(self, card_id):
        if card_id in self.active_people:
            person = self.active_people.pop(card_id)
            time_spent = person.check_out()
            print(f"Person {card_id} was in the gym for {time_spent}")
            return time_spent
        else:
            print("Person not found")

    def use_machine(self, card_id, machine):
        if card_id in self.active_people:
            person = self.active_people[card_id]
            person.current_machine = machine
            self.muscle_group_usage[machine.muscle_group] += 1
        else:
            print("Person not found in gym")

    def update_peak_usage(self):
        current_people = len(self.active_people)
        if current_people > self.peak_usage["max_people"]:
            self.peak_usage["max_people"] = current_people
            self.peak_usage["time_max"] = datetime.datetime.now()
        if current_people < self.peak_usage["min_people"]:
            self.peak_usage["min_people"] = current_people
            self.peak_usage["time_min"] = datetime.datetime.now()

    def show_statistics(self):
        print(f"Max antal personer: {self.peak_usage['max_people']} vid {self.peak_usage['time_max']}")
        print(f"Min antal personer: {self.peak_usage['min_people']} vid {self.peak_usage['time_min']}")
        print("Muskelgrupp statistik:")
        for muscle, count in self.muscle_group_usage.items():
            print(f"{muscle}: {count} användningar")
