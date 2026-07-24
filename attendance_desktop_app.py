import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# Setup Django Environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school_management.settings')
import django
django.setup()

from apps.users.models import User
from apps.academics.models import StudentProfile
from apps.attendance.models import StudentAttendance, TeacherAttendance

# Attempt to import holidays, fallback if not installed
try:
    import holidays
    HAS_HOLIDAYS = True
except ImportError:
    HAS_HOLIDAYS = False

class AttendanceSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Attendance Management System (Django DB)")
        self.root.geometry("900x700")
        self.root.config(bg="#f0f2f5")

        self.students = []
        self.staff = []
        self.student_attendance = {}
        self.staff_attendance = {}

        self.today_date = datetime.now().date()
        self.today_date_str = self.today_date.strftime("%Y-%m-%d")
        
        # Holiday Detection
        self.is_holiday_today = False
        self.holiday_name = ""
        if HAS_HOLIDAYS:
            # Using Bangladesh as region
            bd_holidays = holidays.BD()
            if self.today_date in bd_holidays:
                self.is_holiday_today = True
                self.holiday_name = bd_holidays.get(self.today_date)
            # Weekend detection (Friday/Saturday in BD)
            if self.today_date.weekday() in [4, 5]: # Friday is 4, Saturday is 5
                self.is_holiday_today = True
                self.holiday_name = "Weekend"
        
        self.fetch_django_data()
        self.build_ui()
        self.load_initial_data()

    def fetch_django_data(self):
        # Fetch Students (from StudentProfile)
        for student in StudentProfile.objects.select_related('user').all():
            self.students.append({
                "id": student.id,
                "roll": student.roll_number,
                "name": student.user.get_full_name() or student.user.username,
                "profile": student
            })
            
        # Fetch Teachers (from User where role='TEACHER')
        for teacher in User.objects.filter(role='TEACHER'):
            self.staff.append({
                "id": teacher.id,
                "roll": f"T-{teacher.id}",
                "name": teacher.get_full_name() or teacher.username,
                "profile": teacher
            })

    def build_ui(self):
        # Header
        header = tk.Frame(self.root, bg="#0d3b66", height=60)
        header.pack(fill="x")
        title_text = "📚 Advanced Attendance System"
        if self.is_holiday_today:
            title_text += f" - [HOLIDAY: {self.holiday_name}]"
            
        title_label = tk.Label(
            header, text=title_text, font=("Arial", 16, "bold"), fg="white", bg="#0d3b66"
        )
        title_label.pack(pady=15)

        # Date Display
        date_frame = tk.Frame(self.root, bg="#f0f2f5")
        date_frame.pack(fill="x", padx=20, pady=5)
        tk.Label(date_frame, text=f"Date: {self.today_date_str}", font=("Arial", 12, "bold"), bg="#f0f2f5").pack(side="left")
        
        if not HAS_HOLIDAYS:
            tk.Label(date_frame, text="(Install 'holidays' library for auto holiday detection: pip install holidays)", fg="red", bg="#f0f2f5").pack(side="left", padx=10)

        # Tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=20, pady=10)

        # Create Tab Frames
        self.tab_students = ttk.Frame(self.notebook)
        self.tab_staff = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_students, text="🎓 Student Attendance")
        self.notebook.add(self.tab_staff, text="👨‍🏫 Staff/Teacher Attendance")

        self.build_student_tab()
        self.build_staff_tab()

    def build_student_tab(self):
        # Control Frame
        control = tk.Frame(self.tab_students)
        control.pack(fill="x", pady=5)
        tk.Button(control, text="Mark All Present", bg="#28a745", fg="white", command=lambda: self.mark_all("student", "Present")).pack(side="right", padx=5)
        tk.Button(control, text="Simulate Fingerprint Scan 🖐️", bg="#17a2b8", fg="white", command=lambda: self.simulate_fingerprint("student")).pack(side="left", padx=5)

        # Table
        self.student_tree = self.create_treeview(self.tab_students)

        # Actions
        actions = tk.Frame(self.tab_students)
        actions.pack(fill="x", pady=10)
        
        tk.Button(actions, text="Present", bg="#198754", fg="white", width=10, command=lambda: self.set_status(self.student_tree, self.student_attendance, "Present")).grid(row=0, column=0, padx=5)
        tk.Button(actions, text="Absent", bg="#dc3545", fg="white", width=10, command=lambda: self.set_status(self.student_tree, self.student_attendance, "Absent")).grid(row=0, column=1, padx=5)
        tk.Button(actions, text="Late", bg="#ffc107", fg="black", width=10, command=lambda: self.set_status(self.student_tree, self.student_attendance, "Late")).grid(row=0, column=2, padx=5)
        
        # Student specific leaves
        tk.Button(actions, text="Personal Leave", bg="#6c757d", fg="white", width=15, command=lambda: self.set_status(self.student_tree, self.student_attendance, "Personal Leave")).grid(row=0, column=3, padx=5)
        
        tk.Button(actions, text="💾 Save to Database", bg="#0d6efd", fg="white", command=self.save_student_data).grid(row=0, column=4, padx=20)

    def build_staff_tab(self):
        # Control Frame
        control = tk.Frame(self.tab_staff)
        control.pack(fill="x", pady=5)
        tk.Button(control, text="Mark All Present", bg="#28a745", fg="white", command=lambda: self.mark_all("staff", "Present")).pack(side="right", padx=5)
        tk.Button(control, text="Simulate Fingerprint Scan 🖐️", bg="#17a2b8", fg="white", command=lambda: self.simulate_fingerprint("staff")).pack(side="left", padx=5)

        # Table
        self.staff_tree = self.create_treeview(self.tab_staff)

        # Actions
        actions = tk.Frame(self.tab_staff)
        actions.pack(fill="x", pady=10)
        
        tk.Button(actions, text="Present", bg="#198754", fg="white", width=10, command=lambda: self.set_status(self.staff_tree, self.staff_attendance, "Present")).grid(row=0, column=0, padx=2)
        tk.Button(actions, text="Absent", bg="#dc3545", fg="white", width=10, command=lambda: self.set_status(self.staff_tree, self.staff_attendance, "Absent")).grid(row=0, column=1, padx=2)
        
        # Staff specific leaves
        tk.Button(actions, text="Casual Leave", bg="#6f42c1", fg="white", width=12, command=lambda: self.set_status(self.staff_tree, self.staff_attendance, "Casual Leave")).grid(row=0, column=2, padx=2)
        tk.Button(actions, text="Special Leave", bg="#e83e8c", fg="white", width=12, command=lambda: self.set_status(self.staff_tree, self.staff_attendance, "Special Leave")).grid(row=0, column=3, padx=2)
        tk.Button(actions, text="Holiday", bg="#fd7e14", fg="white", width=12, command=lambda: self.set_status(self.staff_tree, self.staff_attendance, "Holiday")).grid(row=0, column=4, padx=2)

        tk.Button(actions, text="💾 Save to Database", bg="#0d6efd", fg="white", command=self.save_staff_data).grid(row=0, column=5, padx=20)


    def create_treeview(self, parent_frame):
        frame = tk.Frame(parent_frame)
        frame.pack(fill="both", expand=True, pady=5)
        
        columns = ("id", "name", "status")
        tree = ttk.Treeview(frame, columns=columns, show="headings")
        tree.heading("id", text="ID / Roll")
        tree.heading("name", text="Name")
        tree.heading("status", text="Attendance Status")

        tree.column("id", width=100, anchor="center")
        tree.column("name", width=300, anchor="w")
        tree.column("status", width=200, anchor="center")

        tree.pack(side="left", fill="both", expand=True)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        return tree

    def load_initial_data(self):
        default_status = "Pending"
        if self.is_holiday_today:
            default_status = f"Holiday"
            
        for s in self.students:
            uid = s["id"]
            
            # Check if attendance already exists for today
            existing_record = StudentAttendance.objects.filter(student_id=uid, date=self.today_date).first()
            if existing_record:
                status = existing_record.status
            else:
                status = default_status
                
            self.student_attendance[uid] = status
            self.student_tree.insert("", "end", iid=uid, values=(s["roll"], s["name"], status))
            
        for s in self.staff:
            uid = s["id"]
            
            existing_record = TeacherAttendance.objects.filter(teacher_id=uid, date=self.today_date).first()
            if existing_record:
                status = existing_record.status
            else:
                status = default_status
                
            self.staff_attendance[uid] = status
            self.staff_tree.insert("", "end", iid=uid, values=(s["roll"], s["name"], status))

    def set_status(self, tree, data_dict, status):
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a person from the list!")
            return
        
        for item in selected_item:
            uid = item # The iid is the database ID
            roll = tree.item(item, "values")[0]
            name = tree.item(item, "values")[1]
            data_dict[int(uid)] = status
            tree.item(item, values=(roll, name, status))

    def mark_all(self, person_type, status):
        if person_type == "student":
            tree = self.student_tree
            data_list = self.students
            data_dict = self.student_attendance
        else:
            tree = self.staff_tree
            data_list = self.staff
            data_dict = self.staff_attendance
            
        for p in data_list:
            uid = p["id"]
            roll = p["roll"]
            name = p["name"]
            data_dict[uid] = status
            tree.item(uid, values=(roll, name, status))

    def simulate_fingerprint(self, person_type):
        tree = self.student_tree if person_type == "student" else self.staff_tree
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showinfo("Digital Attendance", "Simulating scan...\nPlease select a row first to simulate scanning THAT person's fingerprint.")
            return
            
        for item in selected_item:
            uid = int(item)
            roll = tree.item(item, "values")[0]
            name = tree.item(item, "values")[1]
            status = "Present (Biometric)"
            if person_type == "student":
                self.student_attendance[uid] = status
            else:
                self.staff_attendance[uid] = status
            tree.item(item, values=(roll, name, status))
        messagebox.showinfo("Success", "Fingerprint authenticated successfully!")

    def save_student_data(self):
        if not self.student_attendance:
            messagebox.showerror("Error", "No student data to save!")
            return
            
        try:
            for student_info in self.students:
                uid = student_info["id"]
                status = self.student_attendance.get(uid, "Pending")
                profile = student_info["profile"]
                
                # Create or Update Record
                StudentAttendance.objects.update_or_create(
                    student=profile,
                    date=self.today_date,
                    defaults={
                        'status': status,
                    }
                )
            messagebox.showinfo("Success", "Student attendance saved to Django Database successfully!")
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to save: {str(e)}")

    def save_staff_data(self):
        if not self.staff_attendance:
            messagebox.showerror("Error", "No staff data to save!")
            return
            
        try:
            for staff_info in self.staff:
                uid = staff_info["id"]
                status = self.staff_attendance.get(uid, "Pending")
                profile = staff_info["profile"]
                
                # Create or Update Record
                TeacherAttendance.objects.update_or_create(
                    teacher=profile,
                    date=self.today_date,
                    defaults={
                        'status': status,
                    }
                )
            messagebox.showinfo("Success", "Staff/Teacher attendance saved to Django Database successfully!")
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to save: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = AttendanceSystem(root)
    root.mainloop()
