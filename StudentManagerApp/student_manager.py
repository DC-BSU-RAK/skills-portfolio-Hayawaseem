import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import os
from PIL import Image, ImageTk
import pygame

class StudentManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Manager")
        self.root.geometry("1000x700")
        self.root.configure(bg='#2c3e50')
        
        # Initialize pygame mixer for sound - this will handle the click sounds
        self.init_sound()
        
        # Set window icon with correct path - using our custom icon
        self.set_window_icon()
        
        # Colors for the UI - using a modern color scheme
        self.colors = {
            'primary': '#3498db',      # Blue
            'secondary': '#2ecc71',    # Green
            'accent': '#e74c3c',       # Red
            'warning': '#f39c12',      # Orange
            'dark_bg': '#2c3e50',      # Dark blue-gray
            'light_bg': '#34495e',     # Lighter blue-gray
            'text_light': '#ecf0f1',   # Light text
            'text_dark': '#2c3e50'     # Dark text
        }
        
        # Initialize data - this will store all our student records
        self.students = []
        self.filename = "studentMarks.txt"  # File to save/load data
        self.images = {}  # Dictionary to store images for the UI
        
        # Load images and data when the app starts
        self.load_images()
        self.load_data()
        
        # Create the main GUI - build the user interface
        self.create_gui()
    
    def init_sound(self):
        """Initialize pygame mixer for sound effects - for button clicks"""
        try:
            pygame.mixer.init()
            # Load click sound from our project folder
            script_dir = os.path.dirname(os.path.abspath(__file__))
            click_sound_path = os.path.join(script_dir, "click.wav")
            
            if os.path.exists(click_sound_path):
                self.click_sound = pygame.mixer.Sound(click_sound_path)
                # Set volume to a reasonable level (0.0 to 1.0)
                self.click_sound.set_volume(0.3)
            else:
                print(f"Click sound file not found at: {click_sound_path}")
                self.click_sound = None
        except Exception as e:
            print(f"Error initializing sound: {e}")
            self.click_sound = None
    
    def play_click_sound(self):
        """Play the click sound effect when buttons are pressed"""
        try:
            if self.click_sound:
                self.click_sound.play()
        except Exception as e:
            print(f"Error playing click sound: {e}")
    
    def set_window_icon(self):
        """Set the main window icon from icon.ico file in StudentManagerApp folder"""
        try:
            # Get the directory where this script is located
            script_dir = os.path.dirname(os.path.abspath(__file__))
            # Construct the full path to the icon file
            icon_path = os.path.join(script_dir, "icon.ico")
            
            # Use the icon.ico file from the StudentManagerApp folder
            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
                print(f"Icon loaded from: {icon_path}")
            else:
                print(f"Icon file not found at: {icon_path}")
        except Exception as e:
            print(f"Error setting window icon: {e}")
    
    def load_images(self):
        """Load and resize images for the UI"""
        try:
            # Create sample images using PIL since we don't have actual image files
            self.create_sample_images()
        except Exception as e:
            print(f"Image loading error: {e}")
    
    def create_sample_images(self):
        """Create sample images programmatically for buttons and banners"""
        # Main banner image - just a colored rectangle
        banner_img = Image.new('RGB', (800, 150), color='#3498db')
        self.images['banner'] = ImageTk.PhotoImage(banner_img)
        
        # Button icons (simple colored circles) - different colors for different buttons
        icon_size = (30, 30)
        colors = ['#3498db', '#2ecc71', '#e74c3c', '#f39c12', '#9b59b6', '#1abc9c', '#d35400', '#c0392b']
        
        for i, color in enumerate(colors):
            img = Image.new('RGB', icon_size, color=color)
            self.images[f'icon_{i}'] = ImageTk.PhotoImage(img)
    
    def load_data(self):
        """Load student data from file - or create sample data if file doesn't exist"""
        try:
            if os.path.exists(self.filename):
                with open(self.filename, 'r') as file:
                    lines = file.readlines()
                    for line in lines[1:]:  # Skip the first line (count)
                        data = line.strip().split(',')
                        if len(data) >= 6:
                            student = {
                                'code': int(data[0]),
                                'name': data[1],
                                'mark1': int(data[2]),
                                'mark2': int(data[3]),
                                'mark3': int(data[4]),
                                'exam': int(data[5])
                            }
                            self.students.append(student)
            else:
                self.create_sample_data()  # Create sample data if no file exists
        except Exception as e:
            messagebox.showerror("Error", f"Error loading data: {str(e)}")
            self.create_sample_data()
    
    def create_sample_data(self):
        """Create sample data with some realistic student records"""
        sample_data = [
            [1345, "John Curry", 8, 15, 7, 45],
            [2345, "Sam Sturtivant", 14, 15, 14, 77],
            [9876, "Lee Scott", 17, 11, 16, 99],
            [3724, "Matt Thompson", 19, 11, 15, 81],
            [1212, "Ron Herrema", 14, 17, 18, 66],
            [8439, "Jake Hobbs", 10, 11, 10, 43],
            [2344, "Jo Hyde", 6, 15, 10, 55],
            [9384, "Gareth Southgate", 5, 6, 8, 33],
            [8327, "Alan Shearer", 20, 20, 20, 100],
            [2983, "Les Ferdinand", 15, 17, 18, 92]
        ]
        
        for data in sample_data:
            student = {
                'code': data[0],
                'name': data[1],
                'mark1': data[2],
                'mark2': data[3],
                'mark3': data[4],
                'exam': data[5]
            }
            self.students.append(student)
        
        self.save_data()  # Save the sample data to file
    
    def save_data(self):
        """Save student data to file - called whenever data changes"""
        try:
            with open(self.filename, 'w') as file:
                file.write(f"{len(self.students)}\n")  # First line is count
                for student in self.students:
                    file.write(f"{student['code']},{student['name']},{student['mark1']},{student['mark2']},{student['mark3']},{student['exam']}\n")
        except Exception as e:
            messagebox.showerror("Error", f"Error saving data: {str(e)}")
    
    def calculate_totals(self, student):
        """Calculate total coursework, overall percentage and grade for a student"""
        coursework_total = student['mark1'] + student['mark2'] + student['mark3']
        total_marks = coursework_total + student['exam']
        percentage = (total_marks / 160) * 100  # 160 is max possible marks
        
        # Determine grade based on percentage
        if percentage >= 70:
            grade = 'A'
        elif percentage >= 60:
            grade = 'B'
        elif percentage >= 50:
            grade = 'C'
        elif percentage >= 40:
            grade = 'D'
        else:
            grade = 'F'
        
        return coursework_total, total_marks, percentage, grade
    
    def create_glow_button(self, parent, text, command, color, width=300, height=50):
        """Create a button with glow effect and hover animation"""
        button_frame = tk.Frame(parent, bg=self.colors['dark_bg'])
        
        # Create a wrapper function that plays sound and then executes the command
        def sound_command():
            self.play_click_sound()  # Play click sound first
            command()  # Then execute the original command
        
        # Main button with styling
        button = tk.Button(button_frame, 
                          text=text,
                          command=sound_command,  # Use our sound wrapper
                          font=('Arial', 11, 'bold'),
                          bg=color,
                          fg=self.colors['text_light'],
                          relief='flat',
                          bd=0,
                          width=25,
                          height=2,
                          cursor='hand2')
        
        button.pack(padx=2, pady=2)
        
        # Hover effects - button changes color when mouse is over it
        def on_enter(e):
            button.configure(bg=self.lighten_color(color, 20))
            button_frame.configure(bg=self.lighten_color(color, 40))
        
        def on_leave(e):
            button.configure(bg=color)
            button_frame.configure(bg=self.colors['dark_bg'])
        
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)
        
        return button_frame
    
    def lighten_color(self, color, amount):
        """Lighten a color by given amount - used for hover effects"""
        color = color.lstrip('#')
        rgb = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        light_rgb = tuple(min(255, c + amount) for c in rgb)
        return f'#{light_rgb[0]:02x}{light_rgb[1]:02x}{light_rgb[2]:02x}'
    
    def create_gui(self):
        """Create the enhanced GUI - the main user interface"""
        # Main frame with gradient background
        main_frame = tk.Frame(self.root, bg=self.colors['dark_bg'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Header with banner - the top section of the app
        header_frame = tk.Frame(main_frame, bg=self.colors['primary'], height=120)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        header_frame.pack_propagate(False)  # Don't let the frame shrink
        
        title_label = tk.Label(header_frame, 
                              text="Student Manager", 
                              font=("Arial", 24, "bold"),
                              bg=self.colors['primary'],
                              fg=self.colors['text_light'])
        title_label.pack(expand=True)
        
        subtitle_label = tk.Label(header_frame,
                                text="Manage Student Records Efficiently",
                                font=("Arial", 12),
                                bg=self.colors['primary'],
                                fg=self.colors['text_light'])
        subtitle_label.pack(expand=True)
        
        # Content frame - holds the menu and results area
        content_frame = tk.Frame(main_frame, bg=self.colors['dark_bg'])
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left menu frame - contains all the action buttons
        menu_frame = tk.Frame(content_frame, bg=self.colors['light_bg'], relief='ridge', bd=2, width=350)
        menu_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        menu_frame.pack_propagate(False)  # Prevent frame from shrinking
        
        # Menu title
        menu_title = tk.Label(menu_frame, 
                             text="Menu Options", 
                             font=("Arial", 14, "bold"),
                             bg=self.colors['light_bg'],
                             fg=self.colors['text_light'])
        menu_title.pack(pady=20)
        
        # Button colors - different colors for different functions
        button_colors = [
            self.colors['primary'],    # View All - Blue
            self.colors['secondary'],  # Individual - Green
            '#f39c12',                # Highest - Orange
            '#e74c3c',                # Lowest - Red
            '#9b59b6',                # Sort - Purple
            '#1abc9c',                # Add - Teal
            '#d35400',                # Delete - Dark Orange
            '#c0392b'                 # Update - Dark Red
        ]
        
        # Basic menu buttons section
        basic_label = tk.Label(menu_frame,
                             text="Core Features:",
                             font=("Arial", 11, "bold"),
                             bg=self.colors['light_bg'],
                             fg=self.colors['text_light'])
        basic_label.pack(pady=(10, 5))
        
        # Define all the menu buttons and their functions
        buttons_data = [
            ("View All Student Records", self.view_all_students),
            ("View Individual Student", self.view_individual_student),
            ("Highest Total Score", self.show_highest_student),
            ("Lowest Total Score", self.show_lowest_student),
            ("Sort Student Records", self.sort_students),
            ("Add Student Record", self.add_student),
            ("Delete Student Record", self.delete_student),
            ("Update Student Record", self.update_student)
        ]
        
        self.menu_buttons = []
        for i, (text, command) in enumerate(buttons_data):
            btn_frame = self.create_glow_button(menu_frame, text, command, button_colors[i])
            btn_frame.pack(fill=tk.X, padx=15, pady=8)
            self.menu_buttons.append(btn_frame)
        
        # Statistics frame - shows quick stats at the bottom of the menu
        stats_frame = tk.Frame(menu_frame, bg=self.colors['light_bg'])
        stats_frame.pack(fill=tk.X, side=tk.BOTTOM, pady=20)
        
        stats_label = tk.Label(stats_frame,
                             text="Quick Stats:",
                             font=("Arial", 11, "bold"),
                             bg=self.colors['light_bg'],
                             fg=self.colors['text_light'])
        stats_label.pack()
        
        self.stats_text = tk.Label(stats_frame,
                                 text=f"Students: {len(self.students)}",
                                 font=("Arial", 10),
                                 bg=self.colors['light_bg'],
                                 fg=self.colors['text_light'])
        self.stats_text.pack(pady=5)
        
        # Results frame - where all the student data is displayed
        results_main_frame = tk.Frame(content_frame, bg=self.colors['dark_bg'])
        results_main_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        results_header = tk.Label(results_main_frame,
                                text="Results Display",
                                font=("Arial", 14, "bold"),
                                bg=self.colors['dark_bg'],
                                fg=self.colors['text_light'])
        results_header.pack(pady=(0, 10))
        
        self.results_frame = tk.Frame(results_main_frame, bg=self.colors['light_bg'], relief='sunken', bd=2)
        self.results_frame.pack(fill=tk.BOTH, expand=True)
        
        # Text widget for displaying results with styling - like a console output
        self.results_text = tk.Text(self.results_frame, 
                                   width=80, 
                                   height=25, 
                                   wrap=tk.WORD,
                                   font=("Consolas", 10),  # Monospace font for alignment
                                   bg='#f8f9fa',  # Light background for readability
                                   fg=self.colors['text_dark'],
                                   relief='flat',
                                   padx=10,
                                   pady=10)
        
        # Create scrollbar for the text widget
        scrollbar = ttk.Scrollbar(self.results_frame, orient=tk.VERTICAL, command=self.results_text.yview)
        self.results_text.configure(yscrollcommand=scrollbar.set)
        
        self.results_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Configure tags for colored text - different colors for different content
        self.results_text.tag_configure('header', foreground='#2c3e50', font=('Arial', 12, 'bold'))
        self.results_text.tag_configure('success', foreground='#27ae60')  # Green for good grades
        self.results_text.tag_configure('warning', foreground='#e67e22')  # Orange for average grades
        self.results_text.tag_configure('error', foreground='#e74c3c')    # Red for poor grades
        self.results_text.tag_configure('highlight', background='#fff3cd')  # Yellow highlight
    
    def clear_results(self):
        """Clear the results text area - like clearing a whiteboard"""
        self.results_text.delete(1.0, tk.END)
    
    def display_student(self, student, show_header=False):
        """Display a single student's information with colors based on grades"""
        coursework_total, total_marks, percentage, grade = self.calculate_totals(student)
        
        if show_header:
            # Display column headers for the first student
            header = f"{'Name':<20} {'Code':<8} {'Coursework':<12} {'Exam':<8} {'Total':<8} {'Percentage':<10} {'Grade':<6}\n"
            self.results_text.insert(tk.END, header, 'header')
            self.results_text.insert(tk.END, "─" * 80 + "\n")  # Separator line
        
        # Color code based on grade - visual feedback for performance
        grade_color = 'success' if grade in ['A', 'B'] else 'warning' if grade in ['C', 'D'] else 'error'
        
        line = f"{student['name']:<20} {student['code']:<8} {coursework_total:<12} {student['exam']:<8} {total_marks:<8} {percentage:<10.1f} "
        self.results_text.insert(tk.END, line)
        self.results_text.insert(tk.END, f"{grade:<6}\n", grade_color)  # Grade with color
    
    def update_stats(self):
        """Update the statistics display - keeps the student count current"""
        self.stats_text.config(text=f"Students: {len(self.students)}")
    
    def view_all_students(self):
        """View all student records - like showing the entire class list"""
        self.clear_results()
        self.results_text.insert(tk.END, "ALL STUDENT RECORDS\n", 'header')
        self.results_text.insert(tk.END, "=" * 50 + "\n\n")
        
        if not self.students:
            self.results_text.insert(tk.END, "No student records found.\n", 'error')
            return
        
        # Display header for the first student
        self.display_student(self.students[0], show_header=True)
        
        # Display all students and calculate average
        total_percentage = 0
        for student in self.students:
            self.display_student(student)
            _, _, percentage, _ = self.calculate_totals(student)
            total_percentage += percentage
        
        # Display summary statistics
        avg_percentage = total_percentage / len(self.students)
        self.results_text.insert(tk.END, "\n" + "=" * 50 + "\n")
        self.results_text.insert(tk.END, "SUMMARY:\n", 'header')
        self.results_text.insert(tk.END, f"Number of students: {len(self.students)}\n", 'success')
        self.results_text.insert(tk.END, f"Average percentage: {avg_percentage:.1f}%\n", 'success')
        
        self.update_stats()  # Refresh the stats display
    
    def view_individual_student(self):
        """View individual student record - like looking up one student's report card"""
        if not self.students:
            messagebox.showwarning("Warning", "No student records available.")
            return
        
        # Create a list of student names for selection
        student_names = [f"{student['code']} - {student['name']}" for student in self.students]
        
        selection = self.create_selection_dialog("Select Student", "Choose a student:", student_names)
        if selection is not None:
            selected_student = self.students[selection]
            self.clear_results()
            self.results_text.insert(tk.END, "INDIVIDUAL STUDENT RECORD\n", 'header')
            self.results_text.insert(tk.END, "=" * 50 + "\n\n")
            self.display_student(selected_student, show_header=True)
    
    def show_highest_student(self):
        """Show student with highest overall mark - the top performer"""
        if not self.students:
            messagebox.showwarning("Warning", "No student records available.")
            return
        
        # Find student with highest total marks
        highest_student = max(self.students, key=lambda s: self.calculate_totals(s)[1])
        
        self.clear_results()
        self.results_text.insert(tk.END, "STUDENT WITH HIGHEST OVERALL MARK\n", 'header')
        self.results_text.insert(tk.END, "=" * 50 + "\n\n")
        self.display_student(highest_student, show_header=True)
    
    def show_lowest_student(self):
        """Show student with lowest overall mark - for identifying who needs help"""
        if not self.students:
            messagebox.showwarning("Warning", "No student records available.")
            return
        
        # Find student with lowest total marks
        lowest_student = min(self.students, key=lambda s: self.calculate_totals(s)[1])
        
        self.clear_results()
        self.results_text.insert(tk.END, "STUDENT WITH LOWEST OVERALL MARK\n", 'header')
        self.results_text.insert(tk.END, "=" * 50 + "\n\n")
        self.display_student(lowest_student, show_header=True)
    
    def sort_students(self):
        """Sort student records by total marks - ascending or descending"""
        if not self.students:
            messagebox.showwarning("Warning", "No student records available.")
            return
        
        # Ask user for sort order
        order = messagebox.askquestion("Sort Order", "Sort in ascending order?\n(Click 'No' for descending order)")
        ascending = (order == 'yes')
        
        # Sort students by total marks
        self.students.sort(key=lambda s: self.calculate_totals(s)[1], reverse=not ascending)
        
        self.clear_results()
        if ascending:
            self.results_text.insert(tk.END, "STUDENT RECORDS (ASCENDING ORDER)\n", 'header')
        else:
            self.results_text.insert(tk.END, "STUDENT RECORDS (DESCENDING ORDER)\n", 'header')
        
        self.results_text.insert(tk.END, "=" * 50 + "\n\n")
        self.display_student(self.students[0], show_header=True)
        
        for student in self.students:
            self.display_student(student)
    
    def add_student(self):
        """Add a new student record - like enrolling a new student"""
        dialog = AddStudentDialog(self.root, self.colors, self.play_click_sound)
        self.root.wait_window(dialog.top)
        
        if dialog.result:
            new_student = dialog.result
            # Check if student code already exists
            if any(student['code'] == new_student['code'] for student in self.students):
                messagebox.showerror("Error", "Student code already exists!")
                return
            
            self.students.append(new_student)
            self.save_data()
            messagebox.showinfo("Success", "Student record added successfully!")
            self.view_all_students()  # Refresh the view
    
    def delete_student(self):
        """Delete a student record - like removing a student from the system"""
        if not self.students:
            messagebox.showwarning("Warning", "No student records available.")
            return
        
        student_names = [f"{student['code']} - {student['name']}" for student in self.students]
        
        selection = self.create_selection_dialog("Delete Student", "Select student to delete:", student_names)
        if selection is not None:
            student = self.students[selection]
            # Confirm deletion to prevent accidents
            confirm = messagebox.askyesno("Confirm Delete", 
                                         f"Are you sure you want to delete {student['name']}?")
            if confirm:
                del self.students[selection]
                self.save_data()
                messagebox.showinfo("Success", "Student record deleted successfully!")
                self.view_all_students()
    
    def update_student(self):
        """Update a student record - like correcting information or updating marks"""
        if not self.students:
            messagebox.showwarning("Warning", "No student records available.")
            return
        
        student_names = [f"{student['code']} - {student['name']}" for student in self.students]
        
        selection = self.create_selection_dialog("Update Student", "Select student to update:", student_names)
        if selection is not None:
            student = self.students[selection]
            dialog = UpdateStudentDialog(self.root, student, self.colors, self.play_click_sound)
            self.root.wait_window(dialog.top)
            
            if dialog.result:
                self.students[selection] = dialog.result
                self.save_data()
                messagebox.showinfo("Success", "Student record updated successfully!")
                self.view_all_students()
    
    def create_selection_dialog(self, title, prompt, options):
        """Create a selection dialog with colors and icon - for choosing students"""
        dialog = CustomSelectionDialog(self.root, title, prompt, options, self.colors, self.play_click_sound)
        self.root.wait_window(dialog.top)
        return dialog.result


class CustomSelectionDialog:
    def __init__(self, parent, title, prompt, options, colors, play_sound_callback):
        self.colors = colors
        self.play_sound_callback = play_sound_callback
        self.result = None
        
        self.top = tk.Toplevel(parent)
        self.top.title(title)
        self.top.geometry("500x400")
        self.top.configure(bg=colors['dark_bg'])
        self.top.transient(parent)  # Dialog stays on top of parent
        self.top.grab_set()  # Make dialog modal
        
        # Set the same icon as main window
        self.set_dialog_icon()
        
        # Title of the dialog
        title_label = tk.Label(self.top, text=title, 
                              font=("Arial", 16, "bold"),
                              bg=colors['dark_bg'],
                              fg=colors['text_light'])
        title_label.pack(pady=15)
        
        # Prompt text telling user what to do
        prompt_label = tk.Label(self.top, text=prompt,
                               font=("Arial", 11),
                               bg=colors['dark_bg'],
                               fg=colors['text_light'],
                               wraplength=450)  # Wrap long text
        prompt_label.pack(pady=10)
        
        # Listbox frame - where the student list appears
        list_frame = tk.Frame(self.top, bg=colors['light_bg'], relief='sunken', bd=1)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Listbox with scrollbar - for displaying the student options
        self.listbox = tk.Listbox(list_frame, 
                                 font=("Arial", 10),
                                 bg='#f8f9fa',
                                 fg=colors['text_dark'],
                                 selectbackground=colors['primary'],  # Selected item color
                                 selectforeground=colors['text_light'],
                                 relief='flat')
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.listbox.yview)
        self.listbox.configure(yscrollcommand=scrollbar.set)
        
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=5)
        
        # Add options to listbox - the student names
        for option in options:
            self.listbox.insert(tk.END, option)
        
        # Button frame - Select and Cancel buttons
        button_frame = tk.Frame(self.top, bg=colors['dark_bg'])
        button_frame.pack(pady=15)
        
        def select_with_sound():
            self.play_sound_callback()
            self.select_item()
        
        def cancel_with_sound():
            self.play_sound_callback()
            self.cancel()
        
        select_btn = tk.Button(button_frame, text="Select", 
                              command=select_with_sound,
                              bg=colors['secondary'],
                              fg=colors['text_light'],
                              font=("Arial", 11, "bold"),
                              width=12,
                              cursor='hand2')
        select_btn.pack(side=tk.LEFT, padx=10)
        
        cancel_btn = tk.Button(button_frame, text="Cancel", 
                              command=cancel_with_sound,
                              bg=colors['accent'],
                              fg=colors['text_light'],
                              font=("Arial", 11),
                              width=12,
                              cursor='hand2')
        cancel_btn.pack(side=tk.LEFT, padx=10)
        
        # Bind double-click to select with sound - convenience feature
        def double_click_with_sound(e):
            self.play_sound_callback()
            self.select_item()
        
        self.listbox.bind('<Double-Button-1>', double_click_with_sound)
        
        # Select first item by default - so user can just press Enter
        if options:
            self.listbox.selection_set(0)
            self.listbox.activate(0)
    
    def set_dialog_icon(self):
        """Set the dialog icon from icon.ico file in StudentManagerApp folder"""
        try:
            # Get the directory where this script is located
            script_dir = os.path.dirname(os.path.abspath(__file__))
            # Construct the full path to the icon file
            icon_path = os.path.join(script_dir, "icon.ico")
            
            # Use the icon.ico file from the StudentManagerApp folder
            if os.path.exists(icon_path):
                self.top.iconbitmap(icon_path)
            else:
                print(f"Icon file not found at: {icon_path}")
        except Exception as e:
            print(f"Error setting dialog icon: {e}")
    
    def select_item(self):
        """Select the current item - when user clicks Select or double-clicks"""
        selection = self.listbox.curselection()
        if selection:
            self.result = selection[0]  # Return the index of selected item
            self.top.destroy()
        else:
            tk.messagebox.showwarning("Warning", "Please select a student first.")
    
    def cancel(self):
        """Cancel the operation - when user clicks Cancel"""
        self.top.destroy()


