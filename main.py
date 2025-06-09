from habit_tracker import main
from gui import launch_gui

if __name__ == "__main__":
    choice = input("📋 Smart Habit Tracker\nType 'gui' to launch GUI or press Enter for console: ").strip().lower()
    if choice == "gui":
        launch_gui()
    else:
        main()
