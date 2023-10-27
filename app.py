from flask import Flask
import os
from flask import request, redirect, url_for
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.utils import secure_filename


app = Flask(__name__)
UPLOAD_FOLDER = 'static/product/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db = SQLAlchemy(app) 
#model--------
class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    desc = db.Column(db.String)
    image = db.Column(db.String)  # Path to the image file
    instock = db.Column(db.Boolean, default=True)
    price = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, onupdate=datetime.now)
    def __str__(self):
        return f"{self.name}"

#Routes*********************************************************************
#index-------------------
@app.route("/",endpoint='product.list')
def product_list():
    products = Product.query.all()
    return render_template('product/index.html', products=products)
#details----------------------
@app.route('/product/<int:id>', endpoint='product.details')
def product_details(id):
    product = Product.query.get(id)
    
    return render_template('product/details.html',product=product)
#create---------------------------
@app.route('/product/create', methods=['GET', 'POST'], endpoint='product.create')
def product_create():
    if request.method == 'POST':
       
        name = request.form.get('name')
        desc = request.form.get('desc')
        price = request.form.get('price')
        
        if 'image' in request.files:
            image_file = request.files['image']
            if image_file.filename != '':
                filename = secure_filename(image_file.filename)
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                image_file.save(image_path)
            else:
                image_path = None
        else:
            image_path = None
       
        product = Product(
            name=name,
            desc=desc,
            image=image_path,
            price=price
        )
        db.session.add(product)
        db.session.commit()

        return redirect(url_for('product.list'))

    return render_template('product/create.html')
#-delete-------------------------
@app.route('/product/delete/<int:id>', endpoint='product.delete')
def product_delete(id):
    product = Product.query.get(id)

    if product:       
        db.session.delete(product)
        db.session.commit()

    return redirect(url_for('product.list'))
#Edit----------------------------------------
@app.route('/product/edit/<int:id>', methods=['GET', 'POST'], endpoint='product.edit')
def product_edit(id):
    product = Product.query.get_or_404(id)

    if request.method == 'POST':
        product.name = request.form.get('name')
        product.desc = request.form.get('desc')
        product.price = float(request.form.get('price'))
        product.instock = True if request.form.get('instock') else False

        if 'image' in request.files:
            image_file = request.files['image']
            if image_file.filename != '':
                filename = secure_filename(image_file.filename)
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                image_file.save(image_path)
                product.image = image_path

        db.session.commit()

        return redirect(url_for('product.list'))

    return render_template('product/edit.html', product=product)



