from flask import Flask, render_template, request, session, redirect, url_for
from datetime import timedelta

app = Flask(__name__);

app.secret_key="abcde1234"
app.permanent_session_lifetime=timedelta(minutes=5) # 세션 만료 시간 5분 

products = [
    {"id":1,"name":"노트북","price":3500000},
    {"id":2,"name":"물티슈","price":3500},
    {"id":3,"name":"종이컵","price":350},
    {"id":4,"name":"볼펜","price":1500},
]



@app.route('/')
def product_list():
    return render_template("products.html",products=products);

@app.get('/add/<int:product_id>')
def add_product(product_id):
    product = next((p for p in products if p['id'] == product_id), None)
    if product is None:
        return "상품을 찾을 수 없습니다.", 404
    cart = session.get('cart', {})
    item = cart.get(product['name'], {'price': product['price'], 'qty': 0})
    item['qty'] += 1
    cart[product['name']] = item
    session.permanent = True
    session['cart'] = cart
    return redirect(url_for('cart_list'))


@app.get('/cart')
def cart_list():
    cart = session.get('cart', {})
    total = sum(item['price'] * item['qty'] for item in cart.values())
    return render_template('cart.html', cart=cart, total=total)


@app.get('/remove/<name>')
def remove_product(name):
    cart = session.get('cart', {})
    cart.pop(name, None)
    session['cart'] = cart
    return redirect(url_for('cart_list'))


@app.get('/clear')
def clear_cart():
    session.pop('cart', None)
    return redirect(url_for('cart_list'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
