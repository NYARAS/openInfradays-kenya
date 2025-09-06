from flask import Flask, render_template
from controllers.user_controller import user_bp
from models.base_model import Base, engine

app = Flask(__name__)
Base.metadata.create_all(bind=engine)
app.register_blueprint(user_bp, url_prefix="/users")


@app.route("/")
def hello_world():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
