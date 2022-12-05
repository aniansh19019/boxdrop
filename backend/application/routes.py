from application import app
from flask import request

@app.route('/', methods = ['GET', 'POST'])
def index():
    if request.method == 'POST':

        return(str(request.headers))

    return 'okay'