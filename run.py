from app import create_app
from app.routes import routes

app = create_app()
app.register_blueprint(routes)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=81, debug=True)
