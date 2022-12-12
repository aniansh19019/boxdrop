import pyrebase
import maskpass
import dill
from sqlitedict import SqliteDict


firebaseConfig = {
    "apiKey": "AIzaSyBYHMt5pzxnrfgm_2_LUJHyJzCAGOK8KzI",
    "authDomain": "cldcauth.firebaseapp.com",
    "databaseURL": "",
    "projectId": "cldcauth",
    "storageBucket": "cldcauth.appspot.com",
    "messagingSenderId": "661364563492",
    "appId": "1:661364563492:web:7eeb520dfff35399c8c2b1"
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth=firebase.auth()
db = SqliteDict("userLoginState.sqlite")
USER = False


def is_logged_in():
    loggedFlag = db["loggedFlag"]
    return loggedFlag


def user_email():
    if not is_logged_in():
        return "None"
    global USER
    USER = db["user"]
    return USER["email"]


def register():
    
    print("\n______________\nRegister new account")
    email = input("\nEnter email:")
    password=maskpass.askpass(prompt="Enter password (atleast 6 characters):", mask="*")
    rpassword=maskpass.askpass(prompt="Confirm password:", mask="*")

    if (password!=rpassword):
        print("Passwords do not match.")
        return
    
    try:
        user = auth.create_user_with_email_and_password(email, password)
        print("Successful")
        user = auth.sign_in_with_email_and_password(email, password)
        loggedIn(user)
        # print(user)
    except:
        print("Registration Failed")


def login():
    print("\n______________\nLogin")
    email = input("\nEnter email:")
    password=maskpass.askpass(prompt="Enter password:", mask="*")

    try:
        user = auth.sign_in_with_email_and_password(email, password)
        loggedIn(user)
    except:
        print("Login failed")


def loggedIn(user):
    print("\n______________\nLoggedIn!\n")
    global USER
    USER = user

    # Saving login state in SqliteDict
    db["loggedFlag"] = True
    db["user"] = USER
    db.commit()


def logout():
    # Saving login state in SqliteDict
    global USER
    USER = False
    db["loggedFlag"] = False
    db["user"] = False
    db.commit()


def interface():
    while (1):
        z = input("\n______________\nWelcome to BoxDrop\nEnter\n0 -> Exit\n1 -> Register a new account\n2 -> Log In\n")
        if z=="0":
            return False
        elif z=="1":
            register()
            return True
        elif z=="2":
            login()
            return True
        else:
            print("Invalid input, try again")


# interface()
# print(is_logged_in())
# print(user_email())
# logout()
