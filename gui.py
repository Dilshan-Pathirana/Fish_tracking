import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import os
from multiprocessing import Pool
from datetime import datetime
from tracker_wrapper import process_video
from distance_calculator import calculate_summary  # We'll add this function next

NUM_WORKERS = 10

class FishTrackerGUI:
    def __init__(self, master):
        self.master = master
        master.title("Fish Tracker")

        self.video_dir = tk.StringVar()
        self.output_dir = tk.StringVar()

        # Folder selectors
        tk.Label(master, text="Select Video Folder").grid(row=0, column=0, sticky="w")
        tk.Entry(master, textvariable=self.video_dir, width=50).grid(row=0, column=1, padx=5)
        tk.Button(master, text="Browse", command=self.select_video_folder).grid(row=0, column=2)

        tk.Label(master, text="Select Output Folder").grid(row=1, column=0, sticky="w")
        tk.Entry(master, textvariable=self.output_dir, width=50).grid(row=1, column=1, padx=5)
        tk.Button(master, text="Browse", command=self.select_output_folder).grid(row=1, column=2)

        # Buttons
        tk.Button(master, text="Start Tracking", command=self.start_tracking).grid(row=2, column=1, pady=5)
        tk.Button(master, text="Calculate Distance Summary", command=self.run_distance_summary).grid(row=3, column=1, pady=5)
        tk.Button(master, text="Quit", command=master.quit).grid(row=4, column=1, pady=5)

        # Progress display
        self.progress = tk.DoubleVar()
        self.progress_bar = tk.Scale(master, variable=self.progress, from_=0, to=100,
                                     orient="horizontal", length=400, label="Progress (%)")
        self.progress_bar.grid(row=5, column=0, columnspan=3, pady=10)

        self.status_box = scrolledtext.ScrolledText(master, width=80, height=10)
        self.status_box.grid(row=6, column=0, columnspan=3, padx=10, pady=5)

    def select_video_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.video_dir.set(folder)

    def select_output_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.output_dir.set(folder)

    def log_message(self, msg):
        self.status_box.insert(tk.END, msg + "\n")
        self.status_box.see(tk.END)
        self.master.update_idletasks()

    def start_tracking(self):
        video_folder = self.video_dir.get()
        output_folder = self.output_dir.get()

        if not video_folder or not output_folder:
            messagebox.showwarning("Missing Input", "Please select both input and output folders.")
            return

        video_files = sorted([
            os.path.join(video_folder, f) for f in os.listdir(video_folder)
            if f.lower().endswith((".mp4", ".avi", ".mov"))
        ])

        if not video_files:
            messagebox.showerror("No Videos", "No video files found in the selected folder.")
            return

        self.status_box.delete('1.0', tk.END)
        self.progress.set(0)

        log_filename = os.path.join(output_folder, f"batch_log_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt")
        with open(log_filename, 'w', encoding="utf-8") as logfile:
            for idx, video in enumerate(video_files, 1):
                result = process_video(video, output_folder)
                self.log_message(result)
                logfile.write(result + "\n")
                self.progress.set((idx / len(video_files)) * 100)

        messagebox.showinfo("Done", f"Processed {len(video_files)} video(s).\nLog saved to:\n{log_filename}")

    def run_distance_summary(self):
        output_dir = self.output_dir.get()
        if not output_dir:
            messagebox.showwarning("Missing Output Folder", "Please select the output folder first.")
            return

        summary_path = calculate_summary(output_dir)
        if summary_path:
            messagebox.showinfo("Summary Complete", f"Distance summary written to:\n{summary_path}")
        else:
            messagebox.showerror("Error", "Could not calculate distance summary.")


# Entry point
if __name__ == "__main__":
    import multiprocessing
    multiprocessing.freeze_support()

    root = tk.Tk()
    app = FishTrackerGUI(root)
    root.mainloop()
