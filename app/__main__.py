from app.server.app import app

if __name__ == '__main__':
    app.run(port=8080, debug=True) #TODO change back to 80 and remove debug
