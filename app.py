import psycopg2
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
HOST = config['database']['host']
PORT = config['database']['port']
DBNAME = config['database']['dbname']
USER = config['database']['user']
PASSWORD = config['database']['password']

class User:
	def __init__(self, first_name, last_name, email, password, active=True):
		self.first_name = first_name
		self.last_name = last_name
		self.email = email
		self.password = password
		self.active = active
		self.username = first_name[0].lower() + '_' + last_name.lower()

	def __str__(self):
		return f"User info:\nusername - {self.username}\nfirst name - {self.first_name}\nlast name - {self.last_name}\nemail - {self.email}\n"

class Storage:
	def __init__(self, host, port, dbname, user, password):
		self.host = host
		self.port = port
		self.dbname = dbname
		self.user = user
		self.password = password

	def connect(self):
		try:
			self.connection = psycopg2.connect(
				host = HOST,
				port = PORT,
				dbname = DBNAME,
				user = USER,
				password = PASSWORD
			)
			print(f"Connection to database {DBNAME} established successfully!")
		except Exception as e:
			print(f"Error: {e}")

	def close_connection(self):
		try:
			self.connection.close()
			print("Connection closed")
		except Exception as e:
			print(f"Error: {e}")

	def save_user(self, user: User):
		cursor = self.connection.cursor()
		try:
			cursor.execute("BEGIN;")
			cursor.execute("""INSERT INTO s_user (first_name, last_name, email, password, username)
				           VALUES (%s, %s, %s, %s, %s);""", (user.first_name, user.last_name,
				           user.email, user.password, user.username))
			self.connection.commit()
			print(f"User {user.username} was saved successfully")
			cursor.close()
			self.close_connection()
		except Exception as e:
			print(f"Error: {e}")
			self.connection.rollback()
			cursor.close()
			self.close_connection()

	#TODO
	def show_users(self):
		pass

storage = Storage(HOST, PORT, DBNAME, USER, PASSWORD)

while True:
	check = input("New registration? y/n: ")
	if check == 'y':
		print("Registration")
		first_name = input("Your first name: ")
		last_name = input("Your last name: ")
		email = input("Your email: ")
		password = input("Your password: ")

		user = User(first_name, last_name, email, password)
		storage.connect()
		storage.save_user(user)
	elif check == 'n':
		break
	else:
		print("Input correct value")