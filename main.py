from flask import Flask,jsonify, request


# url http://127.0.0.1:5000/products

class Product:
    def __init__(self, product_id, name, price, stock):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.stock = stock


products = [
    Product(product_id=201, name="DELL", price=42000, stock=20),
    Product(product_id=202, name="HP", price=34000, stock=13),
    Product(product_id=203, name="Lenovo Touch", price=28000, stock=8),
    Product(product_id=204, name="Lenovo", price=23000, stock=5),
    Product(product_id=205, name="Asus", price=20000, stock=20)
]

def productToJson(product):
    return {
        "id": product.product_id,
        "name": product.name,
        "price": product.price,
        "stock": product.stock
    }


# create an app
app = Flask("API APP")


@app.route('/products',methods=['GET'])
def getALLProducts():
    print("called getALLProducts")

    productlist = []
    for product in products:
        productlist.append(productToJson(product))

    return jsonify({"products":productlist})


@app.route('/products/<int:productid>',methods=['GET'])
def getProductById(productid):
    print("called getProductById")

    for product in products:
        if product.product_id == productid:
            return jsonify({"product" : productToJson(product)})

    return jsonify({"Error":"Product not found"}),404

@app.route('/products/search', methods=['GET'])
def search():
    print("called Search")
    keyword = request.args.get("keyword", "").lower()
    print("Keyword:", keyword)

    matched_products = []
    for product in products:
        if keyword in str(product.product_id).lower() or keyword in product.name.lower():
            matched_products.append(productToJson(product))

    return jsonify({"results": matched_products})


    if len(productList) > 0:
        return jsonify({"results": productList})
    else:
        return jsonify({"Error": "Product not found"}),404

cart = []  # Define cart at the top-level if not already
orders = []

@app.route('/cart/add', methods=['POST'])
def addTocart():
    print("called addToCart")
    data = request.get_json()
    product_id = data.get("product_id")
    quantity = data.get("qnty")

    print("product_id:", product_id)
    print("quantity:", quantity)

    product = None
    for p in products:
        if p.product_id == product_id:
            product = p

    if product and product.stock >= quantity:
        product.stock -= quantity
        cart.append({"product": productToJson(product), "quantity": quantity})
        return jsonify({"message": "Product added to cart successfully", "cart": cart})
    elif product:
        return jsonify({"error": "Product quantity insufficient"}), 400

    return jsonify({"error": "Product not found"}), 404

@app.route('/cart/remove', methods=['POST'])
def removeFromCart():
    print("called removeFromCart")
    data = request.get_json()
    product_id = data.get("product_id")
    quantity = data.get("qnty")

    for c in cart:
        if c["product"]["id"] == product_id:
            cart.remove(c)
            return jsonify({"message": "Product removed from cart successfully", "cart": cart})

    return jsonify({"error": "Product not found in the cart"}), 404

@app.route('/cart/order', methods=['POST'])
def orderFromCart():
    if len(cart) <= 0:
        return jsonify({"error": "Cart is empty"}), 404

    order = cart.copy()
    orders.append(order)
    cart.clear()
    return jsonify({"message": "Order placed successfully", "order": orders})

@app.route('/orders', methods=['GET'])
def getALLOrders():
    return jsonify({"orders": orders})



# app run
if __name__ == '__main__':
    app.run(debug=True)