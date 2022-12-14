from flask import Flask
app = Flask(__name__)
app.secret_key = "is it a secret tho"
DATABASE = "recipes"