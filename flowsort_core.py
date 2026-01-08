import os
import sys
import ctypes
import tkinter as tk
import pathlib
import shutil
from datetime import datetime

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

class FlowSortCore:
    def __init__(self):
        if not is_admin():
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
            sys.exit()

        self.base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        self.icon_path = os.path.join(self.base_path, "icon.ico")

        if len(sys.argv) < 2:
            self.show_instruction_toast()
        else:
            try:
                mode = sys.argv[2]
                folder_path = sys.argv[3]
                self.execute_sorting(mode, folder_path)
            except IndexError:
                pass

    def show_instruction_toast(self):
        root = tk.Tk()
        root.overrideredirect(True)
        root.attributes("-topmost", True)
        root.configure(bg="white", highlightbackground="#e0e0e0", highlightthickness=1)
        
        if os.path.exists(self.icon_path):
            root.iconbitmap(self.icon_path)
            
        w, h = 260, 130
        sw, sh = root.winfo_screenwidth(), root.winfo_screenheight()
        root.geometry(f"{w}x{h}+{sw-w-10}+{sh-h-90}")

        tk.Frame(root, bg="#f44336", width=4).pack(side="left", fill="y")
        f = tk.Frame(root, bg="white")
        f.pack(fill="both", expand=True, padx=15, pady=10)

        tk.Label(f, text="FlowSort Активен", fg="#f44336", bg="white", font=("Segoe UI", 10, "bold")).pack(anchor="w")
        tk.Label(f, text="Нажмите правой кнопкой мыши\nв любой папке для сортировки.", 
                 fg="#666666", bg="white", font=("Segoe UI", 8), justify="left").pack(pady=5, anchor="w")
        
        tk.Button(f, text="ПОНЯТНО", command=root.destroy, 
                  bg="#f44336", fg="white", activebackground="#f44336", activeforeground="white",
                  relief="flat", font=("Segoe UI", 8, "bold"), padx=15).pack(side="bottom", anchor="e")
        
        root.after(10000, root.destroy)
        root.mainloop()

    def execute_sorting(self, mode, path):
        try:
            os.chdir(path)
            files = [f for f in os.listdir() if os.path.isfile(f) and f != "flowsort_core.exe"]
            if mode == "az":
                files.sort(key=str.lower)
                self.rename_files(files)
            elif mode == "za":
                files.sort(key=str.lower, reverse=True)
                self.rename_files(files)
            elif mode == "size_up":
                files.sort(key=os.path.getsize)
                self.rename_files(files)
            elif mode == "size_down":
                files.sort(key=os.path.getsize, reverse=True)
                self.rename_files(files)
            elif mode == "time_new":
                files.sort(key=os.path.getmtime, reverse=True)
                self.rename_files(files)
            elif mode == "time_old":
                files.sort(key=os.path.getmtime)
                self.rename_files(files)
            elif mode == "smart":
                self.smart_category_sort(files)
        except:
            pass

    def rename_files(self, files):
        for i, f in enumerate(files, 1):
            name = f[4:] if f[:3].isdigit() and f[3] == "_" else f
            new_name = f"{i:03d}_{name}"
            if f != new_name:
                try: os.rename(f, new_name)
                except: pass

    def smart_category_sort(self, files):
        cats = {
            "Images": [".jpg", ".png", ".jpeg", ".gif", ".webp", ".ico", ".svg"],
            "Docs": [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".pptx", ".csv", ".rtf"],
            "Video": [".mp4", ".mkv", ".mov", ".avi", ".wmv"],
            "Music": [".mp3", ".wav", ".flac", ".m4a", ".ogg"],
            "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
            "Programs": [".exe", ".msi", ".bat", ".cmd"]
        }
        for f in files:
            ext = pathlib.Path(f).suffix.lower()
            target = "Others"
            for folder, extensions in cats.items():
                if ext in extensions:
                    target = folder
                    break
            if not os.path.exists(target):
                try: os.makedirs(target)
                except: pass
            dest = os.path.join(target, f)
            if os.path.exists(dest):
                dest = os.path.join(target, f"{datetime.now().second}_{f}")
            try: shutil.move(f, dest)
            except: pass

if __name__ == "__main__":
    FlowSortCore()