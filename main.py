"""GUI application for interactive fish tracking with batch processing.

Provides a modern Tkinter/ttk graphical interface for selecting video and
output folders, calibrating the arena, monitoring live per-video progress,
and calculating distance summaries. Supports parallel batch processing of
multiple videos with cancellation and persisted user settings.
"""

import json
import multiprocessing
import os
import queue
import sys
import threading
import time
import tkinter as tk
import webbrowser
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from datetime import datetime
from tkinter import filedialog, messagebox, ttk
from typing import Optional

from distance_calculator import calculate_summary
from tracker_wrapper import process_video

NUM_CORES = multiprocessing.cpu_count()
NUM_WORKERS = max(NUM_CORES * 3, 24)

SETTINGS_PATH = os.path.join(os.path.expanduser("~"), ".fishtracker_settings.json")

VIDEO_EXTENSIONS = (".mp4", ".avi", ".mov")

# --- Palette -----------------------------------------------------------
# A small, deliberate palette rather than platform defaults. Values tuned
# for contrast in both the light and dark variants below.
PALETTE = {
    "light": {
        "bg": "#f5f6fa",
        "surface": "#ffffff",
        "surface_alt": "#eef1f8",
        "border": "#dfe3ec",
        "text": "#1b1f27",
        "text_muted": "#5b6270",
        "accent": "#2f6fed",
        "accent_hover": "#2557c7",
        "accent_text": "#ffffff",
        "success": "#1a9e5c",
        "error": "#d64545",
        "warning": "#c98a12",
    },
    "dark": {
        "bg": "#15171c",
        "surface": "#1e2129",
        "surface_alt": "#262a34",
        "border": "#333844",
        "text": "#e9ebf1",
        "text_muted": "#9aa1b1",
        "accent": "#5b8cff",
        "accent_hover": "#7aa0ff",
        "accent_text": "#0b0e14",
        "success": "#3ddc84",
        "error": "#ff6b6b",
        "warning": "#e6b450",
    },
}


