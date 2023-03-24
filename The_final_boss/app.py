from fastapi import FastAPI, Request, Response, Form
from fastapi.responses import Response
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles   # Used for serving static files
import uvicorn
from fastapi.responses import RedirectResponse
from urllib.request import urlopen
from urllib.request import urlopen
from pydantic import BaseModel                    # Used to define the model matching the DB Schema
import mysql.connector as mysql
from fastapi.templating import Jinja2Templates    # Used for generating HTML from templatized files
import os
import mysql.connector as mysql
from dotenv import load_dotenv
import dbutils as db                              # Import helper module of database functions!
import bcrypt
# Use MySQL for storing session data
from sessiondb import Sessions
from typing import Optional

sessions = Sessions(db.db_config, secret_key=db.session_config['session_key'], expiry=600000)

app = FastAPI()

views = Jinja2Templates(directory='views')        # Specify where the HTML files are located
app.mount('/public', StaticFiles(directory='public'), name='public')

pwd_salt = bcrypt.gensalt()

class User(BaseModel):
   uname: str
   psw: str
   email: str


#route for main page
@app.get("/", response_class=HTMLResponse)
def get_html() -> HTMLResponse:
   with open("views/index.html") as html:
       return HTMLResponse(content=html.read())

#route for registration page
@app.get("/registration", response_class=HTMLResponse)
def get_html() -> HTMLResponse:
   with open("views/registration.html") as html:
       return HTMLResponse(content=html.read())
   
#route for login page
@app.get("/log", response_class=HTMLResponse)
def get_html() -> HTMLResponse:
   with open("views/login.html") as html:
       return HTMLResponse(content=html.read())



load_dotenv('credentials.env')

# Read Database connection variables
db_host = os.environ['MYSQL_HOST']
db_user = os.environ['MYSQL_USER']
db_pass = os.environ['MYSQL_PASSWORD']
db_name = os.environ['MYSQL_DATABASE']


#validate if unique in database when user try to register
def isNotValidateReg(email, pid, username):
    db =mysql.connect(user=db_user, password=db_pass, host=db_host,database=db_name)
    cursor = db.cursor()
    query = "SELECT * FROM User WHERE email = %s;"
    values=(email,)
    cursor.execute(query, values)
    isEmail = cursor.fetchone()
    query = "SELECT * FROM User WHERE student_id = %s"
    values = (pid,)
    cursor.execute(query, values)
    isid = cursor.fetchone()

    query = "SELECT * FROM User WHERE username = %s;"
    values=(username,)
    cursor.execute(query, values)
    isUsername = cursor.fetchone()
    

    if isEmail is not None or isid is not None or isUsername is not None:
        return True
    else:
        return False


#post request for account registration
@app.post("/reg/{fname}/{lname}/{sid}/{email}/{uname}/{psw}")
def addAccount(email:str,fname:str,lname:str,psw:str, sid:str,uname:str):
     db =mysql.connect(user=db_user, password=db_pass, host=db_host,database=db_name)
     cursor = db.cursor()
     

     if isNotValidateReg(email,sid,uname):
        print("here")
        return 0
       
     else:
        pwd = bcrypt.hashpw(psw.encode('utf-8'), pwd_salt)
     
        query = 'insert into User (first_name, last_name, student_id, email, username, password) values (%s, %s, %s, %s, %s, %s);'
        values = (fname, lname, sid, email, uname, pwd)
        cursor.execute(query, values)

#Commit the changes and close the connection
        db.commit()
        cursor.close()
        db.close()
        return 1


# A function to authenticate users when trying to login or use protected routes
def authenticate_user(username:str, password:str) -> bool:


  return db.check_user_password(username, password)

#handle post request for log in
@app.post("/log/{uname}/{password}")
def post_login(uname:str, password:str, request:Request, response:Response) -> dict:
  
  session = sessions.get_session(request)
  if len(session) > 0:
    sessions.end_session(request, response)

  # Authenticate the user
  userid = authenticate_user(uname, password)
  if userid != None:
    session_data = {'username': uname, 'logged_in': True, 'user_id': userid}
    session_id = sessions.create_session(response, session_data)
    
    return {'message': 'Login successful', 'session_id': session_id}
  else:
    print("session is not created")
    return {'message': 'Invalid username or password', 'session_id': 0}
  

@app.get('/home', response_class=HTMLResponse)
def get_home(request:Request) -> HTMLResponse:
  session = sessions.get_session(request)
  print(len(session))
  print(session.get('logged_in'))
  if len(session) > 0 and session.get('logged_in'):
    session_id = request.cookies.get("session_id")
    
    print("password is correct! sucsseful")

    template_data = {'request':request, 'session':session, 'session_id':session_id}
    return views.TemplateResponse('home.html', template_data)
  else:
    return RedirectResponse(url="/log", status_code=302)

@app.post('/logout')
def post_logout(request:Request, response:Response):
  sessions.end_session(request, response)
  # return RedirectResponse(url="/log", status_code=302)
  

@app.put("/modify/{id}")
def modify_setting(id:int,user: User):
   if(user.uname != ""):
      db.update_userName(id, user.uname)
   if(user.psw != ""):
      db.update_password(id,user.psw)
   if(user.email != ""):
      db.update_email(id,user.email)
   
 #request to get the mvp page  
@app.get('/mvp', response_class=HTMLResponse)
def get_home(request:Request) -> HTMLResponse:
  session = sessions.get_session(request)

  if len(session) > 0 and session.get('logged_in'):
    
     with open("views/mvp.html") as html:
       return HTMLResponse(content=html.read())
  else:
    return RedirectResponse(url="/log", status_code=302)

#request to get the leaderboard page  
@app.get('/leaderboard', response_class=HTMLResponse)
def get_home(request:Request) -> HTMLResponse:
  session = sessions.get_session(request)
  if len(session) > 0 and session.get('logged_in'):
    
     with open("views/leaderboard.html") as html:
       return HTMLResponse(content=html.read())
  else:
    return RedirectResponse(url="/log", status_code=302)


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=6543, reload=True)



