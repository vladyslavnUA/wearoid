from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
import os

host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/sunglasses')
client = MongoClient(host=host)
db = client.get_default_database()
sunglasses = db.sunglasses


app = Flask(__name__)

# @app.route("/login")
# def login:
# 	auth = request.authorization
# 	return " "

@app.route("/")
def sunglasses_index():
	#this will show the type of pants we have
	return render_template("sunglasses_index.html", sunglasses=sunglasses.find())

@app.route("/sunglasses", methods=["POST"])
def sunglasses_submit():
	sunglass = {
		"sunglass_name": request.form.get("sunglass_name"),
		"description": request.form.get("description"),
		"price": request.form.get("price"),
        "brand": request.form.get("brand")
	}
	sunglass_id = sunglasses.insert_one(sunglass).inserted_id
	print(sunglass_id)
	return redirect(url_for("sunglasses_show", sunglass_id = sunglass_id))

@app.route("/sunglasses/<sunglass_id>")
def sunglasses_show(sunglass_id):
	sunglass = sunglasses.find_one({'_id' : ObjectId(sunglass_id)})
	return render_template("sunglasses_show.html", sunglass = sunglass)

@app.route("/sunglasses/new")
def sunglasses_new():
	return render_template("sunglasses_new.html", sunglass={}, title ="New Item")

@app.route("/sunglasses/<sunglass_id>/edit")
def sunglasses_edit(sunglass_id):
	sunglass = sunglasses.find_one({"_id" : ObjectId(sunglass_id)})
	return render_template("sunglasses_edit.html", sunglass = sunglass, title = "Edit Item")

@app.route("/sunglasses/<sunglass_id>", methods = ['POST'])
def sunglasses_update(sunglass_id):
	updated_sunglass = {
		"sunglass_name": request.form.get("sunglass_name"),
		"description": request.form.get("description"),
		"price": request.form.get("price"),
        "brand": request.form.get("brand")
	}

	sunglasses.update_one( {"_id" : ObjectId(sunglass_id)}, {"$set" : updated_sunglass})
	return redirect(url_for("sunglasses_show", sunglass_id = sunglass_id))

@app.route("/sunglasses/<sunglass_id>/delete", methods=["POST"])
def sunglasses_delete(sunglass_id):
	sunglasses.delete_one({"_id" : ObjectId(sunglass_id)})
	return redirect(url_for("sunglasses_index"))


if __name__ == "__main__":
	app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))
