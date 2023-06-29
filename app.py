# This is the file for housing the main dash application.
# This is where we define tthe various css items to fetch
# as well as the layout of our app

# package imports
from content import app

server = app.server

if __name__ == "__main__":
    #app.run_server(debug=True)
    app.run_server(host='127.0.0.1', port=8050, debug=True)
     
