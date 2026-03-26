# FocusLog
Minimal offline focus tracker with session logs and Pomodoro support
# Focus Tracker

A simple offline tool to track how much time you spend studying or taking breaks.

This project includes two versions:
- HTML (browser-based)
- Python (desktop app)

You can use either one.

---

## 🚀 HTML Version (Recommended)

**File:** `study_tracker.html`

- Open and use instantly  
- Clean and modern UI  
- Pomodoro mode included ⏱️  
- Export logs anytime  
- No setup required  

👉 Recommended for most users

---

## 🖥️ Python Version

**File:** `study_tracker.py`

- Runs as a desktop app  
- Saves logs to `study_logs.json`  
- Fully offline  

**Run:**
```bash
python study_tracker.py
```

---

## 🧠 How to Use

1. Enter your subject or task  
2. Click **Start Study** or **Start Break**  
3. Click **Stop** to log your session  
4. (Optional) Use Pomodoro mode  

---

## 📂 Data Format

Both versions use the same structure:

```json
{
  "type": "Study",
  "subject": "Example",
  "startTime": "...",
  "durationSeconds": 3600
}
```

---

## 📸 Screenshots

![Light UI_HTML](screenshots/ui-html-light.png)  
![Dark UI_HTML](screenshots/ui-html-dark.png)  
![Final UI_HTML](screenshots/overall-html-ui.png)  
![Pomodoro_HTML](screenshots/pomodoro-set-panel-html.png)  
![Past_Session_HTML](screenshots/past-sessions-panel-html.png)
![Overall_UI_PY](screenshots/overall-py-ui.png)  

---

## 🤔 Which One Should You Use?

Both work fine.

But the HTML version is:
- easier  
- faster to start  
- more polished  

---

## 🧩 Notes

- Works completely offline  
- No tracking  
- No accounts  
- Your data stays with you  

---

## 🎯 Goal

Keep it simple.  
Track your time.  
Stay consistent.
