#Import libraries
import os
import json
from datetime import datetime, timedelta

Data_File ="habits.json"

def main():
    data = load_data()

    while True:
        print("\n📋 Smart Habit Tracker")
        print("1. Add habit(s)")
        print("2. Mark today's progress")
        print("3. View weekly summary")
        print("4. Exit")
        choice = input("Choose an option (1-4): ").strip()

        if choice == "1":
            add_habit(data)
        elif choice == "2":
            mark_progress(data)
        elif choice == "3":
            view_summary(data)
        elif choice == "4":
            save_data(data)
            print("Progress saved. Goodbye!")
            break
        else:
            print("Invalid option. Try again.")



#Load data or create a data file if one doesnot exists
def load_data():
    """
    This function:Tries to read from a file named habits.json
    If the file doesnot exist, it creates a new structure with:
    An empty habit list
    An empty progress dictionary
    """
    if os.path.exists(Data_File):
        with open(Data_File, "r") as file:
            return json.load(file)
    else:
        return {
            "habits": [],
            "progress": {}
        }
    
#This function will save the habit data back into the habits.json file.
def save_data(data):
    with open(Data_File, "w") as file:
        json.dump(data, file, indent= 4)

def add_habit(data):
    """
    Handles one or many habits
    Uses simple loops and if statements
    Skips empty inputs and duplicates
    """
    new_input = input("Enter habit(s) to track (one or more, separated by commas): ").strip()

    if not new_input:
        print("No input provided.")
        return

    new_habits_raw = new_input.split(",")
    added = 0

    for raw in new_habits_raw:
        habit = raw.strip()
        if habit == "":
            continue
        if habit not in data["habits"]:
            data["habits"].append(habit)
            added += 1
        else:
            print(f"Habit '{habit}' is already being tracked.")

    if added:
        print(f"{added} new habit(s) added.")
    else:
        print("No new habits were added.")

def mark_progress(data):
    today = datetime.today().strftime('%Y-%m-%d')

    if not data["habits"]:
        print("No habits to track yet. Add some first.")
        return

    if today in data["progress"]:
        overwrite = input("You've already marked today. Overwrite? (y/n): ").lower()
        if overwrite != "y":
            print("Skipped updating today's progress.")
            return

    data["progress"][today] = {}

    print(f"\nMark your progress for {today}:")
    for habit in data["habits"]:
        answer = input(f"Did you do '{habit}' today? (y/n): ").lower()
        data["progress"][today][habit] = (answer == "y")

    print("Today's progress recorded!")



def view_summary(data):
    print("\n=== Weekly Summary ===")

    if not data["habits"]:
        print("No habits to summarize.")
        return

    today = datetime.today()
    last_7_days = []
    for i in range(7):
        day = (today - timedelta(days=i)).strftime('%Y-%m-%d')
        last_7_days.append(day)

    for habit in data["habits"]:
        count = 0
        for day in last_7_days:
            if data["progress"].get(day, {}).get(habit):
                count += 1
        print(f"{habit}: {count}/7 days completed")

if __name__ == "__main__":
    main()


    