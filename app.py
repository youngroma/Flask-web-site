import os
from flask import Flask, request, redirect, url_for, render_template, flash, abort, session
from werkzeug.utils import secure_filename
from config import app, db, ALLOWED_EXTENSIONS
from models import Item
from uploads import allowed_file

@app.route('/create', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        title = request.form['title']
        price = request.form['price']
        is_active = request.form.get('isActive') == 'on'
        file = request.files['file']

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            photo_path = os.path.join('static/img/', filename)

            new_item = Item(title=title, price=price, isActive=is_active, photo=photo_path)
            db.session.add(new_item)
            db.session.commit()

            return redirect(url_for('index'))
    return render_template('create.html')


@app.route('/')
def index():
    data = Item.query.all()
    sort_by = request.args.get('sort_by')
    if sort_by == 'price':
        items = Item.query.order_by(Item.price).all()
    elif sort_by == 'title':
        items = Item.query.order_by(Item.title).all()
    # elif sort_by == 'date':
    #     items = Item.query.order_by(Item.date).all()
    else:
        items = Item.query.all()


    return render_template('index.html', data=items)

@app.route('/contact')
def about():
    return render_template('contact.html')

@app.route('/base')
def base():
    return render_template('base.html')

@app.route("/products/<int:id_post>")
def show_post(id_post):
    item = Item.query.get_or_404(id_post)
    return render_template('post.html', item=item)

@app.route('/add_to_cart/<int:item_id>', methods=['POST'])
def add_to_cart(item_id):
    item = Item.query.get_or_404(item_id)

    if 'cart' not in session:
        session['cart'] = []

    cart = session['cart']
    cart.append({'id': item.id, 'title': item.title, 'price': item.price, 'photo': item.photo})
    session['cart'] = cart

    return redirect(url_for('index'))

@app.route('/cart')
def cart():
    cart_items = session.get('cart', [])
    total_price = sum(item['price'] for item in cart_items)
    return render_template('cart.html', cart_items=cart_items, total_price=total_price)

@app.route('/remove_from_cart/<int:item_id>', methods=['POST'])
def remove_from_cart(item_id):
    cart = session.get('cart', [])
    cart = [item for item in cart if item['id'] != item_id]
    session['cart'] = cart
    return redirect(url_for('cart'))

@app.route('/checkout', methods=['POST'])
def checkout():

    session.pop('cart', None)
    return redirect(url_for('index'))



if __name__ == "__main__":
    app.run(debug=True)
