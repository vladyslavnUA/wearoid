from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
import os

host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/Wearoid')
client = MongoClient(host=f'{host}?retryWrites=false') #mongo client
app = Flask(__name__)

db = client.get_default_database()
products = db.products
comments = db.comments

@app.route('/')
def products_index():
    #index products
    return render_template('products_index.html', products=products.find())

@app.route('/products/new')
def products_new():
    #create a new product
    return render_template('products_new.html')

@app.route('/products', methods=['post'])
def products_submit():
    #grab video IDs and make a list out of them
    # video_ids = request.form.get('video_ids').split()
    
    product = {
        'title': request.form.get('title'),
        'description': request.form.get('description'),
        'price': request.form.get('price'),
        'image': request.form.get('image')
    }
    product_id = products.insert_one(product).inserted_id
    return redirect(url_for('products_show', product_id=product_id))

@app.route('/products/<product_id>')
def products_show(product_id):
    #one product
    product = products.find_one({'_id': ObjectId(product_id)})
    product_comments = comments.find({'product_id': ObjectId(product_id)})
    return render_template('products_show.html', product=product, comments=product_comments)

@app.route('/products/<product_id>', methods=['post'])
def products_update(product_id):
    # videos_ids = request.form.get('videos_ids').split('/')
    # videos = video_url_creator(videos_ids)

    updated_product = {
        'title': request.form.get('title'),
        'description': request.form.get('description'),
        'price': request.form.get('price'),
        'image': request.form.get('image')
    }

    products.update_one(
        {'_id': ObjectId(product_id)},
        {'$set': updated_product})
    return redirect(url_for('products_show', product_id=product_id))

@app.route('/products/<product_id>/edit')
def products_edit(product_id):
    product = products.find_one({'_id': ObjectId(product_id)})
    return render_template('products_edit.html', product=product, title='Edit Product')

@app.route('/products/<product_id>/delete', methods=['post'])
def products_delete(products_id):
    products.delete_one({'_id': ObjectId(product_id)})
    return redirect(url_for('products_index'))

@app.route('/products/comments', methods=['post'])
def comments_new():
    comment = {
        'title': request.form.get('title'),
        'content': request.form.get('content'),
        'product_id': ObjectId(request.form.get('product_id')),
    }
    print(comment)
    comment_id = comments.insert_one(comment).inserted_id
    return redirect(url_for('products_show', product_id=request.form.get('product_id')))

@app.route('/products/comments/<comment_id>', methods=['post'])
def comments_delete(comment_id):
    comment = comments.find_one({'_id': ObjectId(comment_id)})
    comments.delete_one({'_id': ObjectId(comment_id)})
    return redirect(url_for('products_show', product_id=comment.get('product_id')))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))