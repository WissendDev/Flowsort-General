import os, sys, ctypes, winreg, tkinter as tk
import requests
from tkinter import ttk, filedialog
from threading import Thread

def is_admin():
    try: return ctypes.windll.shell32.IsUserAnAdmin()
    except: return False

if not is_admin():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    sys.exit()

class FlowSortInstaller:
    def __init__(self):
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.configure(bg="white", highlightbackground="#f44336", highlightthickness=1)
        
        w, h = 420, 280
        sw, sh = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        self.root.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")

        self.url_core = "https://www.dropbox.com/scl/fi/4t1nee0msmxyn03owwqjh/flowsort_core.exe?rlkey=qyrcbr7srqsb6v2ei6e9nm1q1&dl=1"
        self.url_uninst = "https://www.dropbox.com/scl/fi/8aarp3p4dc4ap1bbuv8a/uninstaller.exe?rlkey=ndf010vzkljyubch11etfb8pw&st=r6vmn1ec&dl=1"
        self.url_icon = "https://www.dropbox.com/scl/fi/3pfwngue5ilx3vwfz86l3/icon.ico?rlkey=p84re0m87bo8mryqmv3dfyxns&dl=1"

        self.install_dir = tk.StringVar(value=os.path.join(os.environ['PROGRAMFILES'], "FlowSort"))

        tk.Label(self.root, text="Установка FlowSort", fg="#f44336", bg="white", font=("Segoe UI", 13, "bold")).pack(pady=(15, 5), anchor="w", padx=25)
        tk.Label(self.root, text="Выберите папку для установки:", fg="#666666", bg="white", font=("Segoe UI", 9)).pack(anchor="w", padx=25)
        
        path_frame = tk.Frame(self.root, bg="white")
        path_frame.pack(fill="x", padx=25, pady=5)
        self.path_entry = tk.Entry(path_frame, textvariable=self.install_dir, font=("Segoe UI", 9), relief="flat", highlightbackground="#e0e0e0", highlightthickness=1)
        self.path_entry.pack(side="left", fill="x", expand=True, ipady=3)
        tk.Button(path_frame, text="...", command=self.browse_folder, bg="#f5f5f5", relief="flat", padx=10).pack(side="right", padx=(5, 0))

        self.status = tk.Label(self.root, text="Программа будет доступна в меню ПКМ.", fg="#999999", bg="white", font=("Segoe UI", 8))
        self.status.pack(anchor="w", padx=25, pady=5)

        self.btn_frame = tk.Frame(self.root, bg="white")
        self.btn_frame.pack(fill="x", side="bottom", pady=20, padx=25)
        self.ins_btn = tk.Button(self.btn_frame, text="Установить", command=self.start_install, bg="#f44336", fg="white", activebackground="#f44336", activeforeground="white", relief="flat", font=("Segoe UI", 10, "bold"), padx=20)
        self.ins_btn.pack(side="right", padx=5)
        tk.Button(self.btn_frame, text="Выход", command=sys.exit, bg="#f5f5f5", fg="#333333", activebackground="#f5f5f5", relief="flat", font=("Segoe UI", 10), padx=15).pack(side="right")

        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure("G.Horizontal.TProgressbar", background='#4CAF50', troughcolor='#f0f0f0', borderwidth=0, thickness=6)
        self.progress = ttk.Progressbar(self.root, orient="horizontal", length=370, mode="determinate", style="G.Horizontal.TProgressbar")

    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder: self.install_dir.set(folder.replace("/", "\\"))

    def start_install(self):
        self.ins_btn.config(state="disabled")
        self.progress.pack(pady=(5, 0), padx=25)
        Thread(target=self.logic, daemon=True).start()

    def download(self, url, dest):
        r = requests.get(url, timeout=60)
        r.raise_for_status()
        with open(dest, 'wb') as f:
            f.write(r.content)

    def logic(self):
        try:
            target = self.install_dir.get()
            if not os.path.exists(target): os.makedirs(target, exist_ok=True)
            
            self.status.config(text="Загрузка основного файла...")
            core_p = os.path.join(target, "flowsort_core.exe")
            self.download(self.url_core, core_p)
            self.progress['value'] = 35
            
            self.status.config(text="Загрузка иконки...")
            icon_p = os.path.join(target, "icon.ico")
            self.download(self.url_icon, icon_p)
            self.progress['value'] = 60
            
            self.status.config(text="Загрузка деинсталлятора...")
            self.download(self.url_uninst, os.path.join(target, "uninstaller.exe"))
            self.progress['value'] = 85
            
            self.reg(core_p, icon_p)
            self.progress['value'] = 100
            self.status.config(text="Установка завершена!", fg="#4CAF50")
            
            ctypes.windll.shell32.ShellExecuteW(None, "runas", core_p, None, None, 1)
            self.ins_btn.config(text="Готово", state="normal", command=sys.exit)
        except Exception as e:
            self.status.config(text=f"Ошибка: {str(e)}", fg="red")
            self.ins_btn.config(state="normal")

    def reg(self, exe_path, icon_path):
        base = r"Directory\Background\shell\FlowSort"
        with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, base) as k:
            winreg.SetValueEx(k, "MUIVerb", 0, winreg.REG_SZ, "FlowSort")
            winreg.SetValueEx(k, "SubCommands", 0, winreg.REG_SZ, "")
            winreg.SetValueEx(k, "Icon", 0, winreg.REG_SZ, icon_path)
        sub = base + r"\shell"
        items = {"01": ("Name (A-Z)", "az"), "02": ("Name (Z-A)", "za"), "03": ("Size (Min)", "size_up"), "04": ("Size (Max)", "size_down"), "05": ("Newest", "time_new"), "06": ("Oldest", "time_old"), "07": ("Smart Sort", "smart")}
        for k, (l, m) in items.items():
            with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, f"{sub}\\{k}") as sk:
                winreg.SetValueEx(sk, "MUIVerb", 0, winreg.REG_SZ, l)
                with winreg.CreateKey(sk, "command") as ck:
                    winreg.SetValue(ck, "", winreg.REG_SZ, f'"{exe_path}" --sort {m} "%V"')

if __name__ == "__main__":
    FlowSortInstaller().root.mainloop()