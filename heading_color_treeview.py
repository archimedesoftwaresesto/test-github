import tkinter as tk
from tkinter import ttk

root = tk.Tk()

style = ttk.Style()
style.theme_use("alt")#this line is important in order to add background color in the heading section

style.configure("My.Treeview.Heading",
                background='green',
                foreground ='white')
style.map('My.Treeview.Heading',background=[('active','red')])#this line for hovering over the heading section

columns = ("Name", "Age", "Email")

my_table = ttk.Treeview(root,style="My.Treeview",columns=columns)
my_table.heading("#0",text="Number")
my_table.heading("Name",text="Name")
my_table.heading("Age",text="Age")
my_table.heading("Email",text="Email")
my_table.pack(fill=tk.BOTH,expand=True)


root.mainloop()