class AddStudentDialog:
    def __init__(self, parent, colors, play_sound_callback):
        self.colors = colors
        self.play_sound_callback = play_sound_callback
        self.top = tk.Toplevel(parent)
        self.top.title("Add New Student")
        self.top.geometry("400x400")
        self.top.configure(bg=colors['dark_bg'])
        self.top.transient(parent)
        self.top.grab_set()  # Modal dialog
        
        self.result = None  # Will store the new student data
        
        # Title of the add student dialog
        title_label = tk.Label(self.top, text="Add New Student", 
                              font=("Arial", 16, "bold"),
                              bg=colors['dark_bg'],
                              fg=colors['text_light'])
        title_label.pack(pady=20)
        
        # Form frame - where all the input fields go
        form_frame = tk.Frame(self.top, bg=colors['dark_bg'])
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20)
        
        # Create form fields - labels and input boxes
        self.create_form_field(form_frame, "Student Code:", 0)
        self.create_form_field(form_frame, "Student Name:", 1)
        self.create_form_field(form_frame, "Course Mark 1 (0-20):", 2)
        self.create_form_field(form_frame, "Course Mark 2 (0-20):", 3)
        self.create_form_field(form_frame, "Course Mark 3 (0-20):", 4)
        self.create_form_field(form_frame, "Exam Mark (0-100):", 5)
        
        # Buttons - Add and Cancel
        button_frame = tk.Frame(self.top, bg=colors['dark_bg'])
        button_frame.pack(pady=20)
        
        def add_with_sound():
            self.play_sound_callback()
            self.add_student()
        
        def cancel_with_sound():
            self.play_sound_callback()
            self.cancel()
        
        add_btn = tk.Button(button_frame, text="Add Student", 
                           command=add_with_sound,
                           bg=colors['secondary'],
                           fg=colors['text_light'],
                           font=("Arial", 12, "bold"),
                           width=15,
                           cursor='hand2')
        add_btn.pack(side=tk.LEFT, padx=10)
        
        cancel_btn = tk.Button(button_frame, text="Cancel", 
                              command=cancel_with_sound,
                              bg=colors['accent'],
                              fg=colors['text_light'],
                              font=("Arial", 12),
                              width=15,
                              cursor='hand2')
        cancel_btn.pack(side=tk.LEFT, padx=10)
    
    def create_form_field(self, parent, label_text, row):
        """Create a form field with label and entry - for inputting student data"""
        label = tk.Label(parent, text=label_text,
                        bg=self.colors['dark_bg'],
                        fg=self.colors['text_light'],
                        font=("Arial", 10))
        label.grid(row=row, column=0, sticky=tk.W, pady=8)
        
        entry = tk.Entry(parent, font=("Arial", 10), width=30)
        entry.grid(row=row, column=1, pady=8, padx=10)
        
        # Store reference to entry so we can get the values later
        setattr(self, f'entry_{row}', entry)
    
    def add_student(self):
        """Add the new student - validate input and create student record"""
        try:
            # Get values from all input fields
            code = int(self.entry_0.get())
            name = self.entry_1.get()
            mark1 = int(self.entry_2.get())
            mark2 = int(self.entry_3.get())
            mark3 = int(self.entry_4.get())
            exam = int(self.entry_5.get())
            
            # Validate input ranges
            if not (1000 <= code <= 9999):
                messagebox.showerror("Error", "Student code must be between 1000 and 9999")
                return
            
            if not (0 <= mark1 <= 20 and 0 <= mark2 <= 20 and 0 <= mark3 <= 20):
                messagebox.showerror("Error", "Course marks must be between 0 and 20")
                return
            
            if not (0 <= exam <= 100):
                messagebox.showerror("Error", "Exam mark must be between 0 and 100")
                return
            
            # Create the student dictionary
            self.result = {
                'code': code,
                'name': name,
                'mark1': mark1,
                'mark2': mark2,
                'mark3': mark3,
                'exam': exam
            }
            
            self.top.destroy()  # Close the dialog
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for all fields")
    
    def cancel(self):
        """Cancel the operation - close dialog without adding"""
        self.top.destroy()

class UpdateStudentDialog(AddStudentDialog):
    def __init__(self, parent, student, colors, play_sound_callback):
        super().__init__(parent, colors, play_sound_callback)
        self.top.title("Update Student")  # Different title for update
        
        # Pre-fill fields with current values - so user can see what they're updating
        self.entry_0.insert(0, str(student['code']))
        self.entry_1.insert(0, student['name'])
        self.entry_2.insert(0, str(student['mark1']))
        self.entry_3.insert(0, str(student['mark2']))
        self.entry_4.insert(0, str(student['mark3']))
        self.entry_5.insert(0, str(student['exam']))
        
        # Make code read-only - student code shouldn't change
        self.entry_0.config(state='readonly')

def main():
    root = tk.Tk()
    app = StudentManager(root)
    root.mainloop()

if __name__ == "__main__":
    main()
