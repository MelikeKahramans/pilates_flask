from app import create_app, mysql, login_manager, db   # create_app'tan db nesnesini de import ediyoruz

app, mysql, login_manager, db = create_app()

if __name__ == '__main__':
    app.run(debug=True)
