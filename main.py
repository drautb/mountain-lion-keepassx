import os
import sys
import ttk

from Tkinter import *
from pykeepass import PyKeePass


# Database Parameters
DATABASE_FILE =  os.environ["DATABASE_FILE"] or sys.argv[1]
DATABASE_PASSWORD = os.environ["DATABASE_PASSWORD"] or sys.argv[2]


# Load Database
kp = PyKeePass(DATABASE_FILE, DATABASE_PASSWORD)

all_entries = kp.find_entries_by_title(".*", True)
entry_titles = map(lambda e: e.title, kp.find_entries_by_title(".*", True))


# Setup GUI
master = Tk()

# Left Side - Listbox of entries
left_frame = Frame(master)
left_frame.pack(fill=BOTH, expand=1, side=LEFT)

selected_entry = ()
entry_choices = Listbox(left_frame, listvariable=selected_entry)
entry_choices.pack(padx=5, pady=5, fill=BOTH, expand=1)

for entry in all_entries:
    entry_choices.insert(END, entry.title)

# Right side, RO data
right_frame = Frame(master)
right_frame.pack(fill=BOTH, expand=1, side=RIGHT)

# Username frame
username_frame = Frame(right_frame)
username_frame.pack()

username_label = Label(username_frame, text="Username:")
username_label.pack(side=LEFT)

username_value = StringVar()
username_field = Entry(username_frame, textvariable=username_value, width=50)
username_field.pack(side=RIGHT)

# Password frame
password_frame = Frame(right_frame)
password_frame.pack()

password_label = Label(password_frame, text="Password:")
password_label.pack(side=LEFT)

password_value = StringVar()
password_field = Entry(password_frame, textvariable=password_value, width=50)
password_field.pack(side=RIGHT)

def callback():
  selected_indicies_tuple = entry_choices.curselection()
  if (len(selected_indicies_tuple) == 1):
    entry_title = entry_choices.get(selected_indicies_tuple[0])
    entry = kp.find_entry_by_title(entry_title)
    if (entry != None):
      username_value.set(entry.username)
      password_value.set(entry.password)

b = Button(right_frame, text="Refresh", command=callback)
b.pack()

mainloop()
