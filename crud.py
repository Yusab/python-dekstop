import sqlite3
information ='''
please input the options below :
	CALCULATE to calculate anything
	ADD to create data
	READ to read data
	SEARCH to look for any data
	UPDATE to update data
	DELETE to remove data
	EXIT to close the program
'''
print("Welcome to CRUD Program with Python Console by Yusuf Abdulloh")
print(information)
global conn, cursor
conn = sqlite3.connect('testDB.db')
while True:
	options=input('enter the options: ').lower()
	
	def database():
		cursor = conn.cursor()
		cursor.execute("CREATE TABLE IF NOT EXISTS 'COMPANY'(ID integer primary key autoincrement not null,NAME text not null, AGE int not null , ADDRESS char(50), SALARY real);")
		
	def calculate():
		print('Input what you what to calculate!')
		global cal
		cal = eval(input())
		print(cal)
		
	def add():
		global naming,aging,addressing,salaries
		print('Please,input correct data!')
		naming = input('Name :') # mengisi variabel naming
		aging = input('Age :') # mengisi variabel aging
		addressing = input('Address :') # mengisi variabel addressing
		salaries = input('Salary :') # mengisi variabel salaries
		conn.execute("INSERT INTO COMPANY ( NAME, AGE, ADDRESS, SALARY) values (?,?,?,? )", (naming,aging,addressing,salaries,)); #memasukan data dengan sql ini
		conn.commit()
		print ("Enter data success!")# mencetak informasi bila sukses
		print ("+++++++++");
		showdata()
		print ("+++++++++");
		
	def showdata() :
		cursor = conn.execute("SELECT ID, NAME, ADDRESS, SALARY from COMPANY")
		for row in cursor:
			print ("ID\t= ",row[0])
			print ("NAME\t= ",row[1])
			print ("ADRRESS = ",row[2])
			print ("SALARY\t= ",row[3],"\n")
			
	def search():
		global srccolumn,searching
#default srccolumn
		print('Search data table Company, if it leave blank will be searched by ID')
		srccolumn = input('Enter searching by column :')
		if srccolumn == '':
			srccolumn = 'ID'
		searching = str(input('Search :'))
		cursor = conn.execute("SELECT ID, NAME, ADDRESS, SALARY from COMPANY where " + srccolumn +" like '"+ searching +"%';")
		for row in cursor:
			print ("ID\t= ",row[0])
			print ("NAME\t= ",row[1])
			print ("ADRRESS= ",row[2])
			print ("SALARY = ",row[3],"\n")
			print ("Operasi sukses");
			
	def delete():
		global ids
		ids = str(input('Which id do you want to delete :'))
		conn.execute('delete from COMPANY where id='+ids)
		conn.commit()
		print ("Data deleted :", conn.total_changes)
		showdata()
	
	def update():
		global ids, salaries
		ids = str(input('Enter the ID that you want to change:'))
		salaries = input('Enter salary to change:')
		conn.execute("UPDATE COMPANY set SALARY ="+ salaries +" where ID="+ ids +"")
		conn.commit()
		print ("Data Updated:", conn.total_changes)
		cursor = conn.execute("SELECT ID, NAME, ADDRESS, SALARY from COMPANY where ID="+ids)
		showdata()

	database()
	if options == 'calculate':
		calculate()
	elif options == 'add':
		add()
	elif options == 'search':
		search()
	elif options == 'read':
		showdata()
	elif options == 'update':
		update()
	elif options == 'delete':
		delete()
	elif options =='exit':
		print('Thanks for using this application')
		conn.close()
		break
	else:
		print('you choose the wrong input!')