#import modules
import tkinter as tk
import sqlite3
import tkinter.messagebox as tkMessageBox
from tkinter import ttk
win = tk.Tk()
win.title('CRUD Tkinter')

#buat fungsi-fungsi
def database():
	global conn, cursor
	conn = sqlite3.connect('testDB.db')
	cursor = conn.cursor()
	cursor.execute("CREATE TABLE IF NOT EXISTS 'COMPANY'(ID integer primary key autoincrement not null,NAME text not null, AGE int not null , ADDRESS char(50), SALARY real);")
	
def entry():
	database()
	conn.execute("INSERT INTO COMPANY ( NAME, AGE, ADDRESS, SALARY) values (?,?,?,? )", (name.get(),age.get(),address.get(),salary.get(),));
	conn.commit()
	sta.configure(text = 'Status :Entry data success!')
	sta.configure(foreground = 'green')
	read()
	clear()
	
def clear():
	name.set("")
	age.set(0)
	address.set('')
	salary.set(0)

def read():
	tree.delete(*tree.get_children())
	database()
	cursor.execute("SELECT * FROM COMPANY ORDER BY NAME")
	fetch = cursor.fetchall()
	for data in fetch:
		tree.insert('', 'end', values=(data[0], data[1], data[2], data[3], data[4]))
	cursor.close()
	conn.close()
	sta.config(text="Successfully read the data from database",foreground="black")

def onSelected(event):
	clear()
	global ID
	curItem = tree.focus()
	contents =(tree.item(curItem))
	selecteditem = contents['values']
	ID = selecteditem[0]
	name.set(selecteditem[1])
	age.set(selecteditem[2])
	address.set(selecteditem[3])
	salary.set(selecteditem[4])

def update():
	database()
	if salary.get() == 0:
		sta.config(text="Please input salary", foreground="red")
	else:
		tree.delete(*tree.get_children())
		cursor.execute("UPDATE COMPANY SET NAME = ?, AGE = ?, ADDRESS =?, SALARY = ? WHERE ID = ?", (name.get(),age.get(),address.get(),salary.get(), int(ID)))
		conn.commit()
	conn.close()
	clear()
	read()
	sta.config(text="Successfully updated the data", foreground="black")

def remove():
	if not tree.selection():
		sta.config(text="Please select an item first", foreground="red")
	else:
		result = tkMessageBox.askquestion('Manipulation Data Application Python', 'Are you sure you want to delete this record?', icon="warning")
		if result == 'yes':
			curItem = tree.focus()
			contents =(tree.item(curItem))
			selecteditem = contents['values']
			tree.delete(curItem)
			database()
			cursor.execute("DELETE FROM COMPANY WHERE ID = %d" % selecteditem[0])
			conn.commit()
			cursor.close()
			conn.close()
			sta.config(text="Successfully deleted the data", foreground="black")

#buat variabel-variabel
name = tk.StringVar()
age = tk.IntVar()
address = tk.StringVar()
salary = tk.IntVar()

#menginisiasi komponen-komponen
labTittle = ttk.Label(win, font=(16), foreground='#0000FF', text='Add An employee')
labNama = ttk.Label(win, text='Name ')
labAge = ttk.Label(win, text='Age ')
labAddress = ttk.Label(win, text='Address')
labSalary = ttk.Label(win, text='Salary')
sta = ttk.Label(win, text='Status :')

#colom-colom
colName = ttk.Entry(win, textvariable=name)
colAge = ttk.Entry(win, textvariable=age)
colAddress = ttk.Entry(win, textvariable=address)
colSalary = ttk.Entry(win, textvariable=salary)

#Tombol tombol
bAdd = ttk.Button(win, text='Add', command=entry)
bReset = ttk.Button(win, text='Reset', command=clear)
bUpdate = ttk.Button(win, text='Update', command=update)
bRemove = ttk.Button(win, text='Remove', command=remove)

#menempatkan komponen-komponen
labTittle.grid(column=1,sticky=tk.W+tk.E)
labNama.grid(column=0,row=1)
labAge.grid(column=0,row=2)
labAddress.grid(column=0,row=3)
labSalary.grid(column=0,row=4)
sta.grid(column=1,row=5,sticky=tk.W+tk.E)
colName.grid(column=1, row=1)
colAge.grid(column=1, row=2)
colAddress.grid(column=1, row=3)
colSalary.grid(column=1, row=4)
bAdd.grid(column=2, row=0,sticky=tk.W+tk.E)
bReset.grid(column=2, row=1,sticky=tk.W+tk.E)
bUpdate.grid(column=2, row=2,sticky=tk.W+tk.E)
bRemove.grid(column=2, row=3,sticky=tk.W+tk.E)

#menambahkan Treeview
tree = ttk.Treeview(win,columns=("ID", "NAME", "AGE", "ADDRESS", "SALARY"), selectmode="extended", height=500)
tree.heading('ID', text="ID", anchor='w')
tree.heading('NAME', text="NAME", anchor='w')
tree.heading('AGE', text="AGE", anchor='w')
tree.heading('ADDRESS', text="ADDRESS", anchor='w')
tree.heading('SALARY', text="SALARY", anchor='w')
tree.column('#0', stretch=False, minwidth=0, width=0)
tree.column('#1', stretch=False, minwidth=0, width=40)
tree.column('#2', stretch=False, minwidth=0, width=120)
tree.column('#3', stretch=False, minwidth=0, width=40)
tree.column('#4', stretch=False, minwidth=0, width=120)
tree.grid(column=0,columnspan=3,row=7)
tree.bind('<Double-Button-1>', onSelected)

#menjalankan applikasi
read()
win.mainloop()