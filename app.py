from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"


@app.route("/", methods=["GET", "POST"])
def hello_world():
    if request.method == "POST":
        title = request.form["title"]
        desc = request.form["description"]
        todo = Todo(title=title, description=desc)
        db.session.add(todo)
        db.session.commit()
    allTodo = Todo.query.all()
    return render_template("index.html", allTodo=allTodo)


@app.route("/show")
def show():
    allTodo = Todo.query.all()
    return "banchod"


@app.route("/update/<int:sno>", methods=["GET", "POST"])
def update(sno):
    if request.method == "POST":
        title = request.form["title"]
        desc = request.form["description"]
        allTodo = Todo.query.filter_by(sno=sno).first()
        allTodo.title = title
        allTodo.description = desc
        db.session.add(allTodo)
        db.session.commit()
        return redirect("/")
    allTodo = Todo.query.filter_by(sno=sno).first()
    return render_template("update.html", todo=allTodo)


@app.route("/delete/<int:sno>")
def delete(sno):
    allTodo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(allTodo)
    db.session.commit()
    return redirect("/")


if __name__ == "__main__":
    with app.app_context():        
        db.create_all()  
        app.run(debug=True)
