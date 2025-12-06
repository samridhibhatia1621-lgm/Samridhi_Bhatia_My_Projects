import tkinter as tk
from tkinter import ttk
import subprocess

class JobSchedulerGUI:
    def __init__(self, root):
        self.root = root
        root.title(" Job Scheduler ")
        root.configure(bg="#ffe6f0")  

        tk.Label(root, text="Job Scheduling Simulator", font=("Helvetica", 18, "bold"),
                 bg="#ffe6f0", fg="#003366").pack(pady=10)

        main_frame = tk.Frame(root, bg="#ffe6f0")  
        main_frame.pack(padx=20, pady=10)

        headers = ["Burst Time", "Priority"]
        for i, text in enumerate(headers):
            tk.Label(main_frame, text=text, font=("Arial", 10, "bold"),
                     bg="#ffe6f0").grid(row=0, column=i, padx=10, pady=5)

        self.burst_entries = []
        self.priority_entries = []
        
        for i in range(5):
            b = tk.Entry(main_frame, width=10)
            p = tk.Entry(main_frame, width=10)

            b.grid(row=i + 1, column=0, padx=5, pady=2)
            p.grid(row=i + 1, column=1, padx=5, pady=2)

            self.burst_entries.append(b)
            self.priority_entries.append(p)
            

        options_frame = tk.Frame(root, bg="#ffe6f0")  
        options_frame.pack(pady=10)

        tk.Label(options_frame, text="Select Algorithm:", bg="#ffe6f0", font=("Arial", 10)).grid(row=0, column=0)
        self.algo_choice = ttk.Combobox(options_frame, values=[
            "FCFS", "SJF", "Priority Scheduling", "Round Robin"
        ])
        self.algo_choice.grid(row=0, column=1, padx=10)
        self.algo_choice.set("Priority Scheduling")

        tk.Label(options_frame, text="Quantum (if needed):", bg="#ffe6f0", font=("Arial", 10)).grid(row=0, column=2)
        self.quantum_entry = tk.Entry(options_frame, width=5)
        self.quantum_entry.grid(row=0, column=3, padx=5)

        run_btn = tk.Button(root, text=" Run Scheduler", bg="#0066cc", fg="white",
                            font=("Arial", 11, "bold"), command=self.run_scheduler)
        run_btn.pack(pady=10)

        self.output_text = tk.Text(root, height=15, width=100, bg="#FFFFFF", font=("Courier", 10)) 
        self.output_text.pack(pady=10)

    def run_scheduler(self):
        algo_map = {
            "FCFS": "1",
            "SJF": "2",
            "Priority Scheduling": "3",
            "Round Robin": "4",
        }

        input_lines = []
        valid_jobs = []

        for i in range(len(self.burst_entries)):
            burst = self.burst_entries[i].get().strip()
            priority = self.priority_entries[i].get().strip()

            if burst and priority :
                valid_jobs.append(f"{burst} {priority} ")

        if not valid_jobs:
            self.output_text.insert(tk.END, "Please enter at least one complete job.\n")
            return

        input_lines.append(str(len(valid_jobs))) 
        input_lines.extend(valid_jobs)

        algo_number = algo_map.get(self.algo_choice.get(), "1")
        input_lines.append(algo_number)

        if algo_number == "4":  
            quantum = self.quantum_entry.get().strip()
            if not quantum:
                self.output_text.insert(tk.END, " Please enter quantum for Round Robin.\n")
                return
            input_lines.append(quantum)

        input_text = "\n".join(input_lines)

        try:
            result = subprocess.run(
                ["code.exe"], 
                input=input_text,
                text=True,
                capture_output=True
            )
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, result.stdout)
        except Exception as e:
            self.output_text.insert(tk.END, f"Error: {e}\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = JobSchedulerGUI(root)
    root.mainloop()
