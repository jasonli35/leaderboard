# Necessary Imports
import mysql.connector as mysql                   # Used for interacting with the MySQL database
import os                                         # Used for interacting with the system environment
from dotenv import load_dotenv                    # Used to read the credentials
import bcrypt
import json

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# Configuration
load_dotenv('credentials.env')                 # Read in the environment variables for MySQL
db_config = {
  "host": os.environ['MYSQL_HOST'],
  "user": os.environ['MYSQL_USER'],
  "password": os.environ['MYSQL_PASSWORD'],
  "database": os.environ['MYSQL_DATABASE']
}
session_config = {
  'session_key': os.environ['SESSION_KEY']
}

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# Define helper functions for CRUD operations
# CREATE SQL query
def create_user(first_name:str, last_name:str, username:str, password:str) -> int:
  password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

  db = mysql.connect(**db_config)
  
  cursor = db.cursor()
  query = "insert into User (first_name, last_name, username, password) values (%s, %s, %s, %s)"
  values = (first_name, last_name, username, password)
  cursor.execute(query, values)
  db.commit()
  db.close()
  return cursor.lastrowid

# SELECT SQL query
def select_users(user_id:int=None) -> list:
  db = mysql.connect(**db_config)
  cursor = db.cursor()
  if user_id == None:
    query = f"select id, first_name, last_name, username from User;"
    cursor.execute(query)
    result = cursor.fetchall()
  else:
    query = f"select id, first_name, last_name, username from User where id={user_id};"
    cursor.execute(query)
    result = cursor.fetchone()
  db.close()
  return result

#select user by user name
def select_users_by_uname(user_name:str) -> list:
  db = mysql.connect(**db_config)
  cursor = db.cursor()
  query = f"select email from User where username='{user_name}';"
  try:
    cursor.execute(query)
  except RuntimeError as err:
    print("runtime error: {0}".format(err))
  result = cursor.fetchone()
  db.close()
  return result

# UPDATE SQL query
def update_user(user_id:int, first_name:str, last_name:str, username:str, password:str) -> bool:
  password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
  db = mysql.connect(**db_config)
  cursor = db.cursor()
  query = "update users set first_name=%s, last_name=%s, username=%s, password=%s where id=%s;"
  values = (first_name, last_name, username, password, user_id)
  try:
    cursor.execute(query, values)
  except RuntimeError as err:
   print("runtime error: {0}".format(err))
  db.commit()
  db.close()
  return True if cursor.rowcount == 1 else False

# UPDATE password by id
def update_password(user_id:int, password:str) -> bool:
  password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
  db = mysql.connect(**db_config)
  cursor = db.cursor()
  query = "update User set password=%s where id=%s;"
  values = (password, user_id)
  try:
    cursor.execute(query, values)
  except RuntimeError as err:
   print("runtime error: {0}".format(err))
  db.commit()
  db.close()
  return True if cursor.rowcount == 1 else False

# UPDATE user name by id
def update_userName(user_id:int, user_name:str) -> bool:
 
  db = mysql.connect(**db_config)
  cursor = db.cursor()
  query = "update User set username=%s where id=%s;"
  values = (user_name, user_id)
  try:
    cursor.execute(query, values)
  except RuntimeError as err:
   print("runtime error: {0}".format(err))
  db.commit()
  db.close()
  return True if cursor.rowcount == 1 else False

# UPDATE email by id
def update_email(user_id:int, email:str) -> bool:
 
  db = mysql.connect(**db_config)
  cursor = db.cursor()
  query = "update User set email=%s where id=%s;"
  values = (email, user_id)
  try:
    cursor.execute(query, values)
  except RuntimeError as err:
   print("runtime error: {0}".format(err))
  db.commit()
  db.close()
  return True if cursor.rowcount == 1 else False


# DELETE SQL query
def delete_user(user_id:int) -> bool:
  db = mysql.connect(**db_config)
  cursor = db.cursor()
  cursor.execute(f"delete from User where id={user_id};")
  db.commit()
  db.close()
  return True if cursor.rowcount == 1 else False

# SELECT query to verify hashed password of users; if password is correct return user id; otherwise return nothing
def check_user_password(username:str, password:str) -> bool:
  db = mysql.connect(**db_config)
  cursor = db.cursor()
  query = 'select password, id from User where username=%s'
  cursor.execute(query, (username,))
  result = cursor.fetchone()
  cursor.close()
  db.close()

  if result is not None:
    if(bcrypt.checkpw(password.encode('utf-8'), result[0].encode('utf-8'))):
      return result[1]
    
  return None