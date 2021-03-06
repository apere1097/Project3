from flask import Flask, render_template, request, url_for
from flask_pymongo import PyMongo
from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, SelectField,DateField

app = Flask(__name__)
app.config["SECRET_KEY"] = "holy_this_one_super_secret_key"
app.config["MONGO_URI"] = "mongodb+srv://testuser:testuser1@cluster0.pyivg.mongodb.net/db?retryWrites=true&w=majority"
mongo = PyMongo(app)


class Expenses(FlaskForm):

    description = StringField('description')

    category = SelectField('category', choices=[('', ''),
                                                ('clothing', 'Clothing'),
                                                ('college', 'College'),
                                                ('electricity', 'Electricity'),
                                                ('gas', 'Gas'),
                                                ('groceries', 'Groceries'),
                                                ('internet', 'Internet'),
                                                ('paper', 'Paper'),
                                                ('printer_ink', 'Printer ink')])

    cost = DecimalField('cost')

    date = DateField('date', format='%m-%d-%Y')


def get_total_expenses(category):

    total_expense = 0

    cat_expenses = mongo.db.expenses.find({"category": category})

    for i in cat_expenses:
        total_expense += float(i["cost"])

    return total_expense


@app.route('/')
def index():

    my_expenses = mongo.db.expenses.find()

    total_cost = 0

    for i in my_expenses:
        total_cost += float(i["cost"])

    expensesByCategory = [
        ("clothing", get_total_expenses("clothing")),
        ("college", get_total_expenses("college")),
        ("electricity", get_total_expenses("electricity")),
        ("gas", get_total_expenses("gas")),
        ("groceries", get_total_expenses("groceries")),
        ("internet", get_total_expenses("internet")),
        ("paper", get_total_expenses("paper")),
        ("printer ink", get_total_expenses("printer_ink"))]

    return render_template("index.html", expenses=total_cost, expensesByCategory=expensesByCategory)


@app.route('/addExpenses',methods=["GET","POST"])
def addExpenses():

    expensesForm = Expenses(request.form)

    if request.method == "POST":

        description = request.form["description"]
        category = request.form["category"]
        cost = request.form["cost"]
        date = request.form["date"]

        add_expense = [{"description": description,
                        "category": category,
                        "cost": cost,
                        "date": date}]

        mongo.db.expenses.insert_one(add_expense[0])

        return render_template("expenseAdded.html")

    return render_template("addExpenses.html", form=expensesForm)


app.run()
