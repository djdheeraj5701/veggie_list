from flask import Flask, render_template, request, redirect, url_for
import sqlalchemy as db

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///veggie.sqlite'

column_headers=['item_id','name','categories','description','price_curr','price_mrp']

engine=db.create_engine(app.config['SQLALCHEMY_DATABASE_URI'],connect_args={"check_same_thread":False})
connection = engine.connect()
metadata = db.MetaData()
'''
    item_id | name | categories | description | price_curr | price_mrp
'''
table=db.Table('veggie', metadata,
                        db.Column(column_headers[0],db.Integer, primary_key=True),
                        db.Column(column_headers[1],db.String(50)),
                        db.Column(column_headers[2],db.String(50)),
                        db.Column(column_headers[3],db.String(50)),
                        db.Column(column_headers[4],db.Float),
                        db.Column(column_headers[5],db.Float)
                    )
metadata.create_all(engine)

class Product:
    ItemList = []

    def __init__(self, name, categories, description, images):
        self.name = name
        self.item_id = len(Product.ItemList)
        self.categories = categories
        self.description = description
        self.images = images
        self.dealers = dict()
        self.price = [0.0, 0.0]  # curr,mrp
        Product.ItemList.append(self)

    def editContent(self, i, new_val):
        contents = {'name': self.name, 'categories': self.categories, 'description': self.description,
                    'images': self.images, 'price': self.price}
        if i in contents.keys():
            contents[i] = new_val
            return True
        return False

@app.route('/')
def index():
    query = "SELECT * FROM veggie"
    result_proxy = connection.execute(query)
    products = result_proxy.fetchall()
    return render_template('index.html',products=products)


@app.route('/add', methods=['POST'])
def add():
    rf=request.form
    price=rf['price'].split()
    name, categories, description, price_curr, price_mrp=rf['name'],rf['categories'],rf['description'],float(price[0]),float(price[1])
    query='INSERT INTO veggie(name,categories,description,price_curr,price_mrp) VALUES (?,?,?,?,?)'
    connection.execute(query, (name,categories,description,price_curr,price_mrp))
    return redirect(url_for('index'))

@app.route('/delete/<item_id>')
def delete(item_id):
    query='DELETE FROM veggie WHERE item_id=?'
    connection.execute(query,item_id)
    return redirect(url_for('index'))

@app.route('/update/<item_id>',methods=["POST"])
def update(item_id):
    price_curr=float(request.form['price'])
    query='UPDATE veggie SET price_curr=? WHERE item_id=?'
    connection.execute(query,(price_curr,item_id))
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=False)
