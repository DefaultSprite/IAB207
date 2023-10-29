from server import create_app

# creates main
if __name__ == '__main__':
    app = create_app()
    app.run(debug = True)