import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import os
import sys
import concurrent.futures
from datetime import datetime
from tracker_wrapper import process_video
from distance_calculator import calculate_summary  # We'll add this function next

NUM_WORKERS = 10

def get_resource_path(relative_path):
    """Get absolute path to resource, works for PyInstaller and dev mode"""
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

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

        # Log total count and all names
        self.log_message(f"🔍 Found {len(video_files)} videos:")
        for v in video_files:
            self.log_message(f"  • {os.path.basename(v)}")

        batch_size = 10
        total = len(video_files)
        log_filename = os.path.join(output_folder, f"batch_log_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt")

        with open(log_filename, 'w', encoding="utf-8") as logfile:
            with concurrent.futures.ThreadPoolExecutor(max_workers=batch_size) as executor:
                for batch_start in range(0, total, batch_size):
                    batch = video_files[batch_start:batch_start + batch_size]
                    batch_names = [os.path.basename(v) for v in batch]

                    self.log_message(f"\n▶️ Starting batch: {', '.join(batch_names)}")
                    logfile.write(f"\n▶️ Starting batch: {', '.join(batch_names)}\n")

                    futures = {executor.submit(process_video, video, output_folder): video for video in batch}

                    for future in concurrent.futures.as_completed(futures):
                        video = futures[future]
                        video_name = os.path.basename(video)
                        try:
                            result = future.result()
                            msg = f"✅ Completed {video_name}: {result}"
                            self.log_message(msg)
                            logfile.write(msg + "\n")
                        except Exception as e:
                            msg = f"❌ Error with {video_name}: {e}"
                            self.log_message(msg)
                            logfile.write(msg + "\n")

                    self.log_message(f"✔️ Finished batch: {', '.join(batch_names)}")
                    logfile.write(f"✔️ Finished batch: {', '.join(batch_names)}\n")

                    self.progress.set(min(100, ((batch_start + len(batch)) / total) * 100))

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

    try:
        root = tk.Tk()
        app = FishTrackerGUI(root)
        root.mainloop()
    except Exception as e:
        import traceback
        with open("gui_crash_log.txt", "w") as f:
            traceback.print_exc(file=f)
        print("An error occurred. See gui_crash_log.txt for details.")
        input("Press Enter to exit...")
