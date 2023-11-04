from fastapi import FastAPI, HTTPException
import json
from pydantic import BaseModel
from datetime import datetime

class customers(BaseModel):
	customerid: int
	firstname: str
	lastname: str
	number: str
	address: str
	email: str

class orders(BaseModel):
	orderid: int
	customerid: int
	shoeid: int
	productid: int
	orderdate: datetime

class products(BaseModel):
	productid: int
	productname: str
	productdescription: str
	type: str
	price: float
	stock: int

class shoes(BaseModel):
	shoeid: int
	shoetype: str
	shoesize: int
	shoecolor: str
	shoebrand: str
	initialcondition: str

json_filename="shoewizard.json"

with open(json_filename,"r") as read_file:
	data = json.load(read_file)

app = FastAPI()

@app.get('/customers')
async def read_all_customers():
	return data['customers']

@app.get('/orders')
async def read_all_orders(customerid: int, shoeid: int):
	matching_orders = []
	for order in data['orders']:
		if order['customerid'] == customerid and order['shoeid'] == shoeid:
			matching_orders.append(order)

	if not matching_orders:
		raise HTTPException(status_code=404, detail="No matching orders found")

	matching_product_ids = [order['productid'] for order in matching_orders]

	recommendations = []
	for product in data['products']:
		if product['productid'] in matching_product_ids:
			recommendations.append(product['productname'])

	if not recommendations:
		raise HTTPException(status_code=404, detail="No recommendations found")

	recommendation_sentence = "Based on your orders, we recommend the following products: " + ", ".join(recommendations)

	return recommendation_sentence

@app.get('/products')
async def read_all_products():
	return data['products']

@app.get('/shoes')
async def read_all_shoes():
	return data['shoes']

@app.post('/customers')
async def add_customer(customerid: int, firstname: str, lastname: str, number: str, address: str, email: str):
	item_found = False
	for customer_item in data['customers']:
		if customer_item['customerid'] == customerid:
			item_found = True
			return "Customer ID "+str(customerid)+" exists."
	
	if not item_found:
		new_customer = {
			"customerid": customerid,
			"firstname": firstname,
			"lastname": lastname,
			"number": number,
			"address": address,
			"email": email
		}

		data['customers'].append(new_customer)

		with open("shoewizard.json","w") as write_file:
			json.dump(data, write_file, indent=4)

		return "Customer with ID " + str(customerid) + " added successfully."
	
	raise HTTPException(
		status_code=404, detail=f'item not found'
	)

@app.post('/products')
async def add_product(productid: int, productname: str, productdescription: str, type: str, price: float, stock: int):
	item_found = False
	for product_item in data['products']:
		if product_item['productid'] == productid:
			item_found = True
			return "Product ID "+str(productid)+" exists."
	
	if not item_found:
		new_product = {
			"customerid": productid,
			"productname": productname,
			"productdescription": productdescription,
			"type": type,
			"price": price,
			"stock": stock
		}

		data['products'].append(new_product)

		with open("shoewizard.json","w") as write_file:
			json.dump(data, write_file, indent=4)

		return "Product with ID " + str(productid) + " added successfully."
	
	raise HTTPException(
		status_code=404, detail=f'item not found'
	)

@app.post('/shoes')
async def add_shoe(shoeid: int, shoetype: str, shoesize: int, shoecolor: str, shoebrand: str, initialcondition: str):
	item_found = False
	for shoe_item in data['shoes']:
		if shoe_item['productid'] == shoeid:
			item_found = True
			return "Shoe ID "+str(shoeid)+" exists."
	
	if not item_found:
		new_shoe = {
			"shoeid": shoeid,
			"shoetype": shoetype,
			"shoesize": shoesize,
			"shoecolor": shoecolor,
			"shoebrand": shoebrand,
			"initialcondition": initialcondition
		}

		data['shoes'].append(new_shoe)

		with open("shoewizard.json","w") as write_file:
			json.dump(data, write_file, indent=4)

		return "Shoe with ID " + str(shoeid) + " added successfully."
	
	raise HTTPException(
		status_code=404, detail=f'item not found'
	)

@app.put('/products')
async def update_product(productid: int, productname: str, productdescription: str, type: str, price: float, stock: int):
	for product_item in data['products']:
		if product_item['productid'] == productid:
            # Update the customer's information
			product_item['productname'] = productname
			product_item['productdescription'] = productdescription
			product_item['type'] = type
			product_item['price'] = price
			product_item['stock'] = stock

			with open("shoewizard.json","w") as write_file:
				json.dump(data, write_file, indent=4)
			return "Product with ID " + str(productid) + " updated successfully."
	
	return "Product ID not found."

	raise HTTPException(status_code=404, detail="Customer not found")

@app.delete('/products/{productid}')
async def delete_product(productid: int):
	for product_item in data['products']:
		if product_item['productid'] == productid:
			data['products'].remove(product_item)

			with open("shoewizard.json","w") as write_file:
				json.dump(data, write_file, indent=4)
			return "Product with ID " + str(productid) + " deleted successfully."

	return "Product ID not found."

	raise HTTPException(
	status_code=404, detail=f'item not found'
	)



@app.post('/orders')
async def add_order(customerid: int, shoeid: int):
	global next_orderid

	if (len(data['orders']) == 0):
		next_orderid = 1

	customer_shoe = None
	for shoe_item in data['shoes']:
		if shoe_item['shoeid'] == shoeid:
			customer_shoe = shoe_item
			break
	
	if customer_shoe is None:
		raise HTTPException(status_code=404, detail="Shoe not found")
	
	matching_products = []
	for product_item in data['products']:
		if product_item['producttype'] == customer_shoe['shoetype']:
			matching_products.append(product_item)

	if not matching_products:
		raise HTTPException(status_code=404, detail="No matching products found for the shoe type")
	
	for product_item in matching_products:
		productid = product_item['productid']

		orderid = next_orderid

		orderdate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

		new_order = {
			"orderid": orderid,
			"customerid": customerid,
			"shoeid": shoeid,
			"productid": productid,
			"orderdate": orderdate
		}

		data['orders'].append(new_order)

		with open("shoewizard.json","w") as write_file:
			json.dump(data, write_file, indent=4)
		
		next_orderid += 1
	
	return "Order recommendation created."