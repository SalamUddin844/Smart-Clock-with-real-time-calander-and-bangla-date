import tkinter as tk
from tkinter import messagebox
from tkcalendar import Calendar
import time
from datetime import datetime, timedelta
import threading

# Function to update the time display
def update_time():
    while True:
        current_time = time.strftime('%H:%M:%S %p')
        time_label.config(text=current_time)
        time.sleep(1)

# Function to set an alarm
def set_alarm():
    alarm_time = alarm_entry.get()
    if alarm_time:
        alarm_thread = threading.Thread(target=alarm_check, args=(alarm_time,))
        alarm_thread.start()
    else:
        messagebox.showwarning("Invalid Input", "Please enter a valid time.")

# Function to check if the current time matches the alarm time
def alarm_check(alarm_time):
    while True:
        current_time = datetime.now().strftime('%H:%M')
        if current_time == alarm_time:
            messagebox.showinfo("Alarm", "Time to wake up!")
            break
        time.sleep(30)  # Check every 30 seconds

# Function to update the Bengali date display
def update_bengali_date():
    while True:
        today = datetime.now()
        bd_date = gregorian_to_bengali(today.year, today.month, today.day)
        bangla_date_label.config(text=f'বাংলা তারিখ: {bd_date}')  # Display Bengali date
        time.sleep(60)  # Update every minute

# Custom function to convert Gregorian date to Bengali date
def gregorian_to_bengali(year, month, day):
    # Define the start of the Bengali year
    bengali_months = [
        "বৈশাখ", "জ্যৈষ্ঠ", "আষাঢ়", "শ্রাবণ", "ভাদ্র", "আশ্বিন",
        "কার্তিক", "অগ্রহায়ণ", "পৌষ", "মাঘ", "ফাল্গুন", "চৈত্র"
    ]
    bengali_days_in_month = [31, 31, 31, 31, 31, 30, 30, 30, 30, 30, 30, 30]

    # Calculate the starting date of the Bengali year
    if month < 4 or (month == 4 and day < 14):
        bengali_year = year - 594
    else:
        bengali_year = year - 593

    # Calculate the Bengali month and day
    start_date = datetime(year, 4, 14)
    current_date = datetime(year, month, day)
    delta = current_date - start_date
    total_days = delta.days

    # Adjust for leap years
    if total_days < 0:
        total_days += 365 + (1 if (year - 1) % 4 == 0 else 0)
        bengali_year -= 1

    bengali_month = 0
    while total_days >= bengali_days_in_month[bengali_month]:
        total_days -= bengali_days_in_month[bengali_month]
        bengali_month += 1

    bengali_day = total_days + 1
    bengali_month_name = bengali_months[bengali_month]

    return f"{bengali_day} {bengali_month_name} {bengali_year}"

# Function to resize calendar font based on window size
def resize_calendar(event):
    width = root.winfo_width()
    height = root.winfo_height()
    font_size = min(width // 50, height // 25)
    cal.configure(font=('calibri', font_size))

# Setting up the GUI
root = tk.Tk()
root.title("Smart Clock")
root.configure(bg='#f0f0f0')  # Light grey background

# Time label
time_label = tk.Label(root, font=('calibri', 40, 'bold'), background='#add8e6', foreground='#00008b')  # Light blue background, dark blue text
time_label.pack(anchor='center', pady=(20, 0))

# Alarm input
alarm_frame = tk.Frame(root, bg='#f0f0f0')  # Light grey background
alarm_frame.pack(anchor='center')

alarm_label = tk.Label(alarm_frame, text="Set Alarm (HH:MM):", font=('calibri', 12), bg='#f0f0f0', fg='#2f4f4f')  # Dark grey text
alarm_label.pack(side=tk.LEFT)

alarm_entry = tk.Entry(alarm_frame, font=('calibri', 12))
alarm_entry.pack(side=tk.LEFT)

alarm_button = tk.Button(alarm_frame, text="Set Alarm", font=('calibri', 12), command=set_alarm)
alarm_button.pack(side=tk.LEFT)

# Bengali date label
bangla_date_label = tk.Label(root, font=('calibri', 14, 'bold'), bg='#f0f0f0', fg='#2f4f4f')  # Dark grey text
bangla_date_label.pack(anchor='center', pady=10)

# Calendar
calendar_frame = tk.Frame(root, bg='#f0f0f0')  # Light grey background
calendar_frame.pack(anchor='center', pady=20, expand=True, fill=tk.BOTH)

calendar_label = tk.Label(calendar_frame, text="Select Date:", font=('calibri', 12), bg='#f0f0f0', fg='#2f4f4f')  # Dark grey text
calendar_label.pack(side=tk.TOP, padx=10)

cal = Calendar(calendar_frame, selectmode='day', font=('calibri', 14), background='white', foreground='black', headersbackground='white', normalbackground='white', weekendbackground='white', othermonthbackground='white', othermonthwebackground='white')
cal.pack(side=tk.TOP, expand=True, fill=tk.BOTH)

# Bind the resize event to the function
root.bind('<Configure>', resize_calendar)

# Start the time update thread
time_thread = threading.Thread(target=update_time)
time_thread.start()

# Start the Bengali date update thread
bengali_date_thread = threading.Thread(target=update_bengali_date)
bengali_date_thread.start()

root.mainloop()
