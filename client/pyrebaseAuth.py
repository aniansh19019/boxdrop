import pyrebase
import maskpass


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
loggedFlag = False


def is_logged_in():
    return loggedFlag


def user_email(user):
    return user["email"]


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
    global loggedFlag
    loggedFlag = True
    # print(user)

    while (1):
        z = input("\nWelcome User:"+user["email"]+"\nEnter\n0 -> Sign Out\n1 -> Print idToken\n2 -> call is_logged_in()\n3 -> call user_email()\n4 -> user info\n")
        if z=="0":
            loggedFlag = False
            return
        elif z=="1":
            print(user["idToken"])
        elif z=="2":
            print(is_logged_in())
        elif z=="3":
            print(user_email(user))
        elif z=="4":
            print(auth.get_account_info(user["idToken"]))
        else:
            print("Invalid input, try again")





# def passwordReset():
#     print("\n______________\nForgot password>")
#     email = input("\nEnter email:")

#     try:
#         auth.send_password_reset_email(email)
#     except:
#         print("Error")


def interface():
    while (1):
        z = input("\n______________\nWelcome to BoxDrop\nEnter\n0 -> Exit\n1 -> Register a new account\n2 -> Log In\n")
        if z=="0":
            exit()
        elif z=="1":
            register()
        elif z=="2":
            login()
        # elif z=="3":
        #     passwordReset()
        else:
            print("Invalid input, try again")


interface()
