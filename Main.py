import tkinter as tk
from tkinter import ttk, messagebox
import threading
import requests
import subprocess
import os
import sys
import tempfile
import time
import colorsys

class DarkTheme:
    PINK = "#c792ea"
    GRAY = "#A0A0A0"
    GRAYTWO = "#FFFFFF"
    BG_COLOR = "#1e1e1e"
    FG_COLOR = "#ffffff"
    BUTTON_BG = "#3d3d3d"
    BUTTON_FG = "#ffffff"
    ENTRY_BG = "#2d2d2d"
    ENTRY_FG = "#ffffff"
    HIGHLIGHT_COLOR = "#007acc"
    ERROR_COLOR = "#ff5252"
    SUCCESS_COLOR = "#4caf50"
    INFO_COLOR = "#2196f3"
    
    RAINBOW_COLORS = [
        "#FFFFFF", "#ff0000", "#ff9900", "#ffee00", 
        "#33ff00", "#00fff2", "#0077ff", "#0400ff",
        "#4c00ff", "#cc00ff", "#ff00dd", "#ff0040"
    ]

class InstallerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AppName")
        self.root.geometry("400x260")
        self.root.resizable(False, False)
        self.root.overrideredirect(True)
        
        self.close_btn_color = DarkTheme.GRAY
        self.minimize_btn_color = DarkTheme.PINK
        
        self.apply_dark_theme()
        
        self.title_chars = list("AppName")
        self.char_colors = [DarkTheme.RAINBOW_COLORS[0]] * len(self.title_chars)
        self.rainbow_position = -5
        self.title_labels = []
        
        self.create_title_bar()
        
        main_frame = tk.Frame(root, bg=DarkTheme.BG_COLOR, padx=20, pady=20)
        main_frame.pack(expand=True, fill="both")
        
        login_frame = tk.Frame(main_frame, bg=DarkTheme.BG_COLOR)
        login_frame.pack(pady=10, fill="x")
        
        username_frame = tk.Frame(login_frame, bg=DarkTheme.BG_COLOR)
        username_frame.pack(fill="x", pady=5)
        username_label = tk.Label(username_frame, text="Username:", 
                                width=12, 
                                bg=DarkTheme.BG_COLOR, 
                                fg=DarkTheme.GRAY)
        username_label.pack(side="left")
        self.username_entry = tk.Entry(username_frame, 
                                     bg=DarkTheme.ENTRY_BG, 
                                     fg=DarkTheme.ENTRY_FG,
                                     insertbackground=DarkTheme.FG_COLOR,
                                     relief=tk.FLAT,
                                     highlightthickness=1,
                                     highlightcolor=DarkTheme.GRAY,
                                     highlightbackground=DarkTheme.BUTTON_BG)
        self.username_entry.pack(side="left", expand=True, fill="x")
        
        password_frame = tk.Frame(login_frame, bg=DarkTheme.BG_COLOR)
        password_frame.pack(fill="x", pady=5)
        password_label = tk.Label(password_frame, text="Password:", 
                                width=12, 
                                bg=DarkTheme.BG_COLOR, 
                                fg=DarkTheme.GRAY)
        password_label.pack(side="left")
        self.password_entry = tk.Entry(password_frame, show="*", 
                                     bg=DarkTheme.ENTRY_BG, 
                                     fg=DarkTheme.ENTRY_FG,
                                     insertbackground=DarkTheme.FG_COLOR,
                                     relief=tk.FLAT,
                                     highlightthickness=1,
                                     highlightcolor=DarkTheme.GRAY,
                                     highlightbackground=DarkTheme.BUTTON_BG)
        self.password_entry.pack(side="left", expand=True, fill="x")
        
        self.status_label = tk.Label(main_frame, text="hi :>", 
                                   foreground=DarkTheme.GRAY,
                                   bg=DarkTheme.BG_COLOR)
        self.status_label.pack(pady=10)
        
        self.login_button = tk.Button(main_frame, text="Login", 
                                    command=self.validate_login,
                                    bg=DarkTheme.ENTRY_BG, 
                                    fg=DarkTheme.GRAY,
                                    activebackground=DarkTheme.ENTRY_BG,
                                    activeforeground=DarkTheme.GRAY,
                                    relief=tk.FLAT,
                                    padx=20, pady=5)
        self.login_button.pack(pady=10)
        
        self.info_text_label = tk.Label(main_frame, text="bottom message",  
                                      bg=DarkTheme.BG_COLOR, 
                                      fg=DarkTheme.GRAY)
        self.info_text_label.pack(pady=5)
        
        self.python_script_url = "PYTHON_URL_HERE"
        
        self.center_window()
        
        self.animate_rainbow_title()
    
    def create_title_bar(self):
        title_bar = tk.Frame(self.root, bg=DarkTheme.BG_COLOR, relief="flat", bd=0, height=30)
        title_bar.pack(fill="x")
        
        self.title_frame = tk.Frame(title_bar, bg=DarkTheme.BG_COLOR)
        self.title_frame.pack(side="left", padx=10)
        
        for char in self.title_chars:
            label = tk.Label(self.title_frame, text=char, 
                          bg=DarkTheme.BG_COLOR, fg=DarkTheme.GRAY,
                          font=("Arial", 10, "bold"))
            label.pack(side="left", padx=0)
            self.title_labels.append(label)
        
        self.close_btn = tk.Button(title_bar, text="✕", 
                            width=2, height=1,
                            bg=DarkTheme.BG_COLOR, fg=DarkTheme.GRAY,
                            relief="flat", bd=0,
                            activebackground=DarkTheme.BG_COLOR,
                            activeforeground=DarkTheme.GRAY,
                            command=self.root.destroy)
        self.close_btn.pack(side="right")
        
        self.minimize_btn = tk.Button(title_bar, text="_", 
                               width=2, height=1,
                               bg=DarkTheme.BG_COLOR, fg=DarkTheme.GRAY,
                               relief="flat", bd=0,
                               activebackground=DarkTheme.BG_COLOR,
                               activeforeground=DarkTheme.GRAY,
                               command=self.minimize_window)
        self.minimize_btn.pack(side="right")
        
        spacer = tk.Frame(title_bar, bg=DarkTheme.BG_COLOR)
        spacer.pack(side="left", expand=True, fill="x")
        
        btn_colors_frame = tk.Frame(title_bar, bg=DarkTheme.BG_COLOR)
        btn_colors_frame.pack(side="right", padx=5)
        
        title_bar.bind("<ButtonPress-1>", self.start_move)
        title_bar.bind("<ButtonRelease-1>", self.stop_move)
        title_bar.bind("<B1-Motion>", self.do_move)
        self.title_frame.bind("<ButtonPress-1>", self.start_move)
        self.title_frame.bind("<ButtonRelease-1>", self.stop_move)
        self.title_frame.bind("<B1-Motion>", self.do_move)
    
    def animate_rainbow_title(self):
        rainbow_width = 1
        
        self.rainbow_position += 1
        if self.rainbow_position > len(self.title_chars) + rainbow_width:
            self.rainbow_position = -rainbow_width
        
        for i in range(len(self.title_chars)):
            rel_pos = i - self.rainbow_position
            
            if 0 <= rel_pos < rainbow_width:
                color_idx = int((rel_pos / rainbow_width) * len(DarkTheme.GRAYTWO))
                color_idx = max(0, min(color_idx, len(DarkTheme.GRAYTWO) - 1))
                self.title_labels[i].config(fg=DarkTheme.RAINBOW_COLORS[color_idx])
            else:
                self.title_labels[i].config(fg=DarkTheme.GRAY)
        
        self.root.after(100, self.animate_rainbow_title)
    
    def start_move(self, event):
        self.x = event.x
        self.y = event.y
    
    def stop_move(self, event):
        self.x = None
        self.y = None
    
    def do_move(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry(f"+{x}+{y}")
    
    def minimize_window(self):
        self.root.update_idletasks()
        self.root.overrideredirect(False)
        self.root.state('iconic')
        
        self.root.bind("<Map>", self.on_deiconify)
        
    def on_deiconify(self, event=None):
        if self.root.state() == 'normal':
            self.root.overrideredirect(True)
            
            self.title_labels = []
            
            self.create_title_bar()
            self.center_window()
    
    def apply_dark_theme(self):
        self.root.configure(bg=DarkTheme.BG_COLOR)
        
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure('TFrame', background=DarkTheme.BG_COLOR)
        style.configure('TLabel', background=DarkTheme.BG_COLOR, foreground=DarkTheme.FG_COLOR)
        style.configure('TButton', 
                      background=DarkTheme.BUTTON_BG, 
                      foreground=DarkTheme.BUTTON_FG)
        style.map('TButton', 
                background=[('active', DarkTheme.HIGHLIGHT_COLOR)],
                foreground=[('active', DarkTheme.FG_COLOR)])
    
    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def validate_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if not username or not password:
            self.show_error("Username and Password required!")
            return
        
        self.status_label.config(text="validating...", foreground=DarkTheme.INFO_COLOR)
        self.login_button.config(state="disabled")
        
        threading.Thread(target=self.check_credentials, args=(username, password), daemon=True).start()
    
    def check_credentials(self, username, password):
        try:
            accounts_url = "ACCOUNTS_URL_HERE"
            
            response = requests.get(accounts_url, timeout=10)
            
            if response.status_code == 200:
                credentials = response.text.splitlines()
                
                for credential in credentials:
                    if ":" in credential:
                        stored_username, stored_password = credential.strip().split(":", 1)
                        if stored_username == username and stored_password == password:
                            self.root.after(0, self.login_success)
                            return
                
                self.root.after(0, lambda: self.show_error("Username or Password incorrect!"))
            else:
                self.root.after(0, lambda: self.show_error(f"Connection error: {response.status_code}"))
        
        except Exception as e:
            self.root.after(0, lambda: self.show_error(f"Connection error: {str(e)}"))
        
        finally:
            self.root.after(0, lambda: self.login_button.config(state="normal"))
    
    def show_error(self, message):
        self.status_label.config(text=message, foreground=DarkTheme.ERROR_COLOR)
    
    def login_success(self):
        self.status_label.config(text="Login successful!", 
                               foreground=DarkTheme.SUCCESS_COLOR)
        
        threading.Thread(target=self.download_and_run_script, daemon=True).start()
    
    def download_and_run_script(self):

        try:
            response = requests.get(self.python_script_url, timeout=15)
            
            if response.status_code == 200:
                python_code = response.text
                
                with tempfile.NamedTemporaryFile(suffix='.py', delete=False, mode='w', encoding='utf-8') as temp_file:
                    temp_file_path = temp_file.name
                    temp_file.write(python_code)
                
                self.root.after(0, lambda: self.status_label.config(
                    text="Script downloaded successfull.", 
                    foreground=DarkTheme.SUCCESS_COLOR))
                
                if os.name == 'nt':
                    cmd_command = f'start cmd /k python "{temp_file_path}"'
                else:
                    cmd_command = f'xterm -e "python3 \'{temp_file_path}\'; read -p \'Press enter...\'"'
                
                subprocess.Popen(cmd_command, shell=True)
                
                self.root.after(2000, self.root.destroy)
            else:
                self.root.after(0, lambda: self.show_error(f"Script download error: {response.status_code}"))
        
        except Exception as e:
            self.root.after(0, lambda: self.show_error(f"Script download/run error: {str(e)}"))


if __name__ == "__main__":
    root = tk.Tk()
    app = InstallerApp(root)
    root.mainloop()
