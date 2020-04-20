from flask import Flask, render_template, redirect, render_template_string
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DecimalField
from wtforms.validators import InputRequired, Length
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import webbrowser

app = Flask(__name__)
app.config['SECRET_KEY'] = 'AmazonSecret'

#SQLAlchemy Database Model
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///items.sqlite3'
db = SQLAlchemy(app)

class Item(db.Model):
    itemcode = db.Column(db.Integer, primary_key=True, autoincrement=True)
    itemname = db.Column(db.String(100))
    itemqty = db.Column(db.Integer)
    itemprice = db.Column(db.Float)
    amt = db.Column(db.Float)
    date_created = db.Column(db.DateTime, default=datetime.now())

from app import db
db.create_all()

#Forms WTForms
class AddItemForm(FlaskForm):
    itemname = StringField('itemname', validators=[InputRequired()])
    itemqty = IntegerField('itemqty', validators=[InputRequired()])
    itemprice = DecimalField('itemprice', places=2, validators=[InputRequired()])
    
#HTML
inventoryhtml = """<!doctype html>
    <html>
    <head>
    <style>
        h1 {text-align: center; margin-top:20px;}
        h3 {text-align: center; margin-top:20px;}
        h4 {text-align: center; margin-top:20px;}
        table {text-align: center; margin-top:20px;}
        input {text-align: center; margin-top:20px;}</style>
    </head>
    <body>
    <h1><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/a/a9/Amazon_logo.svg/320px-Amazon_logo.svg.png" style="width:160px;height:48px"></h1>
    <h4><a href= {{ url_for('AddItem') }}>Add item</a></h4>
    <h3>Item successfully added to inventory</h3>
        <table style="width:100%" border="1">
            <th>Item Code</th>
            <th>Item Name</th>
            <th>Quantity</th>
            <th>Price</th>
            <th>Amount</th>
            <th>Date Added</th>
            
            {%for allitems in query%}
            <tr>
            <td>
                {{allitems.itemcode}}
            </td>
            <td>
                {{allitems.itemname}}
            </td>
            <td style="text-align: right;">
                {{allitems.itemqty}}
            </td>
            <td style="text-align: right;">
                {{allitems.itemprice}}
            </td>
            <td style="text-align: right;">
                {{allitems.amt}}
            </td>
            <td>
                {{allitems.date_created}}
            </td>
            </tr>
            {%endfor%}
        </table>
    </form>
    </body>
    </html>
    """

homehtml = """<!doctype html>
    <html>
    <head>
    <style>
        h1 {text-align: center; margin-top:20px;}
        h3 {text-align: center; margin-top:20px;}
        h4 {text-align: center; margin-top:20px;}
        form {text-align: left; margin-top:20px; margin-left:500px}
        input {text-align: left; margin-top:20px; margin-left:50px}
    </style>
    </head>
    <body>
        <h1><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/a/a9/Amazon_logo.svg/320px-Amazon_logo.svg.png" style="width:160px;height:48px"></h1>
    <h3>Add item to Amazon Warehouse</h3>
    <form method="POST" action="{{ url_for('AddItem') }}">
        {{ form.csrf_token }}
        <label for="itemname">Item Name:</label>
        <input type="text" id="itemname" name="itemname" required
            size="10"> <br>
        <label for="itemqty">Quantity:</label>
        <input type="number" id="itemqty" name="itemqty" required
            min=0 size="10"> <br>
        <label for="itemprice">Price:</label>
        <input type="number" id="itemprice" name="itemprice" required
            min=0 size="10"> <br>
        <input type="submit" value="Submit">
        <input type="reset" value="Reset"> <br>
        <h4><a href= {{ url_for('Inventory') }}>View Inventory</a></h4>
    </form>
    </body>
    </html>
    """

#Routes
@app.route('/inventory', methods=['GET', 'POST'])
def Inventory():
    #return render_template('inventory.html', query=Item.query.all())
    return render_template_string(inventoryhtml, query=Item.query.all())

@app.route('/home', methods=['GET', 'POST'])
def AddItem():
    new_form = AddItemForm()
    if new_form.validate_on_submit():
        new_item = Item(itemname=new_form.itemname.data, itemqty=new_form.itemqty.data, itemprice=new_form.itemprice.data, amt=(new_form.itemqty.data)*(new_form.itemprice.data))
        db.session.add(new_item)
        db.session.commit()
        return redirect('inventory')
    return render_template_string(homehtml, form=new_form)

if __name__ == '__main__':
    webbrowser.open_new_tab('http://127.0.0.1:5000/home')
    app.run(debug=True)