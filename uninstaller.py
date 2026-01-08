import os, sys, ctypes, shutil, tkinter as tk
from tkinter import ttk

def is_admin():
    try: return ctypes.windll.shell32.IsUserAnAdmin()
    except: return False

if not is_admin():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    sys.exit()

class Uninstaller:
    def __init__(self):
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.configure(bg="white", highlightbackground="#f44336", highlightthickness=1)
        w, h = 350, 180
        sw, sh = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        self.root.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")

        tk.Label(self.root, text="Удаление FlowSort", fg="#f44336", bg="white", font=("Segoe UI", 12, "bold")).pack(pady=(20, 5), padx=25, anchor="w")
        self.lbl = tk.Label(self.root, text="Вы уверены, что хотите полностью удалить\nFlowSort и все его компоненты?", fg="#666666", bg="white", font=("Segoe UI", 9), justify="left")
        self.lbl.pack(padx=25, anchor="w")

        self.bf = tk.Frame(self.root, bg="white")
        self.bf.pack(fill="x", side="bottom", pady=20, padx=25)
        self.ub = tk.Button(self.bf, text="Удалить всё", command=self.start_uninst, bg="#f44336", fg="white", activebackground="#f44336", activeforeground="white", relief="flat", font=("Segoe UI", 9, "bold"), padx=15)
        self.ub.pack(side="right", padx=5)
        tk.Button(self.bf, text="Отмена", command=sys.exit, bg="#f5f5f5", relief="flat", padx=15).pack(side="right")

        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure("G.Horizontal.TProgressbar", background='#4CAF50', troughcolor='#f0f0f0', borderwidth=0)
        self.pg = ttk.Progressbar(self.root, orient="horizontal", length=300, mode="determinate", style="G.Horizontal.TProgressbar")

    def start_uninst(self):
        self.ub.config(state="disabled")
        self.pg.pack(pady=5)
        self.run_logic(0)

    def run_logic(self, val):
        if val < 100:
            self.pg['value'] = val
            self.root.after(30, lambda: self.run_logic(val + 5))
        else:
            self.final_clean()

    def final_clean(self):
        try:
            os.system(r'reg delete "HKEY_CLASSES_ROOT\Directory\Background\shell\FlowSort" /f')
            temp_path = os.path.join(os.environ['TEMP'], "FlowTemp")
            if os.path.exists(temp_path):
                shutil.rmtree(temp_path, ignore_errors=True)
            self.lbl.config(text="Удаление завершено! Меню очищено.", fg="#4CAF50")
            self.pg.pack_forget()
            self.root.after(2000, sys.exit)
        except:
            sys.exit()

if __name__ == "__main__":
    Uninstaller().root.mainloop()