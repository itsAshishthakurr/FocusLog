import tkinter as tk
from tkinter import messagebox, simpledialog
from datetime import datetime, date
import time
import json
import os

LOG_FILE = "study_logs.json"

def load_logs():
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, 'r') as f:
                logs = json.load(f)
                logs.sort(key=lambda x: datetime.fromisoformat(x['startTime']), reverse=True)
                return logs
        except:
            return []
    return []

def save_logs(logs):
    with open(LOG_FILE, 'w') as f:
        json.dump(logs, f, indent=4)


class StudyTracker:
    def __init__(self, root):
        self.root = root
        root.title("FocusLog")
        root.configure(bg="#f0f4f8")
        root.resizable(False, False)

        self.logs = load_logs()
        self.is_running = False
        self.start_time = 0       # actual epoch time when session started
        self.elapsed = 0
        self.mode = None

        self.pomodoro_mode = False
        self.pomo_duration = 1500

        # ── Variables ──────────────────────────────────────
        self.timer_var = tk.StringVar(value="00:00:00")
        self.mode_var  = tk.StringVar(value="Ready to Start")
        self.subject_var = tk.StringVar(value="Focus")

        # ── Header ─────────────────────────────────────────
        header = tk.Frame(root, bg="#1e293b", pady=10)
        header.pack(fill=tk.X)
        tk.Label(header, text="FocusLog", font=("Consolas", 22, "bold"),
                 bg="#1e293b", fg="#f8fafc").pack()

        # ── Main Card ──────────────────────────────────────
        card = tk.Frame(root, bg="white", padx=20, pady=16,
                        relief=tk.FLAT, bd=0)
        card.pack(padx=24, pady=16, fill=tk.X)

        tk.Label(card, text="Subject / Task", font=("Consolas", 9),
                 fg="#6b7280", bg="white").pack(anchor="w")
        self.entry = tk.Entry(card, textvariable=self.subject_var,
                              font=("Consolas", 11), relief=tk.FLAT,
                              bd=1, highlightthickness=1,
                              highlightbackground="#d1d5db",
                              highlightcolor="#0e7490")
        self.entry.pack(fill=tk.X, pady=(2, 10), ipady=5)

        tk.Label(card, textvariable=self.mode_var, font=("Consolas", 9),
                 fg="#6b7280", bg="white").pack()
        tk.Label(card, textvariable=self.timer_var,
                 font=("Consolas", 36, "bold"),
                 fg="#1e293b", bg="white").pack(pady=(0, 12))

        # ── Button Row 1 ───────────────────────────────────
        btn_row1 = tk.Frame(card, bg="white")
        btn_row1.pack(pady=(0, 6))

        self._btn(btn_row1, "▶  Study",  "#0e7490", "white",
                  lambda: self.start("study")).pack(side=tk.LEFT, padx=4)
        self._btn(btn_row1, "☕  Break",  "#fbbf24", "#1e293b",
                  lambda: self.start("break")).pack(side=tk.LEFT, padx=4)
        self._btn(btn_row1, "⏹  Stop",   "#ef4444", "white",
                  self.stop).pack(side=tk.LEFT, padx=4)

        # ── Button Row 2 ───────────────────────────────────
        btn_row2 = tk.Frame(card, bg="white")
        btn_row2.pack()

        self._btn(btn_row2, "⏱  Pomodoro", "#9333ea", "white",
                  self.toggle_pomodoro).pack(side=tk.LEFT, padx=4)
        self._btn(btn_row2, "+ Add Past Session", "#0f766e", "white",
                  self.open_past_session).pack(side=tk.LEFT, padx=4)

        # ── History ────────────────────────────────────────
        hist_label = tk.Frame(root, bg="#f0f4f8")
        hist_label.pack(fill=tk.X, padx=24, pady=(4, 0))
        tk.Label(hist_label, text="Activity History",
                 font=("Consolas", 12, "bold"),
                 fg="#1e293b", bg="#f0f4f8").pack(anchor="w")
        tk.Frame(hist_label, bg="#d1d5db", height=1).pack(fill=tk.X, pady=(4, 0))

        # Scrollable log area
        outer = tk.Frame(root, bg="#f0f4f8")
        outer.pack(fill=tk.BOTH, expand=True, padx=24, pady=8)

        self.canvas = tk.Canvas(outer, bg="#f0f4f8", bd=0,
                                highlightthickness=0, height=300)
        scrollbar = tk.Scrollbar(outer, orient="vertical",
                                 command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.log_frame = tk.Frame(self.canvas, bg="#f0f4f8")
        self.canvas_window = self.canvas.create_window(
            (0, 0), window=self.log_frame, anchor="nw")

        self.log_frame.bind("<Configure>", self._on_frame_configure)
        self.canvas.bind("<Configure>", self._on_canvas_configure)

        self.render_logs()

    # ── Helpers ───────────────────────────────────────────

    def _btn(self, parent, text, bg, fg, cmd):
        return tk.Button(parent, text=text, bg=bg, fg=fg,
                         font=("Consolas", 9, "bold"),
                         relief=tk.FLAT, cursor="hand2",
                         padx=10, pady=6, command=cmd,
                         activebackground=bg, activeforeground=fg)

    def _on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_canvas_configure(self, event):
        self.canvas.itemconfig(self.canvas_window, width=event.width)

    def fmt(self, seconds):
        h = seconds // 3600
        m = (seconds % 3600) // 60
        s = seconds % 60
        return f"{h:02d}:{m:02d}:{s:02d}"

    def duration_str(self, seconds):
        h = seconds // 3600
        m = (seconds % 3600) // 60
        s = seconds % 60
        parts = []
        if h: parts.append(f"{h}h")
        if m: parts.append(f"{m}m")
        if s or not parts: parts.append(f"{s}s")
        return " ".join(parts)

    # ── Pomodoro ──────────────────────────────────────────

    def toggle_pomodoro(self):
        self.pomodoro_mode = not self.pomodoro_mode
        if self.pomodoro_mode:
            minutes = simpledialog.askinteger(
                "Pomodoro", "Minutes:", initialvalue=25,
                minvalue=1, maxvalue=240)
            if not minutes:
                self.pomodoro_mode = False
                return
            self.pomo_duration = minutes * 60
            self.mode_var.set(f"Pomodoro ({minutes} min)")
        else:
            self.mode_var.set("Ready to Start")

    # ── Timer Core ────────────────────────────────────────

    def start(self, mode):
        if self.is_running:
            return
        self.mode = mode
        self.is_running = True
        self.start_time = time.time()
        self.elapsed = 0
        self.entry.config(state=tk.DISABLED)
        self._tick()

    def _tick(self):
        if not self.is_running:
            return
        self.elapsed = int(time.time() - self.start_time)

        if self.pomodoro_mode:
            remaining = self.pomo_duration - self.elapsed
            if remaining <= 0:
                self.timer_var.set("00:00:00")
                messagebox.showinfo("FocusLog", "Pomodoro complete!")
                self.reset()
                return
            self.timer_var.set(self.fmt(remaining))
        else:
            self.timer_var.set(self.fmt(self.elapsed))

        self.root.after(1000, self._tick)

    def stop(self):
        if not self.is_running:
            return
        if self.elapsed < 5:
            self.reset()
            return
        confirmed = messagebox.askyesno(
            "FocusLog – Confirm Log",
            f"Stop and log this {'Study' if self.mode == 'study' else 'Break'} "
            f"session?\n\nDuration: {self.duration_str(self.elapsed)}")
        if not confirmed:
            return
        self._save_session(
            stype="Study" if self.mode == "study" else "Break",
            subject=self.subject_var.get(),
            start_epoch=self.start_time,
            duration_seconds=self.elapsed
        )
        self.reset()

    def reset(self):
        self.is_running = False
        self.mode = None
        self.elapsed = 0
        self.start_time = 0
        self.timer_var.set("00:00:00")
        self.mode_var.set("Ready to Start")
        self.entry.config(state=tk.NORMAL)

    def _save_session(self, stype, subject, start_epoch, duration_seconds):
        log = {
            "type": stype,
            "subject": subject or "Uncategorized Focus",
            "startTime": datetime.fromtimestamp(start_epoch).isoformat(),
            "durationSeconds": duration_seconds
        }
        self.logs.insert(0, log)
        save_logs(self.logs)
        self.render_logs()

    # ── Add Past Session ──────────────────────────────────

    def open_past_session(self):
        win = tk.Toplevel(self.root)
        win.title("Add Past Session")
        win.configure(bg="#f0f4f8")
        win.resizable(False, False)
        win.grab_set()

        pad = {"padx": 12, "pady": 5}

        tk.Label(win, text="Add Past Session",
                 font=("Consolas", 13, "bold"),
                 bg="#f0f4f8", fg="#1e293b").pack(**pad)

        # Subject
        tk.Label(win, text="Subject / Task", font=("Consolas", 9),
                 fg="#6b7280", bg="#f0f4f8").pack(anchor="w", padx=12)
        subj_var = tk.StringVar(value=self.subject_var.get())
        tk.Entry(win, textvariable=subj_var, font=("Consolas", 10),
                 width=30).pack(**pad)

        # Type
        tk.Label(win, text="Session Type", font=("Consolas", 9),
                 fg="#6b7280", bg="#f0f4f8").pack(anchor="w", padx=12)
        type_var = tk.StringVar(value="Study")
        type_frame = tk.Frame(win, bg="#f0f4f8")
        type_frame.pack(**pad)
        for t in ["Study", "Break"]:
            tk.Radiobutton(type_frame, text=t, variable=type_var, value=t,
                           font=("Consolas", 9), bg="#f0f4f8").pack(side=tk.LEFT, padx=6)

        # Date
        tk.Label(win, text="Date (YYYY-MM-DD)", font=("Consolas", 9),
                 fg="#6b7280", bg="#f0f4f8").pack(anchor="w", padx=12)
        date_var = tk.StringVar(value=date.today().isoformat())
        tk.Entry(win, textvariable=date_var, font=("Consolas", 10),
                 width=16).pack(**pad)

        # Time format toggle
        fmt_frame = tk.Frame(win, bg="#f0f4f8")
        fmt_frame.pack(padx=12, pady=(4,0), anchor="e")
        use24 = tk.BooleanVar(value=False)

        def refresh_labels():
            if use24.get():
                start_lbl.config(text="Start Time (HH:MM, 24h)")
                end_lbl.config(text="End Time (HH:MM, 24h)")
                start_ampm_frame.pack_forget()
                end_ampm_frame.pack_forget()
                fmt_toggle.config(text="Switch to AM/PM")
                start_hr.config(from_=0, to=23)
                end_hr.config(from_=0, to=23)
            else:
                start_lbl.config(text="Start Time")
                end_lbl.config(text="End Time")
                start_ampm_frame.pack(side=tk.LEFT, padx=2)
                end_ampm_frame.pack(side=tk.LEFT, padx=2)
                fmt_toggle.config(text="Switch to 24h")
                start_hr.config(from_=1, to=12)
                end_hr.config(from_=1, to=12)

        fmt_toggle = tk.Button(fmt_frame, text="Switch to 24h",
                               font=("Consolas", 8), fg="#6b7280",
                               bg="#e2e8f0", relief=tk.FLAT,
                               cursor="hand2",
                               command=lambda: [use24.set(not use24.get()), refresh_labels()])
        fmt_toggle.pack()

        # Start time
        start_lbl = tk.Label(win, text="Start Time", font=("Consolas", 9),
                 fg="#6b7280", bg="#f0f4f8")
        start_lbl.pack(anchor="w", padx=12)
        start_time_frame = tk.Frame(win, bg="#f0f4f8")
        start_time_frame.pack(padx=12, pady=(2,6), anchor="w")
        start_hr  = tk.Spinbox(start_time_frame, from_=1, to=12, width=3,
                               font=("Consolas", 10), format="%02.0f")
        start_hr.pack(side=tk.LEFT)
        tk.Label(start_time_frame, text=":", bg="#f0f4f8",
                 font=("Consolas",10)).pack(side=tk.LEFT)
        start_min = tk.Spinbox(start_time_frame, from_=0, to=59, width=3,
                               font=("Consolas", 10), format="%02.0f")
        start_min.pack(side=tk.LEFT)
        start_ampm_frame = tk.Frame(start_time_frame, bg="#f0f4f8")
        start_ampm = tk.StringVar(value="AM")
        tk.Radiobutton(start_ampm_frame, text="AM", variable=start_ampm,
                       value="AM", font=("Consolas",9), bg="#f0f4f8").pack(side=tk.LEFT)
        tk.Radiobutton(start_ampm_frame, text="PM", variable=start_ampm,
                       value="PM", font=("Consolas",9), bg="#f0f4f8").pack(side=tk.LEFT)
        start_ampm_frame.pack(side=tk.LEFT, padx=2)

        # End time
        end_lbl = tk.Label(win, text="End Time", font=("Consolas", 9),
                 fg="#6b7280", bg="#f0f4f8")
        end_lbl.pack(anchor="w", padx=12)
        end_time_frame = tk.Frame(win, bg="#f0f4f8")
        end_time_frame.pack(padx=12, pady=(2,6), anchor="w")
        end_hr  = tk.Spinbox(end_time_frame, from_=1, to=12, width=3,
                             font=("Consolas", 10), format="%02.0f")
        end_hr.pack(side=tk.LEFT)
        tk.Label(end_time_frame, text=":", bg="#f0f4f8",
                 font=("Consolas",10)).pack(side=tk.LEFT)
        end_min = tk.Spinbox(end_time_frame, from_=0, to=59, width=3,
                             font=("Consolas", 10), format="%02.0f")
        end_min.pack(side=tk.LEFT)
        end_ampm_frame = tk.Frame(end_time_frame, bg="#f0f4f8")
        end_ampm = tk.StringVar(value="AM")
        tk.Radiobutton(end_ampm_frame, text="AM", variable=end_ampm,
                       value="AM", font=("Consolas",9), bg="#f0f4f8").pack(side=tk.LEFT)
        tk.Radiobutton(end_ampm_frame, text="PM", variable=end_ampm,
                       value="PM", font=("Consolas",9), bg="#f0f4f8").pack(side=tk.LEFT)
        end_ampm_frame.pack(side=tk.LEFT, padx=2)

        def get_hour_24(spinbox, ampm_var):
            """Convert spinbox (1-12) + AM/PM → 24h integer."""
            try: h = int(spinbox.get())
            except: return None
            if not use24.get():
                ap = ampm_var.get()
                if ap == "AM":
                    if h == 12: h = 0
                elif h != 12:
                    h += 12
            return h

        def get_minute(spinbox):
            try: return int(spinbox.get())
            except: return None

        # Still ongoing?
        ongoing_var = tk.BooleanVar(value=False)

        def toggle_ongoing():
            hide = ongoing_var.get()
            if hide:
                end_lbl.pack_forget()
                end_time_frame.pack_forget()
            else:
                end_lbl.pack(anchor="w", padx=12, before=ongoing_chk)
                end_time_frame.pack(padx=12, pady=(2,6), anchor="w", before=ongoing_chk)

        ongoing_chk = tk.Checkbutton(
            win, text="Still ongoing (timer will resume from start time)",
            variable=ongoing_var, font=("Consolas", 9),
            bg="#f0f4f8", fg="#0f766e",
            command=toggle_ongoing)
        ongoing_chk.pack(padx=12, pady=(4, 0), anchor="w")

        err_lbl = tk.Label(win, text="", font=("Consolas", 9),
                           fg="#ef4444", bg="#f0f4f8")
        err_lbl.pack()

        def submit():
            # ── Validate date ──
            try:
                d = date.fromisoformat(date_var.get().strip())
            except ValueError:
                err_lbl.config(text="Invalid date. Use YYYY-MM-DD.")
                return
            today = date.today()
            if d > today:
                err_lbl.config(text="Date cannot be in the future.")
                return

            # ── Validate start time ──
            sh = get_hour_24(start_hr, start_ampm)
            sm = get_minute(start_min)
            if sh is None or sm is None or not (0 <= sh <= 23) or not (0 <= sm <= 59):
                err_lbl.config(text="Invalid start time.")
                return
            if use24.get():
                # In 24h mode allow 0-23 range in spinbox
                pass
            start_dt = datetime(d.year, d.month, d.day, sh, sm)
            now_dt = datetime.now()
            if start_dt >= now_dt:
                err_lbl.config(text="Start time cannot be in the future.")
                return

            ongoing = ongoing_var.get()

            if ongoing:
                if self.is_running:
                    err_lbl.config(text="A session is already running. Stop it first.")
                    return
                self.mode = "study" if type_var.get() == "Study" else "break"
                self.is_running = True
                self.start_time = start_dt.timestamp()
                self.elapsed = int(time.time() - self.start_time)
                label = "STUDYING" if self.mode == "study" else "ON BREAK"
                self.mode_var.set(f"{label} (resumed): {subj_var.get()}")
                self.subject_var.set(subj_var.get())
                self.entry.config(state=tk.DISABLED)
                self._tick()
                win.destroy()
            else:
                # ── Validate end time ──
                eh = get_hour_24(end_hr, end_ampm)
                em = get_minute(end_min)
                if eh is None or em is None or not (0 <= eh <= 23) or not (0 <= em <= 59):
                    err_lbl.config(text="Invalid end time.")
                    return
                end_dt = datetime(d.year, d.month, d.day, eh, em)
                if end_dt >= now_dt:
                    err_lbl.config(text="End time cannot be in the future.")
                    return
                if end_dt <= start_dt:
                    err_lbl.config(text="End time must be after start time.")
                    return

                duration = int((end_dt - start_dt).total_seconds())
                confirmed = messagebox.askyesno(
                    "Confirm Past Session",
                    f"Log {type_var.get()} session?\n"
                    f"Subject: {subj_var.get()}\n"
                    f"Date: {d.isoformat()}\n"
                    f"Duration: {self.duration_str(duration)}",
                    parent=win)
                if confirmed:
                    self._save_session(
                        stype=type_var.get(),
                        subject=subj_var.get(),
                        start_epoch=start_dt.timestamp(),
                        duration_seconds=duration
                    )
                    win.destroy()

        btn_row = tk.Frame(win, bg="#f0f4f8")
        btn_row.pack(pady=10)
        self._btn(btn_row, "Cancel", "#d1d5db", "#1e293b",
                  win.destroy).pack(side=tk.LEFT, padx=4)
        self._btn(btn_row, "Save Session", "#0e7490", "white",
                  submit).pack(side=tk.LEFT, padx=4)

    # ── Render Logs ───────────────────────────────────────

    def render_logs(self):
        for widget in self.log_frame.winfo_children():
            widget.destroy()

        if not self.logs:
            tk.Label(self.log_frame,
                     text="No logs yet. Start tracking your time!",
                     font=("Consolas", 9), fg="#6b7280",
                     bg="#f0f4f8").pack(pady=10)
            return

        for i, log in enumerate(self.logs):
            is_study = log["type"] == "Study"
            accent   = "#0e7490" if is_study else "#d97706"
            card_bg  = "#f0fdfa" if is_study else "#fffbeb"
            icon     = "📚" if is_study else "☕"

            row = tk.Frame(self.log_frame, bg=card_bg,
                           highlightthickness=1,
                           highlightbackground="#e5e7eb",
                           pady=6, padx=10)
            row.pack(fill=tk.X, pady=4)

            top = tk.Frame(row, bg=card_bg)
            top.pack(fill=tk.X)

            tk.Label(top, text=f"{icon} {log['type']}",
                     font=("Consolas", 10, "bold"),
                     fg=accent, bg=card_bg).pack(side=tk.LEFT)

            # Delete button
            idx = i  # capture
            del_btn = tk.Button(
                top, text="🗑 Delete",
                font=("Consolas", 8), fg="#ef4444",
                bg=card_bg, relief=tk.FLAT, cursor="hand2",
                command=lambda ix=idx: self.delete_log(ix))
            del_btn.pack(side=tk.RIGHT)

            try:
                dt = datetime.fromisoformat(log["startTime"])
                date_str = dt.strftime("%d %b %Y, %I:%M %p")
            except Exception:
                date_str = log.get("startTime", "")

            tk.Label(top, text=date_str,
                     font=("Consolas", 8), fg="#6b7280",
                     bg=card_bg).pack(side=tk.RIGHT, padx=6)

            tk.Label(row, text=log.get("subject", ""),
                     font=("Consolas", 9, "bold"),
                     fg="#1e293b", bg=card_bg).pack(anchor="w")

            tk.Label(row,
                     text=f"Duration: {self.duration_str(log['durationSeconds'])}",
                     font=("Consolas", 9), fg="#6b7280",
                     bg=card_bg).pack(anchor="w")

    def delete_log(self, index):
        log = self.logs[index]
        confirmed = messagebox.askyesno(
            "FocusLog – Delete Log",
            f"Are you sure you want to delete this log?\n\n"
            f"{log['type']} | {log.get('subject','')}\n"
            f"Duration: {self.duration_str(log['durationSeconds'])}")
        if confirmed:
            self.logs.pop(index)
            save_logs(self.logs)
            self.render_logs()


if __name__ == "__main__":
    root = tk.Tk()
    app = StudyTracker(root)
    root.mainloop()