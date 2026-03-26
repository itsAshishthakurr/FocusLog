# FocusLog - Your Personal Study & Time Tracker

FocusLog is a lightweight, offline study and time-tracking application designed to help you stay productive. It allows you to track study sessions and breaks, manually log past activities, and use a built-in timer to maintain focus.

The project offers two distinct versions with identical core features: a modern browser-based HTML version and a standalone Python desktop application.

##Features
-Provides Long study sessions(typical study sessions) and short study sessions(Pomodoro).
-Let's you add past sessions with time and date.
-Let's you add breaks.
-Let's you name subjects/tasks.
-Let's you delete sutdy/tasks log which you created because you simply forgot to turn of the timer.
-Let's you export your logs to a json file.
 

## 🚀 Two Ways to Use FocusLog

### 1. HTML Version (Recommended 🌟)
A polished, modern interface with a built-in dark mode toggle. It runs entirely in your web browser.

- **File:** `focuslog.html`
- **How to use:** Simply double-click `focuslog.html` to open it in your preferred web browser. No installation or internet connection required.
- **Features:** Clean UI, Pomodoro mode, and an Export button.
- **Data Storage:** Uses your browser's Local Storage to save your history. Note: Clearing your browser data may erase your logs.

### 2. Python Version (Desktop App 🐍)
A standalone desktop application built with Python and Tkinter.

- **File:** `focuslog.py`
- **How to use:** 
  - Option A: Double-click `focuslog.py` to run it directly (a terminal window will briefly appear in the background). You can minimize the terminal.
  - Option B: Open your terminal or command prompt in the project folder and run `python focuslog.py`.

- **Requirements:** Requires Python to be installed on your system.
- **Data Storage:** Automatically creates and saves your history to a secure `study_logs.json` file in the same folder. This makes it very easy to backup or view your data manually.

---

## ⚙️ How It Works
1. **Subject/Task:** Enter the name of the subject or task you're working on (e.g., "Calculus", "Reading").

2. **Start Timer:** Click "▶ Study" to start tracking a study session, or "☕ Break" for a break.

3. **Pomodoro Mode:** Use the built-in Pomodoro timer to work in focused bursts (defaults to 25 minutes).

4. **Stop & Log:** When you're done, click "⏹ Stop" to save the session to your Activity History.

5. **Add Past Session:** Forgot to start the timer? No problem. Use the "+ Add Past Session" button to log it manually.

---

## 📂 Data Format (Python Version)
If you use the Python version, your logs are saved in `study_logs.json` in a simple, human-readable format:

```json
[
  {
    "type": "Study",
    "subject": "Mathematics",
    "startTime": "2023-10-27T14:30:00",
    "durationSeconds": 3600
  }
]
```

## 📝 Note
Both versions are completely offline and do the exact same thing.
We recommend the HTML version because it is simpler, more polished,and requires nothing more than a browser
But use whichever feels easiest for your workflow!

Happy Studying!