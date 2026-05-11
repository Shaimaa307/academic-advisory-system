import tkinter as tk
from tkinter import ttk, messagebox
from forward_chain import ForwardChainEngine

class AdvisoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("✨ Academic Expert System ")
        self.root.geometry("850x700")
        
        # --- Summer Korean Aesthetic Palette ---
        self.bg_color = "#FFF9F0"      # Creamy White (Soft Sand)
        self.header_color = "#FFB7B2"  # Pastel Peach (Sunset)
        self.accent_mint = "#BFFCC6"   # Soft Mint
        self.accent_blue = "#B2E2F2"   # Sky Blue
        self.text_color = "#5D5D5D"    # Soft Charcoal
        
        self.root.configure(bg=self.bg_color)
        
        # --- Custom Style for TTK ---
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure("TEntry", fieldbackground="white", borderwidth=0)
        self.style.configure("TCombobox", fieldbackground="white", borderwidth=0)

        # --- Header ---
        header_frame = tk.Frame(root, bg=self.header_color, height=80)
        header_frame.pack(fill=tk.X)
        
        tk.Label(header_frame, text="Academic Advisor", font=("Malgun Gothic", 22, "bold"), 
                 bg=self.header_color, fg="white").pack(pady=15)

        # --- Main Container ---
        main_content = tk.Frame(root, bg=self.bg_color, padx=30, pady=20)
        main_content.pack(expand=True, fill="both")

        # --- Input Card ---
        input_card = tk.LabelFrame(main_content, text=" ✨ Student Profile ", font=("Malgun Gothic", 10, "bold"),
                                   bg="white", fg=self.text_color, padx=20, pady=20, relief="flat")
        input_card.pack(fill=tk.X, pady=10)

        # GPA Input
        tk.Label(input_card, text="Current GPA:", font=("Malgun Gothic", 10), bg="white", fg=self.text_color).grid(row=0, column=0, sticky="w", pady=10)
        self.gpa_input = ttk.Entry(input_card, width=25)
        self.gpa_input.insert(0, "3.8")
        self.gpa_input.grid(row=0, column=1, padx=20)

        # Credits Input
        tk.Label(input_card, text="Completed Credits:", font=("Malgun Gothic", 10), bg="white", fg=self.text_color).grid(row=1, column=0, sticky="w", pady=10)
        self.credits_input = ttk.Entry(input_card, width=25)
        self.credits_input.insert(0, "95")
        self.credits_input.grid(row=1, column=1, padx=20)

        # Career Interest (Combobox for better look)
        tk.Label(input_card, text="Career Focus:", font=("Malgun Gothic", 10), bg="white", fg=self.text_color).grid(row=2, column=0, sticky="w", pady=10)
        self.interest_cb = ttk.Combobox(input_card, values=["ai", "software", "cybersecurity", "data_science"], width=23)
        self.interest_cb.set("ai")
        self.interest_cb.grid(row=2, column=1, padx=20)

        # --- Action Button ---
        self.run_btn = tk.Button(main_content, text="Analyze Profile", command=self.run, 
                                 bg=self.accent_blue, fg=self.text_color, font=("Malgun Gothic", 11, "bold"),
                                 relief="flat", padx=40, pady=10, cursor="hand2", activebackground=self.accent_mint)
        self.run_btn.pack(pady=20)

        # --- Output Area with Tabs ---
        self.tabs = ttk.Notebook(main_content)
        self.tabs.pack(expand=True, fill="both")

        # Tab 1: Summary (Report)
        self.summary_box = tk.Text(self.tabs, font=("Malgun Gothic", 11), bg="white", fg=self.text_color, 
                                   padx=15, pady=15, relief="flat", height=10)
        self.tabs.add(self.summary_box, text=" Advisory Report ")

        # Tab 2: Logic Trace (Reasoning)
        self.trace_box = tk.Text(self.tabs, font=("Consolas", 10), bg="#F8F9FA", fg="#7F8C8D", 
                                 padx=15, pady=15, relief="flat")
        self.tabs.add(self.trace_box, text=" Reasoning Trace ")

    def run(self):
        try:
            # Re-initialize engine for fresh run
            engine = ForwardChainEngine()
            engine.load({
                "gpa": float(self.gpa_input.get()),
                "total_credits": int(self.credits_input.get()),
                "career_interest": self.interest_cb.get(),
                "courses_this_semester": 5
            })
            engine.run()
            
            # Clear previous results
            self.summary_box.delete(1.0, tk.END)
            self.trace_box.delete(1.0, tk.END)
            
            res = engine.summary()
            
            # Stylized Summary Report[cite: 3]
            report = (
                f"🌟 ADVISORY REPORT\n"
                f"{'─'*30}\n"
                f"🎓 Academic Standing : {res['standing']}\n"
                f"📊 Student Level     : {res['level']}\n"
                f"🚀 Career Path       : {res['career_track']}\n"
                f"✨ Honors Status     : {'Qualified' if res['is_honors'] else 'Not yet'}\n"
                f"{'─'*30}\n"
                f"💡 Recommendations: {', '.join(res['recommendations']) if res['recommendations'] else 'Keep up the good work!'}\n"
            )
            
            self.summary_box.insert(tk.END, report)
            
            # Detailed Logic Trace[cite: 3, 5]
            self.trace_box.insert(tk.END, "⚙️ SYSTEM LOGIC TRACE:\n\n" + "\n".join(engine.get_trace()))
            
            # Auto-switch to report tab
            self.tabs.select(0)
            
        except Exception as e:
            messagebox.showerror("Input Error", "Please ensure GPA and Credits are numeric!")

if __name__ == "__main__":
    root = tk.Tk()
    app = AdvisoryApp(root)
    root.mainloop()