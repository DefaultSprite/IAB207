from server import create_app

# Program Entrypoint
if __name__ == '__main__':
    app = create_app()
    app.run(debug = True)