import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import time
import json
import os

class TypingTestApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Typing Test Platform")
        self.root.geometry("800x600")
        
        self.users_data_file = 'users_data.json'
        self.current_user = None
        self.sample_texts = [
            "The quick brown fox jumps over the lazy dog",
            "Python is an interpreted, high-level, general-purpose programming language",
            "Tkinter is the standard GUI library for Python",
            "Artificial intelligence is intelligence demonstrated by machines",
            "Data science is an inter-disciplinary field that uses scientific methods"
        ]
        
        self.load_users_data()
        self.create_login_screen()
        
    def load_users_data(self):
        if os.path.exists(self.users_data_file):
            with open(self.users_data_file, 'r') as file:
                self.users_data = json.load(file)
        else:
            self.users_data = {}

    def save_users_data(self):
        with open(self.users_data_file, 'w') as file:
            json.dump(self.users_data, file, indent=4)
    
    def create_login_screen(self):
        self.clear_screen()
        self.label = tk.Label(self.root, text="Typing Test Platform", font=("Helvetica", 24))
        self.label.pack(pady=20)

        self.login_button = tk.Button(self.root, text="Login", command=self.login, font=("Helvetica", 14))
        self.login_button.pack(pady=10)

        self.register_button = tk.Button(self.root, text="Register", command=self.register, font=("Helvetica", 14))
        self.register_button.pack(pady=10)
    
    def login(self):
        username = simpledialog.askstring("Login", "Enter your username:")
        if username in self.users_data:
            self.current_user = username
            self.create_main_screen()
        else:
            messagebox.showerror("Error", "Username not found!")

    def register(self):
        username = simpledialog.askstring("Register", "Enter a new username:")
        if username and username not in self.users_data:
            self.users_data[username] = {"tests": [], "badges": []}
            self.save_users_data()
            messagebox.showinfo("Success", "User registered successfully!")
        else:
            messagebox.showerror("Error", "Username already exists or invalid!")
    
    def create_main_screen(self):
        self.clear_screen()
        self.welcome_label = tk.Label(self.root, text=f"Welcome, {self.current_user}", font=("Helvetica", 18))
        self.welcome_label.pack(pady=10)

        self.choose_text_label = tk.Label(self.root, text="Choose a text sample:", font=("Helvetica", 14))
        self.choose_text_label.pack(pady=10)

        self.text_var = tk.StringVar(value=self.sample_texts[0])
        self.text_menu = ttk.Combobox(self.root, textvariable=self.text_var, values=self.sample_texts, state="readonly", font=("Helvetica", 12))
        self.text_menu.pack(pady=10)

        self.start_test_button = tk.Button(self.root, text="Start Typing Test", command=self.start_typing_test, font=("Helvetica", 14))
        self.start_test_button.pack(pady=10)

        self.view_results_button = tk.Button(self.root, text="View Results", command=self.view_results, font=("Helvetica", 14))
        self.view_results_button.pack(pady=10)

        self.logout_button = tk.Button(self.root, text="Logout", command=self.logout, font=("Helvetica", 14))
        self.logout_button.pack(pady=10)

    def start_typing_test(self):
        self.clear_screen()
        self.sample_text = self.text_var.get()
        
        self.label = tk.Label(self.root, text=self.sample_text, wraplength=700, font=("Helvetica", 14))
        self.label.pack(pady=20)

        self.entry = tk.Entry(self.root, font=("Helvetica", 14), width=60)
        self.entry.pack(pady=20)
        self.entry.bind("<Return>", self.calculate_results)

        self.start_button = tk.Button(self.root, text="Start", command=self.start_test, font=("Helvetica", 14))
        self.start_button.pack(pady=20)

        self.result_label = tk.Label(self.root, text="", font=("Helvetica", 14))
        self.result_label.pack(pady=20)

    def start_test(self):
        self.entry.delete(0, tk.END)
        self.start_time = time.time()
        self.entry.focus()

    def calculate_results(self, event):
        self.end_time = time.time()
        typed_text = self.entry.get()
        
        time_taken = self.end_time - self.start_time
        words_per_minute = (len(typed_text.split()) / time_taken) * 60
        accuracy = sum(1 for a, b in zip(self.sample_text, typed_text) if a == b) / len(self.sample_text) * 100
        
        result = f"WPM: {words_per_minute:.2f}\nAccuracy: {accuracy:.2f}%"
        self.result_label.config(text=result)

        self.save_result(words_per_minute, accuracy)
        self.check_rewards(words_per_minute, accuracy)
        messagebox.showinfo("Results", result)
        self.create_main_screen()

    def save_result(self, wpm, accuracy):
        if self.current_user:
            self.users_data[self.current_user]["tests"].append({"wpm": wpm, "accuracy": accuracy})
            self.save_users_data()

    def check_rewards(self, wpm, accuracy):
        badges = self.users_data[self.current_user].get("badges", [])
        if wpm > 60 and "Speedster" not in badges:
            badges.append("Speedster")
            messagebox.showinfo("New Badge", "Congratulations! You've earned the 'Speedster' badge!")
        if accuracy > 95 and "Accuracy Ace" not in badges:
            badges.append("Accuracy Ace")
            messagebox.showinfo("New Badge", "Congratulations! You've earned the 'Accuracy Ace' badge!")
        self.users_data[self.current_user]["badges"] = badges
        self.save_users_data()

    def view_results(self):
        self.clear_screen()

        results = self.users_data[self.current_user]["tests"]
        results_text = "\n".join([f"WPM: {r['wpm']:.2f}, Accuracy: {r['accuracy']:.2f}%" for r in results])

        self.results_label = tk.Label(self.root, text=results_text, font=("Helvetica", 14))
        self.results_label.pack(pady=20)

        self.back_button = tk.Button(self.root, text="Back", command=self.create_main_screen, font=("Helvetica", 14))
        self.back_button.pack(pady=10)

    def logout(self):
        self.current_user = None
        self.create_login_screen()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = TypingTestApp(root)
    root.mainloop()
