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
entry_titles = map(lambda e: e.title, all_entries)
entry_titles = sorted(list(set(entry_titles)))

def refresh_entries(search_value):
  if search_value is None:
    search_value = ""
  else:
    search_value = search_value.get().lower()
  entry_choices.delete(0, END)
  for title in entry_titles:
    if search_value in title.lower():
      entry_choices.insert(END, title)

# Setup GUI
master = Tk()
master.title("KeePassX")
master.minsize(640, 480)

# Left Side
left_frame = Frame(master)
left_frame.pack(fill=BOTH, expand=1, side=LEFT)

# Search bar
search_frame = Frame(left_frame)
search_frame.pack()

search_label = Label(search_frame, text="Search:")
search_label.pack(side=LEFT)

search_value = StringVar()
search_field = Entry(search_frame, textvariable=search_value, width=30)
search_field.pack(side=RIGHT)

search_value.trace("w", lambda name, index, mode, sv=search_value: refresh_entries(sv))

# Listbox of entries
selected_entry = ()
entry_choices = Listbox(left_frame, listvariable=selected_entry)
entry_choices.pack(padx=5, pady=5, fill=BOTH, expand=1)
refresh_entries(None)

entry_choices.bind('<Double-1>', lambda x: refresh_data())
entry_choices.bind('<<ListboxSelect>>', lambda x: refresh_data())

# Right side, RO data
right_frame = Frame(master)
right_frame.pack(fill=BOTH, expand=1, side=RIGHT)

# Title Frame
title_frame = Frame(right_frame)
title_frame.pack()

title_label = Label(title_frame, text="Title:")
title_label.pack(side=LEFT)

title_value = StringVar()
title_field = Entry(title_frame, textvariable=title_value, width=50)
title_field.pack(side=RIGHT)

# URL Frame
url_frame = Frame(right_frame)
url_frame.pack()

url_label = Label(url_frame, text="URL:")
url_label.pack(side=LEFT)

url_value = StringVar()
url_field = Entry(url_frame, textvariable=url_value, width=50)
url_field.pack(side=RIGHT)

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

# Notes Frame
notes_frame = Frame(right_frame)
notes_frame.pack()

notes_label = Label(notes_frame, text="Notes:")
notes_label.pack(side=LEFT)

notes_value = StringVar()
notes_field = Message(notes_frame, width=300, textvariable=notes_value)
notes_field.pack(side=RIGHT)


def refresh_data():
  selected_indicies_tuple = entry_choices.curselection()
  if (len(selected_indicies_tuple) == 1):
    entry_title = entry_choices.get(selected_indicies_tuple[0])
    entry = kp.find_entry_by_title(entry_title)
    if (entry != None):
      title_value.set(entry.title)
      url_value.set(entry.url)
      username_value.set(entry.username)
      password_value.set(entry.password)
      notes_value.set(entry.notes)

mainloop()
