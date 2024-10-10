import tkinter as tk
from tkinter import messagebox
import datetime
import matplotlib.pyplot as plt
from collections import defaultdict

class Person:
    def __init__(self, card_id):
        self.card_id = card_id 
        self.entry_time = None
    
    def check_in(self):
        """
        Records the current time as the check-in time for the person.
        """
        self.entry_time = datetime.datetime.now()

    def check_out(self):
        """
        Records the current time and calculates the time spent in the gym.
        
        Returns:
            timedelta: The amount of time the person spent in the gym.
        """
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
        """
        Registers a person as checked in and updates peak usage statistics.
        
        Args:
            person (Person): The person who is checking into the gym.
        """
        person.check_in()
        self.active_people[person.card_id] = person
        self.update_peak_usage()

    def person_check_out(self, card_id):
        """
        Checks a person out of the gym and removes them from the active people list.
        
        Args:
            card_id (str): The unique card ID of the person checking out.
            
        Returns:
            timedelta: The amount of time the person spent in the gym.
            None: If the person is not found in the active people list.
        """
        if card_id in self.active_people:
            person = self.active_people.pop(card_id)
            time_spent = person.check_out()
            return time_spent
        else:
            return None

    def use_machine(self, card_id, machine):
        """
        Registers usage of a machine by a person based on their card ID.
        
        Args:
            card_id (str): The card ID of the person using the machine.
            machine (Machine): The machine being used by the person.
        """
        if card_id in self.active_people:
            self.muscle_group_usage[machine.muscle_group] += 1
        else:
            print("Person not found in gym")

    def update_peak_usage(self):
        """
        Updates the peak gym usage by tracking the maximum and minimum number of people in the gym at any time.
        """
        current_people = len(self.active_people)
        if current_people > self.peak_usage["max_people"]:
            self.peak_usage["max_people"] = current_people
            self.peak_usage["time_max"] = datetime.datetime.now()
        if current_people < self.peak_usage["min_people"]:
            self.peak_usage["min_people"] = current_people
            self.peak_usage["time_min"] = datetime.datetime.now()

    def show_statistics(self):
        """
        Returns the gym's peak usage statistics.
        
        Returns:
            dict: Contains the maximum and minimum number of people in the gym and the times at which these values occurred.
        """
        return self.peak_usage

    def show_muscle_usage(self):
        """
        Returns the muscle group usage statistics.
        
        Returns:
            defaultdict: Tracks how often each muscle group machine was used.
        """
        return self.muscle_group_usage

class GymSystemApp:
    def __init__(self, root, gym_system):
        self.root = root
        self.root.title("Gym Management System")
        self.gym_system = gym_system

        # Main Menu
        self.label = tk.Label(root, text="Welcome to the Gym System", font=("Helvetica", 16))
        self.label.pack(pady=20)

        self.btn_gym_stats = tk.Button(root, text="Gym Usage Statistics", command=self.show_gym_statistics)
        self.btn_gym_stats.pack(pady=10)

        self.btn_muscle_stats = tk.Button(root, text="Muscle Group Usage Statistics", command=self.show_muscle_statistics)
        self.btn_muscle_stats.pack(pady=10)

        self.btn_exit = tk.Button(root, text="Exit", command=root.quit)
        self.btn_exit.pack(pady=10)

    def show_gym_statistics(self):
        """
        Displays the gym's peak usage statistics in a message box.
        """
        stats = self.gym_system.show_statistics()
        messagebox.showinfo("Gym Usage Statistics",
                            f"Max number of people: {stats['max_people']} at {stats['time_max']}\n"
                            f"Min number of people: {stats['min_people']} at {stats['time_min']}")

    def show_muscle_statistics(self):
        """
        Displays a bar chart of the muscle group usage statistics. If no data is available, shows a message box.
        """
        muscle_usage = self.gym_system.show_muscle_usage()
        if muscle_usage:
            muscle_groups = list(muscle_usage.keys())
            usage_counts = list(muscle_usage.values())
            plt.bar(muscle_groups, usage_counts)
            plt.title("Muscle Group Usage")
            plt.xlabel("Muscle Groups")
            plt.ylabel("Usage Count")
            plt.show()
        else:
            messagebox.showinfo("Muscle Group Usage Statistics", "No muscle group data available.")
            
gym_system = GymSystem()

person1 = Person("123")
gym_system.person_check_in(person1)

person2 = Person("124")
gym_system.person_check_in(person2)

person3 = Person("125")
gym_system.person_check_in(person3)

person4 = Person("126")
gym_system.person_check_in(person4)

machine1 = Machine("001", "Chest")
gym_system.use_machine("123", machine1)

machine2 = Machine("002", "Chest")
gym_system.use_machine("124", machine2)

machine3 = Machine("003", "Arms")
gym_system.use_machine("125", machine3)

machine4 = Machine("006", "Legs")
gym_system.use_machine("126", machine4)

gym_system.person_check_out("123")
gym_system.person_check_out("124")
gym_system.person_check_out("125")

root = tk.Tk()
app = GymSystemApp(root, gym_system)
root.mainloop()