def get_resource_path(relative_path: str) -> str:
    """Get absolute path to resource compatible with PyInstaller and dev mode.

    Args:
        relative_path: Relative path to the resource.

    Returns:
        Absolute path to the resource.
    """
    try:
        base_path = sys._MEIPASS  # type: ignore[attr-defined]
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def load_settings() -> dict:
    """Load persisted user settings (folders, calibration) from disk.

    Returns:
        Dict of settings, empty if no settings file exists or it is invalid.
    """
    try:
        with open(SETTINGS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return {}


def save_settings(settings: dict) -> None:
    """Persist user settings (folders, calibration) to disk.

    Args:
        settings: Dict of settings to write.
    """
    try:
        with open(SETTINGS_PATH, "w", encoding="utf-8") as f:
            json.dump(settings, f, indent=2)
    except OSError:
        pass


@dataclass
class TrackingEvent:
    """A single progress event emitted from the worker thread to the UI."""

    kind: str  # "log" | "video_done" | "batch_done" | "error" | "progress"
    payload: dict = field(default_factory=dict)


class FishTrackerGUI:
    """Modern ttk GUI for FishTracker batch processing.

    Provides folder selection, arena calibration, live per-video progress,
    cancellable batch tracking, and distance summary calculation.
    """

    def __init__(self, master: tk.Tk) -> None:
        self.master = master
        master.title("FishTracker")
        master.minsize(880, 640)
        master.geometry("960x700")

        self.settings = load_settings()
        self.theme_name = self.settings.get("theme", "light")

        self.video_dir = tk.StringVar(value=self.settings.get("video_dir", ""))
        self.output_dir = tk.StringVar(value=self.settings.get("output_dir", ""))
        self.arena_width = tk.StringVar(value=str(self.settings.get("arena_width_cm", 28)))
        self.arena_height = tk.StringVar(value=str(self.settings.get("arena_height_cm", 14)))

        self.video_count = tk.StringVar(value="No folder selected")
        self.status_text = tk.StringVar(value="Ready")
        self.progress_value = tk.DoubleVar(value=0)
        self.progress_label = tk.StringVar(value="")

        self._event_queue: "queue.Queue[TrackingEvent]" = queue.Queue()
        self._worker_thread: Optional[threading.Thread] = None
        self._cancel_event = threading.Event()
        self._is_running = False

        self.style = ttk.Style(master)
        self._build_style()
        self._build_layout()
        self._poll_queue()

        master.protocol("WM_DELETE_WINDOW", self._on_close)

    # -- Styling ----------------------------------------------------------

    def _colors(self) -> dict:
        return PALETTE[self.theme_name]

    def _build_style(self) -> None:
        """Configure ttk styles for a clean, modern flat look."""
        c = self._colors()
        self.style.theme_use("clam")
        self.master.configure(bg=c["bg"])

        self.style.configure("TFrame", background=c["bg"])
        self.style.configure("Surface.TFrame", background=c["surface"])
        self.style.configure("Card.TFrame", background=c["surface"], relief="flat")

        self.style.configure(
            "TLabel", background=c["bg"], foreground=c["text"], font=("Segoe UI", 10)
        )
        self.style.configure(
            "Surface.TLabel", background=c["surface"], foreground=c["text"], font=("Segoe UI", 10)
        )
        self.style.configure(
            "Muted.TLabel", background=c["bg"], foreground=c["text_muted"], font=("Segoe UI", 9)
        )
        self.style.configure(
            "SurfaceMuted.TLabel",
            background=c["surface"],
            foreground=c["text_muted"],
            font=("Segoe UI", 9),
        )
        self.style.configure(
            "Title.TLabel",
            background=c["bg"],
            foreground=c["text"],
            font=("Segoe UI Semibold", 18),
        )
        self.style.configure(
            "Subtitle.TLabel",
            background=c["bg"],
            foreground=c["text_muted"],
            font=("Segoe UI", 10),
        )
        self.style.configure(
            "SectionHeader.TLabel",
            background=c["surface"],
            foreground=c["text"],
            font=("Segoe UI Semibold", 11),
        )

        self.style.configure(
            "TEntry",
            fieldbackground=c["surface_alt"],
            foreground=c["text"],
            bordercolor=c["border"],
            lightcolor=c["border"],
            darkcolor=c["border"],
            padding=6,
        )

        self.style.configure(
            "Accent.TButton",
            background=c["accent"],
            foreground=c["accent_text"],
            font=("Segoe UI Semibold", 10),
            padding=(14, 9),
            borderwidth=0,
        )
        self.style.map(
            "Accent.TButton",
            background=[("active", c["accent_hover"]), ("disabled", c["border"])],
            foreground=[("disabled", c["text_muted"])],
        )

        self.style.configure(
            "Secondary.TButton",
            background=c["surface_alt"],
            foreground=c["text"],
            font=("Segoe UI", 10),
            padding=(12, 8),
            borderwidth=1,
        )
        self.style.map(
            "Secondary.TButton",
            background=[("active", c["border"])],
        )

        self.style.configure(
            "Danger.TButton",
            background=c["error"],
            foreground="#ffffff",
            font=("Segoe UI Semibold", 10),
            padding=(12, 8),
            borderwidth=0,
        )
        self.style.map("Danger.TButton", background=[("disabled", c["border"])])

        self.style.configure(
            "Modern.Horizontal.TProgressbar",
            troughcolor=c["surface_alt"],
            background=c["accent"],
            bordercolor=c["surface_alt"],
            lightcolor=c["accent"],
            darkcolor=c["accent"],
            thickness=10,
        )

    # -- Layout -------------------------------------------------------------

    def _build_layout(self) -> None:
        c = self._colors()
        root = ttk.Frame(self.master, padding=0)
        root.pack(fill="both", expand=True)

        self._build_header(root)

        body = ttk.Frame(root, padding=(24, 16, 24, 24))
        body.pack(fill="both", expand=True)
        body.columnconfigure(0, weight=1)
        body.rowconfigure(3, weight=1)

        self._build_folder_card(body)
        self._build_calibration_card(body)
        self._build_actions(body)
        self._build_progress_and_log(body)

    def _build_header(self, parent: ttk.Frame) -> None:
        c = self._colors()
        header = tk.Frame(parent, bg=c["accent"], height=84)
        header.pack(fill="x")
        header.pack_propagate(False)

        left = tk.Frame(header, bg=c["accent"])
        left.pack(side="left", fill="y", padx=24)

        tk.Label(
            left, text="FishTracker", bg=c["accent"], fg=c["accent_text"],
            font=("Segoe UI Semibold", 18), anchor="w",
        ).pack(anchor="w", pady=(16, 0))
        tk.Label(
            left, text="Single-subject video tracking & space-use analysis",
            bg=c["accent"], fg=c["accent_text"], font=("Segoe UI", 9), anchor="w",
        ).pack(anchor="w")

        right = tk.Frame(header, bg=c["accent"])
        right.pack(side="right", fill="y", padx=24)
        theme_btn = tk.Label(
            right, text=("🌙 Dark" if self.theme_name == "light" else "☀️ Light"),
            bg=c["accent"], fg=c["accent_text"], font=("Segoe UI", 10), cursor="hand2",
        )
        theme_btn.pack(anchor="e", pady=(28, 0))
        theme_btn.bind("<Button-1>", lambda e: self._toggle_theme())
        self._theme_btn = theme_btn

    def _card(self, parent: ttk.Frame) -> ttk.Frame:
        c = self._colors()
        outer = tk.Frame(parent, bg=c["border"])
        inner = ttk.Frame(outer, style="Surface.TFrame", padding=16)
        inner.pack(fill="both", expand=True, padx=1, pady=1)
        return outer, inner  # type: ignore[return-value]

    def _build_folder_card(self, parent: ttk.Frame) -> None:
        outer, inner = self._card(parent)
        outer.grid(row=0, column=0, sticky="ew", pady=(0, 12))
        outer.columnconfigure(0, weight=1)
        inner.columnconfigure(1, weight=1)

        ttk.Label(inner, text="1. Select folders", style="SectionHeader.TLabel").grid(
            row=0, column=0, columnspan=3, sticky="w", pady=(0, 12)
        )

        ttk.Label(inner, text="Video folder", style="Surface.TLabel").grid(
            row=1, column=0, sticky="w", padx=(0, 10)
        )
        video_entry = ttk.Entry(inner, textvariable=self.video_dir)
        video_entry.grid(row=1, column=1, sticky="ew", pady=4)
        ttk.Button(
            inner, text="Browse…", style="Secondary.TButton", command=self._select_video_folder
        ).grid(row=1, column=2, padx=(10, 0))

        ttk.Label(inner, text="Output folder", style="Surface.TLabel").grid(
            row=2, column=0, sticky="w", padx=(0, 10)
        )
        output_entry = ttk.Entry(inner, textvariable=self.output_dir)
        output_entry.grid(row=2, column=1, sticky="ew", pady=4)
        ttk.Button(
            inner, text="Browse…", style="Secondary.TButton", command=self._select_output_folder
        ).grid(row=2, column=2, padx=(10, 0))

        ttk.Label(inner, textvariable=self.video_count, style="SurfaceMuted.TLabel").grid(
            row=3, column=0, columnspan=3, sticky="w", pady=(10, 0)
        )

        self.video_dir.trace_add("write", lambda *_: self._refresh_video_count())
        self._refresh_video_count()

    def _build_calibration_card(self, parent: ttk.Frame) -> None:
        outer, inner = self._card(parent)
        outer.grid(row=1, column=0, sticky="ew", pady=(0, 12))
        outer.columnconfigure(0, weight=1)

        ttk.Label(inner, text="2. Calibrate arena", style="SectionHeader.TLabel").grid(
            row=0, column=0, columnspan=4, sticky="w", pady=(0, 4)
        )
        ttk.Label(
            inner,
            text="Real-world dimensions of the tank/arena visible in frame, used to convert pixel distance to cm.",
            style="SurfaceMuted.TLabel",
            wraplength=760,
            justify="left",
        ).grid(row=1, column=0, columnspan=4, sticky="w", pady=(0, 12))

        ttk.Label(inner, text="Width (cm)", style="Surface.TLabel").grid(row=2, column=0, sticky="w")
        ttk.Entry(inner, textvariable=self.arena_width, width=10).grid(
            row=2, column=1, sticky="w", padx=(8, 24)
        )
        ttk.Label(inner, text="Height (cm)", style="Surface.TLabel").grid(row=2, column=2, sticky="w")
        ttk.Entry(inner, textvariable=self.arena_height, width=10).grid(
            row=2, column=3, sticky="w", padx=(8, 0)
        )

    def _build_actions(self, parent: ttk.Frame) -> None:
        row = ttk.Frame(parent, style="TFrame")
        row.grid(row=2, column=0, sticky="ew", pady=(0, 12))

        self.start_btn = ttk.Button(
            row, text="▶  Start Tracking", style="Accent.TButton", command=self._start_tracking
        )
        self.start_btn.pack(side="left")

        self.cancel_btn = ttk.Button(
            row, text="■  Cancel", style="Danger.TButton", command=self._cancel_tracking,
            state="disabled",
        )
        self.cancel_btn.pack(side="left", padx=(10, 0))

        self.summary_btn = ttk.Button(
            row, text="Calculate Distance Summary", style="Secondary.TButton",
            command=self._run_distance_summary,
        )
        self.summary_btn.pack(side="left", padx=(10, 0))

        ttk.Button(
            row, text="Open Output Folder", style="Secondary.TButton",
            command=self._open_output_folder,
        ).pack(side="right")

    def _build_progress_and_log(self, parent: ttk.Frame) -> None:
        c = self._colors()
        outer, inner = self._card(parent)
        outer.grid(row=3, column=0, sticky="nsew")
        outer.columnconfigure(0, weight=1)
        outer.rowconfigure(0, weight=1)
        inner.columnconfigure(0, weight=1)
        inner.rowconfigure(3, weight=1)

        status_row = ttk.Frame(inner, style="Surface.TFrame")
        status_row.grid(row=0, column=0, sticky="ew")
        status_row.columnconfigure(0, weight=1)
        ttk.Label(status_row, textvariable=self.status_text, style="SectionHeader.TLabel").grid(
            row=0, column=0, sticky="w"
        )
        ttk.Label(status_row, textvariable=self.progress_label, style="SurfaceMuted.TLabel").grid(
            row=0, column=1, sticky="e"
        )

        self.progress_bar = ttk.Progressbar(
            inner, variable=self.progress_value, maximum=100,
            style="Modern.Horizontal.TProgressbar",
        )
        self.progress_bar.grid(row=1, column=0, sticky="ew", pady=(8, 12))

        ttk.Label(inner, text="Activity log", style="SurfaceMuted.TLabel").grid(
            row=2, column=0, sticky="w"
        )

        log_frame = tk.Frame(inner, bg=c["border"])
        log_frame.grid(row=3, column=0, sticky="nsew", pady=(4, 0))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)

        self.log_box = tk.Text(
            log_frame, wrap="word", bg=c["surface_alt"], fg=c["text"],
            insertbackground=c["text"], relief="flat", padx=10, pady=8,
            font=("Consolas", 9), borderwidth=0, highlightthickness=0,
        )
        self.log_box.grid(row=0, column=0, sticky="nsew", padx=1, pady=1)
        scrollbar = ttk.Scrollbar(log_frame, command=self.log_box.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.log_box.configure(yscrollcommand=scrollbar.set, state="disabled")

        self.log_box.tag_configure("success", foreground=c["success"])
        self.log_box.tag_configure("error", foreground=c["error"])
        self.log_box.tag_configure("warning", foreground=c["warning"])
        self.log_box.tag_configure("muted", foreground=c["text_muted"])

        footer = ttk.Frame(parent, style="TFrame")
        footer.grid(row=4, column=0, sticky="ew", pady=(12, 0))
        link = ttk.Label(
            footer, text="Made by Dilshan — github.com/Dilshan-Pathirana",
            style="Muted.TLabel", cursor="hand2",
        )
        link.pack(side="right")
        link.bind("<Button-1>", lambda e: webbrowser.open_new("https://github.com/Dilshan-Pathirana"))

    # -- Theme --------------------------------------------------------------

    def _toggle_theme(self) -> None:
        self.theme_name = "dark" if self.theme_name == "light" else "light"
        for widget in self.master.winfo_children():
            widget.destroy()
        self._build_style()
        self._build_layout()
        self._save_current_settings()

    # -- Folder selection -----------------------------------------------------

    def _select_video_folder(self) -> None:
        folder = filedialog.askdirectory(initialdir=self.video_dir.get() or os.path.expanduser("~"))
        if folder:
            self.video_dir.set(folder)
            self._save_current_settings()

    def _select_output_folder(self) -> None:
        folder = filedialog.askdirectory(initialdir=self.output_dir.get() or os.path.expanduser("~"))
        if folder:
            self.output_dir.set(folder)
            self._save_current_settings()

    def _list_video_files(self, folder: str) -> list:
        if not folder or not os.path.isdir(folder):
            return []
        return sorted(
            os.path.join(folder, f) for f in os.listdir(folder)
            if f.lower().endswith(VIDEO_EXTENSIONS)
        )

    def _refresh_video_count(self) -> None:
        folder = self.video_dir.get()
        if not folder:
            self.video_count.set("No folder selected")
            return
        if not os.path.isdir(folder):
            self.video_count.set("Folder not found")
            return
        n = len(self._list_video_files(folder))
        self.video_count.set(f"{n} video file{'s' if n != 1 else ''} found (.mp4, .avi, .mov)")

    def _open_output_folder(self) -> None:
        folder = self.output_dir.get()
        if not folder or not os.path.isdir(folder):
            messagebox.showwarning("Output Folder", "Select a valid output folder first.")
            return
        os.startfile(folder)  # noqa: platform-specific, matches Windows-only usage in this project

    # -- Logging --------------------------------------------------------------

    def _log(self, msg: str, tag: Optional[str] = None) -> None:
        self.log_box.configure(state="normal")
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_box.insert("end", f"[{timestamp}] ", "muted")
        self.log_box.insert("end", msg + "\n", tag or "")
        self.log_box.see("end")
        self.log_box.configure(state="disabled")

    # -- Validation -------------------------------------------------------------

    def _parse_calibration(self) -> Optional[tuple]:
        try:
            width = float(self.arena_width.get())
            height = float(self.arena_height.get())
            if width <= 0 or height <= 0:
                raise ValueError
            return width, height
        except ValueError:
            messagebox.showerror(
                "Invalid Calibration",
                "Arena width and height must be positive numbers (cm).",
            )
            return None

    def _save_current_settings(self) -> None:
        calibration = None
        try:
            calibration = (float(self.arena_width.get()), float(self.arena_height.get()))
        except ValueError:
            pass
        save_settings(
            {
                "video_dir": self.video_dir.get(),
                "output_dir": self.output_dir.get(),
                "arena_width_cm": calibration[0] if calibration else self.settings.get("arena_width_cm", 28),
                "arena_height_cm": calibration[1] if calibration else self.settings.get("arena_height_cm", 14),
                "theme": self.theme_name,
            }
        )

    # -- Tracking workflow -----------------------------------------------------

    def _set_running_state(self, running: bool) -> None:
        self._is_running = running
        state = "disabled" if running else "normal"
        self.start_btn.configure(state=state)
        self.summary_btn.configure(state=state)
        self.cancel_btn.configure(state=("normal" if running else "disabled"))

    def _start_tracking(self) -> None:
        video_folder = self.video_dir.get().strip()
        output_folder = self.output_dir.get().strip()

        if not video_folder or not output_folder:
            messagebox.showwarning("Missing Input", "Please select both input and output folders.")
            return
        if not os.path.isdir(video_folder):
            messagebox.showerror("Invalid Folder", "The selected video folder does not exist.")
            return
        if not os.path.isdir(output_folder):
            messagebox.showerror("Invalid Folder", "The selected output folder does not exist.")
            return
        if os.path.abspath(video_folder) == os.path.abspath(output_folder):
            messagebox.showerror("Invalid Folders", "Video folder and output folder must be different.")
            return

        calibration = self._parse_calibration()
        if calibration is None:
            return

        video_files = self._list_video_files(video_folder)
        if not video_files:
            messagebox.showerror("No Videos", "No video files found in the selected folder.")
            return

        self._save_current_settings()

        self.log_box.configure(state="normal")
        self.log_box.delete("1.0", "end")
        self.log_box.configure(state="disabled")
        self.progress_value.set(0)
        self.status_text.set("Tracking in progress…")
        self._log(f"Found {len(video_files)} video(s) in {video_folder}", "muted")

        self._cancel_event.clear()
        self._set_running_state(True)

        self._worker_thread = threading.Thread(
            target=self._run_batch_worker,
            args=(video_files, output_folder, calibration),
            daemon=True,
        )
        self._worker_thread.start()

    def _run_batch_worker(self, video_files: list, output_folder: str, calibration: tuple) -> None:
        """Runs on a background thread; only communicates via the event queue."""
        total = len(video_files)
        completed = 0
        log_filename = os.path.join(
            output_folder, f"batch_log_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt"
        )
        start_time = time.time()

        try:
            with open(log_filename, "w", encoding="utf-8") as logfile:
                with ThreadPoolExecutor(max_workers=min(NUM_WORKERS, total)) as executor:
                    futures = {
                        executor.submit(process_video, video, output_folder): video
                        for video in video_files
                    }

                    for future in as_completed(futures):
                        video = futures[future]
                        video_name = os.path.basename(video)

                        if self._cancel_event.is_set():
                            for f in futures:
                                f.cancel()

                        try:
                            result = future.result()
                            ok = result.startswith("✅")
                            msg = f"{result}"
                        except Exception as e:
                            ok = False
                            msg = f"❌ Failed: {video_name} with error: {e}"

                        completed += 1
                        logfile.write(msg + "\n")
                        elapsed = time.time() - start_time
                        eta = (elapsed / completed) * (total - completed) if completed else 0

                        self._event_queue.put(
                            TrackingEvent(
                                "video_done",
                                {
                                    "message": msg,
                                    "ok": ok,
                                    "completed": completed,
                                    "total": total,
                                    "eta_seconds": eta,
                                },
                            )
                        )

                        if self._cancel_event.is_set():
                            break

            cancelled = self._cancel_event.is_set()
            self._event_queue.put(
                TrackingEvent(
                    "batch_done",
                    {
                        "log_file": log_filename,
                        "completed": completed,
                        "total": total,
                        "cancelled": cancelled,
                        "calibration": calibration,
                        "output_folder": output_folder,
                    },
                )
            )
        except Exception as e:
            self._event_queue.put(TrackingEvent("error", {"message": str(e)}))

    def _cancel_tracking(self) -> None:
        if not self._is_running:
            return
        self._cancel_event.set()
        self.status_text.set("Cancelling… finishing in-progress videos")
        self.cancel_btn.configure(state="disabled")

    def _poll_queue(self) -> None:
        try:
            while True:
                event = self._event_queue.get_nowait()
                self._handle_event(event)
        except queue.Empty:
            pass
        self.master.after(100, self._poll_queue)

    def _handle_event(self, event: TrackingEvent) -> None:
        if event.kind == "video_done":
            p = event.payload
            tag = "success" if p["ok"] else "error"
            self._log(p["message"], tag)
            pct = (p["completed"] / p["total"]) * 100 if p["total"] else 0
            self.progress_value.set(pct)
            eta = p["eta_seconds"]
            eta_str = f"~{int(eta)}s remaining" if eta > 1 else "finishing…"
            self.progress_label.set(f"{p['completed']}/{p['total']} videos • {eta_str}")

        elif event.kind == "batch_done":
            p = event.payload
            self._set_running_state(False)
            if p["cancelled"]:
                self.status_text.set("Cancelled")
                self._log(f"Cancelled after {p['completed']}/{p['total']} video(s).", "warning")
            else:
                self.status_text.set("Tracking complete")
                self.progress_value.set(100)
                self._log(f"All {p['total']} video(s) processed.", "success")
                self._log("Calculating distance summary…", "muted")
                width, height = p["calibration"]
                threading.Thread(
                    target=self._run_summary_worker,
                    args=(p["output_folder"], width, height, True),
                    daemon=True,
                ).start()
            self._log(f"Log saved to: {p['log_file']}", "muted")

        elif event.kind == "summary_done":
            p = event.payload
            if p["path"]:
                self._log(f"Distance summary saved to: {p['path']}", "success")
                if not p.get("silent"):
                    messagebox.showinfo("Summary Complete", f"Distance summary written to:\n{p['path']}")
            else:
                self._log("Could not calculate distance summary.", "error")
                if not p.get("silent"):
                    messagebox.showerror("Error", "Could not calculate distance summary.")
            self.status_text.set("Ready")

        elif event.kind == "error":
            self._set_running_state(False)
            self.status_text.set("Error")
            self._log(f"Unexpected error: {event.payload['message']}", "error")
            messagebox.showerror("Error", event.payload["message"])

    # -- Distance summary -----------------------------------------------------

    def _run_distance_summary(self) -> None:
        output_dir = self.output_dir.get().strip()
        video_dir = self.video_dir.get().strip()
        if not output_dir or not os.path.isdir(output_dir):
            messagebox.showwarning("Missing Output Folder", "Please select a valid output folder first.")
            return

        calibration = self._parse_calibration()
        if calibration is None:
            return

        self.status_text.set("Calculating distance summary…")
        self._log("Calculating distance summary…", "muted")
        width, height = calibration
        threading.Thread(
            target=self._run_summary_worker,
            args=(output_dir, width, height, False, video_dir or None),
            daemon=True,
        ).start()

    def _run_summary_worker(
        self,
        output_dir: str,
        width: float,
        height: float,
        silent: bool,
        video_dir: Optional[str] = None,
    ) -> None:
        try:
            summary_path = calculate_summary(
                output_dir, videos_dir=video_dir, real_width_cm=width, real_height_cm=height
            )
        except Exception as e:
            summary_path = None
            self._event_queue.put(TrackingEvent("error", {"message": str(e)}))
            return
        self._event_queue.put(
            TrackingEvent("summary_done", {"path": summary_path, "silent": silent})
        )

    # -- Shutdown -----------------------------------------------------------

    def _on_close(self) -> None:
        if self._is_running:
            if not messagebox.askyesno(
                "Tracking in progress",
                "Tracking is still running. Quit anyway? In-progress videos will finish in the background until the process exits.",
            ):
                return
        self._save_current_settings()
        self.master.destroy()


def main() -> None:
    """Entry point for the GUI application."""
    multiprocessing.freeze_support()

    try:
        root = tk.Tk()
        FishTrackerGUI(root)
        root.mainloop()
    except Exception:
        import traceback

        with open("gui_crash_log.txt", "w") as f:
            traceback.print_exc(file=f)
        print("An error occurred. See gui_crash_log.txt for details.")
        input("Press Enter to exit...")


if __name__ == "__main__":
    main()
