from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#Database config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

database = SQLAlchemy(app)

#MODEL
class Todo(database.Model):
    id = database.Column(database.Integer,primary_key = True)
    title = database.Column(database.String(100))
    complete = database.Column(database.Boolean)

#url path or route
@app.route("/")
def home():
    return "Welcome to Flask"

@app.route("/todo")
def todoView():
    todos = Todo.query.all()
    return render_template("base.html", todos=todos)

@app.route("/add", methods = ['POST'])
def addTodo():
    title = request.form.get("title")
    newTodo = Todo(title=title,complete = False)
    database.session.add(newTodo)
    database.session.commit()
    return redirect(url_for("todoView"))

@app.route("/update/<int:__id>")
def updateTodo(__id):
    todo = Todo.query.filter_by(id=__id).first()
    todo.complete = not todo.complete
    database.session.commit()
    return redirect(url_for("todoView"))

@app.route("/delete/<int:__id>")
def deleteTodo(__id):
    todo = Todo.query.filter_by(id=__id).first()
    database.session.delete(todo)
    database.session.commit()
    return redirect(url_for("todoView"))

# @app.route("/edit/<int:__id>")
# def editTodo(__id):
#     todo = Todo.query.filter_by(id=__id).first()
#     if request.method ==  'POST':
#         todo.title = request.form['title']
#         try:
#             database.session.commit()
#             return render_template("editTodo.html", todo=todo)
#         except:
#             return "An error occured"

#     else:
#         return redirect("todoView")
    


if __name__ == "__main__":
    database.create_all() #for creating the database entities
    app.run(debug=True)