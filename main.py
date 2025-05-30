import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.figure

class DataVisualizationGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("CSV Data Visualization Tool")
        self.root.geometry("800x600")
        
        # Data storage
        self.df = None
        self.current_file = None
        
        # Create main frame
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # File selection section
        file_frame = ttk.LabelFrame(main_frame, text="File Selection", padding="10")
        file_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        file_frame.columnconfigure(1, weight=1)
        
        ttk.Button(file_frame, text="Browse CSV File", command=self.browse_file).grid(row=0, column=0, padx=(0, 10))
        self.file_label = ttk.Label(file_frame, text="No file selected", foreground="gray")
        self.file_label.grid(row=0, column=1, sticky=(tk.W, tk.E))
        
        # Chart selection section
        chart_frame = ttk.LabelFrame(main_frame, text="Chart Options", padding="10")
        chart_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Create buttons for different chart types
        self.btn1 = ttk.Button(chart_frame, text="Issue Counts by Problem and Status", 
                              command=self.plot_issue_counts, state="disabled")
        self.btn1.grid(row=0, column=0, padx=5, pady=5, sticky=(tk.W, tk.E))
        
        self.btn2 = ttk.Button(chart_frame, text="Average Time to Solve by Problem Type", 
                              command=self.plot_avg_time_to_solve, state="disabled")
        self.btn2.grid(row=0, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))
        
        self.btn3 = ttk.Button(chart_frame, text="Issues Reported Over Time", 
                              command=self.plot_issues_over_time, state="disabled")
        self.btn3.grid(row=1, column=0, padx=5, pady=5, sticky=(tk.W, tk.E))
        
        self.btn4 = ttk.Button(chart_frame, text="Issues by Comuna and Problem Type", 
                              command=self.plot_issues_by_comuna, state="disabled")
        self.btn4.grid(row=1, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))
        
        # Configure chart frame columns to expand equally
        chart_frame.columnconfigure(0, weight=1)
        chart_frame.columnconfigure(1, weight=1)
        
        # Chart display area
        self.chart_frame = ttk.LabelFrame(main_frame, text="Chart Display", padding="10")
        self.chart_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.chart_frame.columnconfigure(0, weight=1)
        self.chart_frame.rowconfigure(0, weight=1)
        
        # Welcome message
        welcome_label = ttk.Label(self.chart_frame, text="Select a CSV file to begin", 
                                 font=("Arial", 12), foreground="gray")
        welcome_label.grid(row=0, column=0)
        
        # Store button references for enabling/disabling
        self.chart_buttons = [self.btn1, self.btn2, self.btn3, self.btn4]
        
    def browse_file(self):
        """Open file dialog to select CSV file"""
        file_path = filedialog.askopenfilename(
            title="Select CSV File",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                self.load_data(file_path)
                self.current_file = file_path
                # Show just the filename in the label
                filename = file_path.split('/')[-1] if '/' in file_path else file_path.split('\\')[-1]
                self.file_label.config(text=f"Loaded: {filename}", foreground="green")
                
                # Enable chart buttons
                for btn in self.chart_buttons:
                    btn.config(state="normal")
                    
                # Clear the chart area
                self.clear_chart_area()
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load CSV file:\n{str(e)}")
                self.file_label.config(text="Error loading file", foreground="red")
    
    def load_data(self, path):
        """Load CSV data with proper date parsing"""
        self.df = pd.read_csv(path, parse_dates=['Fecha'], dayfirst=False)
        
    def clear_chart_area(self):
        """Clear the current chart display"""
        for widget in self.chart_frame.winfo_children():
            widget.destroy()
            
    def create_matplotlib_canvas(self, fig):
        """Create and display matplotlib canvas in tkinter"""
        self.clear_chart_area()
        
        # Create a frame to hold both canvas and toolbar
        canvas_frame = ttk.Frame(self.chart_frame)
        canvas_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        canvas_frame.columnconfigure(0, weight=1)
        canvas_frame.rowconfigure(0, weight=1)
        
        canvas = FigureCanvasTkAgg(fig, canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Add toolbar for zoom, pan, etc.
        from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
        toolbar_frame = ttk.Frame(canvas_frame)
        toolbar_frame.grid(row=1, column=0, sticky=(tk.W, tk.E))
        toolbar = NavigationToolbar2Tk(canvas, toolbar_frame)
        toolbar.update()
        
    def plot_issue_counts(self):
        """Plot issue counts by problem and status"""
        if self.df is None:
            return
            
        try:
            # Create figure
            fig = matplotlib.figure.Figure(figsize=(10, 6))
            ax = fig.add_subplot(111)
            
            # Count issues by Problema and Estado
            count = self.df.groupby(['Problema', 'Estado']).size().unstack(fill_value=0)
            count.plot(kind='bar', stacked=True, ax=ax)
            
            ax.set_title('Issue Counts by Problem Type and Status')
            ax.set_xlabel('Problem Type')
            ax.set_ylabel('Number of Issues')
            ax.tick_params(axis='x', rotation=45)
            fig.tight_layout()
            
            self.create_matplotlib_canvas(fig)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create chart:\n{str(e)}")
    
    def plot_avg_time_to_solve(self):
        """Plot average time to solve by problem type"""
        if self.df is None:
            return
            
        try:
            # Create figure
            fig = matplotlib.figure.Figure(figsize=(10, 6))
            ax = fig.add_subplot(111)
            
            # Filter solved issues with TiempoSolucion values
            solved = self.df[self.df['Estado'] == 'Solucionado'].copy()
            solved['TiempoSolucion'] = pd.to_numeric(solved['TiempoSolucion'], errors='coerce')
            avg_time = solved.groupby('Problema')['TiempoSolucion'].mean().dropna()
            
            if avg_time.empty:
                messagebox.showwarning("Warning", "No solved issues with valid solution times found.")
                return
                
            avg_time.plot(kind='bar', ax=ax)
            ax.set_title('Average Time to Solve by Problem Type (days)')
            ax.set_xlabel('Problem Type')
            ax.set_ylabel('Average Days to Solve')
            ax.tick_params(axis='x', rotation=45)
            fig.tight_layout()
            
            self.create_matplotlib_canvas(fig)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create chart:\n{str(e)}")
    
    def plot_issues_over_time(self):
        """Plot number of issues reported over time"""
        if self.df is None:
            return
            
        try:
            # Create figure
            fig = matplotlib.figure.Figure(figsize=(10, 6))
            ax = fig.add_subplot(111)
            
            # Count issues by month
            df_copy = self.df.copy()
            df_copy['Month'] = df_copy['Fecha'].dt.to_period('M')
            monthly_counts = df_copy.groupby('Month').size()
            
            monthly_counts.plot(kind='line', marker='o', ax=ax)
            ax.set_title('Number of Issues Reported Over Time')
            ax.set_xlabel('Month')
            ax.set_ylabel('Number of Issues')
            fig.tight_layout()
            
            self.create_matplotlib_canvas(fig)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create chart:\n{str(e)}")
    
    def plot_issues_by_comuna(self):
        """Plot issue counts by comuna and problem type"""
        if self.df is None:
            return
            
        try:
            # Create figure
            fig = matplotlib.figure.Figure(figsize=(12, 6))
            ax = fig.add_subplot(111)
            
            # Count issues by Comuna and Problema
            comuna_problem_counts = self.df.groupby(['Comuna', 'Problema']).size().unstack(fill_value=0)
            comuna_problem_counts.plot(kind='bar', stacked=True, ax=ax)
            
            ax.set_title('Issue Counts by Comuna and Problem Type')
            ax.set_xlabel('Comuna')
            ax.set_ylabel('Number of Issues')
            ax.tick_params(axis='x', rotation=45)
            fig.tight_layout()
            
            self.create_matplotlib_canvas(fig)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create chart:\n{str(e)}")

def main():
    root = tk.Tk()
    app = DataVisualizationGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 
