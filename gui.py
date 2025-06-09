import tkinter as tk
from tkinter import messagebox, simpledialog
from habit_tracker import load_data, save_data, datetime, timedelta

def launch_gui():
    data = load_data()

    def add_habits_gui():
        habits_input = simpledialog.askstring("Add Habit(s)", "Enter habit(s) separated by commas:")
        if habits_input:
            new_habits = habits_input.split(",")
            added = 0
            for raw in new_habits:
                habit = raw.strip()
                if habit and habit not in data["habits"]:
                    data["habits"].append(habit)
                    added += 1
            if added:
                messagebox.showinfo("Success", f"Added {added} new habit(s).")
            else:
                messagebox.showinfo("Info", "No new habits added or they already exist.")
            save_data(data)

    def mark_today_gui():
        today = datetime.today().strftime('%Y-%m-%d')
        if today not in data["progress"]:
            data["progress"][today] = {}

        if not data["habits"]:
            messagebox.showwarning("No Habits", "Please add habits first.")
            return

        for habit in data["habits"]:
            result = messagebox.askyesno("Daily Check-in", f"Did you do '{habit}' today?")
            data["progress"][today][habit] = result

        save_data(data)
        messagebox.showinfo("Done", "Progress recorded for today!")

    def show_summary_gui():
        today = datetime.today()
        last_7_days = [(today - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(7)]

        summary = ""
        for habit in data["habits"]:
            count = 0
            for day in last_7_days:
                if data["progress"].get(day, {}).get(habit):
                    count += 1
            summary += f"{habit}: {count}/7 days\n"

        messagebox.showinfo("Weekly Summary", summary or "No data yet.")

    def show_streaks_gui():
        today = datetime.today()
        summary = ""

        for habit in data["habits"]:
            streak = 0
            for i in range(100):
                day = (today - timedelta(days=i)).strftime('%Y-%m-%d')
                if data["progress"].get(day, {}).get(habit):
                    streak += 1
                else:
                    break
            summary += f"{habit}: {streak}-day streak\n"

        messagebox.showinfo("Current Streaks", summary or "No streaks found.")

    def on_exit():
        save_data(data)
        root.destroy()

    # GUI Layout
    root = tk.Tk()
    root.title("Smart Habit Tracker")
    root.geometry("300x300")

    tk.Button(root, text="Add Habit(s)", width=25, command=add_habits_gui).pack(pady=10)
    tk.Button(root, text="Mark Today's Progress", width=25, command=mark_today_gui).pack(pady=10)
    tk.Button(root, text="Weekly Summary", width=25, command=show_summary_gui).pack(pady=10)
    tk.Button(root, text="View Streaks", width=25, command=show_streaks_gui).pack(pady=10)
    tk.Button(root, text="Exit", width=25, command=on_exit).pack(pady=10)

    root.mainloop()

if __name__ == "__main__": 
    launch_gui()
