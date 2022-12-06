
# Also build a cli to take user input
# The interface should have options for login, register, forgot password, logout, etc.
# The interface should also have the option of selecting the root directory for the user.

def user_email():
    '''
    Returns the email of the current user.
    '''
    pass


def is_logged_in():
    '''
    Checks if the user is logged in.
    Returns True if logged in, False otherwise.
    '''
    pass


def login(email, password):
    '''
    Logs in the user with the given email and password.
    '''
    pass

def forgot_password(email):
    '''
    Sends a password reset link to the given email.
    '''
    pass

def register(email, password):
    '''
    Registers a new user with the given email and password.
    '''
    pass

def logout():
    '''
    Logs out the current user.
    '''
    pass