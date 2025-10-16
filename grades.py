import tkinter as tk
from tkinter import ttk, messagebox
import requests
class GradeApp:
    def __init__(self, root):
        self.is_dark_mode = False
        self.subjects = []
        self.selected_subject = tk.StringVar()
        self.root = root
        self.root.title("Futuristic Grade Calculator")
        self.root.geometry("900x600")
        self.root.resizable(True, True)

        # Dark mode toggle
        self.toggle_btn = tk.Button(self.root, text="🌙 Dark Mode", command=self.toggle_mode, font=("Arial", 12), bg="#222", fg="#fff")
        self.toggle_btn.pack(anchor="ne", padx=10, pady=10)

        title_label = tk.Label(self.root, text="Grade Calculator", font=("Orbitron", 20, "bold"), pady=10)
        title_label.pack()

        # Subject selection
        self.subject_frame = tk.Frame(self.root, padx=10, pady=10)
        self.subject_frame.pack()
        tk.Label(self.subject_frame, text="Select Subject:", font=("Arial", 13)).grid(row=0, column=0, sticky="e")
        self.subject_dropdown = ttk.Combobox(self.subject_frame, textvariable=self.selected_subject, font=("Arial", 13), state="readonly")
        self.subject_dropdown.grid(row=0, column=1, padx=5)
    # tk.Button(self.subject_frame, text="Load Grades", command=self.load_subject_grades, font=("Arial", 12), bg="#4CAF50", fg="white").grid(row=0, column=2, padx=5)

        # Manual entry for grades/weights
        self.input_frame = tk.Frame(self.root, padx=10, pady=10)
        self.input_frame.pack()
        tk.Label(self.input_frame, text="Number of grades:", font=("Arial", 12)).grid(row=0, column=0, sticky="e")
        self.num_grades_entry = tk.Entry(self.input_frame, font=("Arial", 12), width=10)
        self.num_grades_entry.grid(row=0, column=1, padx=5)
        tk.Button(self.input_frame, text="Next", command=self.create_grade_fields, font=("Arial", 12), bg="#4CAF50", fg="white").grid(row=0, column=2, padx=5)

        self.grade_entries = []
        self.weight_entries = []
        self.fields_canvas = None
        self.fields_frame = None
        self.scrollbar = None
        self.result_label = tk.Label(self.root, text="", font=("Arial", 13), fg="#333")
        self.result_label.pack(pady=10)
    def toggle_mode(self):
        self.is_dark_mode = not self.is_dark_mode
        if self.is_dark_mode:
            self.root.configure(bg="#181818")
            self.toggle_btn.config(text="☀️ Light Mode", bg="#444", fg="#fff")
            self.result_label.config(bg="#181818", fg="#fff")
            self.input_frame.config(bg="#181818")
            self.subject_frame.config(bg="#181818")
        else:
            self.root.configure(bg="#f0f0f0")
            self.toggle_btn.config(text="🌙 Dark Mode", bg="#222", fg="#fff")
            self.result_label.config(bg="#f0f0f0", fg="#333")
            self.input_frame.config(bg="#f0f0f0")
            self.subject_frame.config(bg="#f0f0f0")

    def load_subject_grades(self):
        # Placeholder for API call to Eljur
        try:
            # Example: response = requests.get('YOUR_ELJUR_API_URL', params={'auth_token': 'YOUR_TOKEN'})
            # grades_data = response.json()
            # self.subjects = [subject['name'] for subject in grades_data['subjects']]
            # self.subject_dropdown['values'] = self.subjects
            # messagebox.showinfo("API", "Subjects loaded from Eljur API!")
            # For demo, use static subjects:
            self.subjects = ["Math", "Physics", "English", "History"]
            self.subject_dropdown['values'] = self.subjects
            if self.subjects:
                self.selected_subject.set(self.subjects[0])
            messagebox.showinfo("Demo", "Subjects loaded! Select one to continue.")
        except Exception as e:
            messagebox.showerror("API Error", f"Failed to load grades.\nError: {e}")

    def create_grade_fields(self):
        # Optionally, you could pre-fill grades/weights from API for selected subject here
        try:
            num_grades = int(self.num_grades_entry.get())
            if num_grades <= 0:
                self.result_label.config(text="Enter a positive number.")
                return
        except ValueError:
            self.result_label.config(text="Please enter a valid number.")
            return

        if self.fields_canvas:
            self.fields_canvas.destroy()
        if self.scrollbar:
            self.scrollbar.destroy()
        self.grade_entries = []
        self.weight_entries = []

        # Create a canvas and a vertical scrollbar for scrolling
        self.fields_canvas = tk.Canvas(self.root, height=300, bg="#222" if self.is_dark_mode else "#f0f0f0")
        self.scrollbar = tk.Scrollbar(self.root, orient="vertical", command=self.fields_canvas.yview)
        self.fields_canvas.configure(yscrollcommand=self.scrollbar.set)
        self.fields_canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.fields_frame = tk.Frame(self.fields_canvas, padx=10, pady=10, bg="#222" if self.is_dark_mode else "#f0f0f0")
        self.fields_canvas.create_window((0, 0), window=self.fields_frame, anchor="nw")

        grade_label_font = ("Orbitron", 12)
        entry_font = ("Orbitron", 12)
        for i in range(num_grades):
            tk.Label(self.fields_frame, text=f"Grade {i+1}:", font=grade_label_font, fg="#00eaff" if self.is_dark_mode else "#222", bg="#222" if self.is_dark_mode else "#f0f0f0").grid(row=i, column=0, sticky="e", padx=2, pady=2)
            grade_entry = tk.Entry(self.fields_frame, font=entry_font, width=8, bg="#333" if self.is_dark_mode else "#fff", fg="#fff" if self.is_dark_mode else "#222")
            grade_entry.grid(row=i, column=1, padx=2, pady=2)
            self.grade_entries.append(grade_entry)

        for i in range(num_grades):
            tk.Label(self.fields_frame, text=f"Weight {i+1} (decimal):", font=grade_label_font, fg="#00eaff" if self.is_dark_mode else "#222", bg="#222" if self.is_dark_mode else "#f0f0f0").grid(row=i, column=2, sticky="e", padx=2, pady=2)
            weight_entry = tk.Entry(self.fields_frame, font=entry_font, width=8, bg="#333" if self.is_dark_mode else "#fff", fg="#fff" if self.is_dark_mode else "#222")
            weight_entry.grid(row=i, column=3, padx=2, pady=2)
            self.weight_entries.append(weight_entry)

        tk.Button(self.fields_frame, text="Calculate", command=self.calculate_average, font=("Orbitron", 13), bg="#00eaff" if self.is_dark_mode else "#2196F3", fg="#222" if self.is_dark_mode else "#fff").grid(row=num_grades, column=0, columnspan=4, pady=10)

        # Update scroll region
        self.fields_frame.update_idletasks()
        self.fields_canvas.config(scrollregion=self.fields_canvas.bbox("all"))
    # API integration placeholder
    # To fetch grades from your online journal, you can use:
    # import requests
    # response = requests.get('YOUR_API_URL')
    # grades_data = response.json()

    def calculate_average(self):
        try:
            grades = [float(e.get()) for e in self.grade_entries]
            weights = [float(e.get()) for e in self.weight_entries]
            if len(grades) == 0 or len(weights) == 0:
                self.result_label.config(text="Please enter all grades and weights.")
                return
            weighted_sum = sum(grades[i] * weights[i] for i in range(len(grades)))
            total_weight = sum(weights)
            if total_weight == 0:
                self.result_label.config(text="Total weight cannot be zero.")
                return
            average = weighted_sum / total_weight
            self.result_label.config(text=f"Your weighted average is: {average:.2f}")
        except ValueError:
            self.result_label.config(text="Please enter valid numbers for grades and weights.")

if __name__ == "__main__":
    root = tk.Tk()
    app = GradeApp(root)
    root.mainloop()