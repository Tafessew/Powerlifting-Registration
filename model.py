# model.py 
# Date: 2025-04-29
# Author: Wada Tafesse
# Description: Contains functions for saving and loading lifter registration data using CSV files.

import csv
import os
from tkinter import messagebox  # Needed for error popup

# Represent a lifter and their data
class Lifter:
    def __init__(self, name, gender, weight_class, division, squat="", bench="", deadlift=""):
        self.name = name
        self.gender = gender
        self.weight_class = weight_class
        self.division = division
        self.squat = squat
        self.bench = bench
        self.deadlift = deadlift

    def set_attempts(self, squat, bench, deadlift):
        self.squat = squat
        self.bench = bench
        self.deadlift = deadlift

    def to_list(self):
        return [self.name, self.gender, self.weight_class, self.division,
                self.squat, self.bench, self.deadlift]

# Manages the list of lifters and file I/O
class LifterManager:
    def __init__(self, filename="registrations.csv"):
        self.filename = filename
        self.lifters = self.load_lifters()

    def add_lifter(self, lifter):
        self.lifters.append(lifter)
        self.save_lifter_to_csv(lifter)

    # Saves a single lifter to the CSV file
    def save_lifter_to_csv(self, lifter):
        file_exists = os.path.isfile(self.filename)
        try:
            with open(self.filename, mode='a', newline='') as file:
                writer = csv.writer(file)
                if not file_exists or os.path.getsize(self.filename) == 0:
                    writer.writerow(["Name", "Gender", "Weight Class", "Division", "Squat", "Bench", "Deadlift"])
                writer.writerow(lifter.to_list())
        except PermissionError:
            messagebox.showerror("Error", "Cannot write to file. Please close Excel if it's open.")

    # Loads lifters from the CSV file
    def load_lifters(self):
        lifters = []
        if os.path.exists(self.filename):
            with open(self.filename, mode='r') as file:
                reader = csv.reader(file)
                next(reader, None)  # Skip header row
                for row in reader:
                    if len(row) == 7:
                        lifters.append(Lifter(*row))
        return lifters

    # Returns formatted list of lifters
    def get_roster(self):
        return [f"{l.name}, {l.gender}, {l.weight_class}, {l.division}, "
                f"Squat: {l.squat}kg, Bench: {l.bench}kg, Deadlift: {l.deadlift}kg"
                for l in self.lifters]

    # Saves the full roster to a .txt file
    def save_roster_as_txt(self, path):
        with open(path, 'w') as f:
            for lifter in self.get_roster():
                f.write(lifter + "\n")
