from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
import mysql.connector
from mysql.connector import errorcode

config = {
    'host' : 'shoewizardsdb.mysql.database.azure.com',
    'user' : 'sqladmin',
    'password' : 'Triguna1956',
    'database' : 'shoewizardsdb',
    'client_flags' : [mysql.connector.ClientFlag.SSL],
    'ssl_ca' : './ssl/DigiCertGlobalRootG2.crt.pem'
}

try :
    conn = mysql.connector.connect(**config)
    print("Connection established")
except mysql.connector.Error as err :
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR :
        print("Something is wrong with the user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR :
        print("Database does not exist")
    else :
        print(err)
else :
    cursor = conn.cursor()
    
    app = FastAPI()

    @app.get('/customers')
    async def read_all_customers():
        query = ("SELECT * FROM customers")
        cursor.execute(query)
        result = cursor.fetchall()
        return result

    @app.get('/consultations')
    async def read_customer_consultations(customerid: int, shoeid: int):
        query = ("SELECT * FROM consultations WHERE customerid = %s AND shoeid = %s")
        cursor.execute(query, (customerid, shoeid))
        result = cursor.fetchall()
        if result :
            consultations = []
            for consultation in result:
                productid = consultation[3]
                query = ("SELECT * FROM products WHERE productid = %s")
                cursor.execute(query, (productid,))
                result = cursor.fetchall()
                if result :
                    consultations.append(result[0][1])
                else :
                    return "No matching products found."
            return "Based on your consultation, we recommend the following products: " + ", ".join(consultations)
        else :
            return "No matching consultations found."
    
    @app.get('/products')
    async def read_all_products():
        query = ("SELECT * FROM products")
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    
    @app.get('/products/{productid}')
    async def read_product(productid: int):
        query = ("SELECT * FROM products WHERE productid = %s")
        cursor.execute(query, (productid,))
        result = cursor.fetchall()
        if result :
            return result
        else :
            return "Product ID "+str(productid)+" does not exist."
    
    @app.get('/shoes')
    async def read_all_shoes():
        query = ("SELECT * FROM shoes")
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    
    @app.post('/customers')
    async def add_customer(firstname: str, lastname: str, phonenumber: str, address: str, email: str):
        query = ("SELECT * FROM customers")
        cursor.execute(query)
        result = cursor.fetchall()
        if not result :
            customerid = 1
        else :
            query = ("SELECT MAX(customerid) FROM customers")
            cursor.execute(query)
            result = cursor.fetchall()
            customerid = result[0][0] + 1

        query = ("INSERT INTO customers (customerid, firstname, lastname, phonenumber, address, email) VALUES (%s, %s, %s, %s, %s, %s)")
        cursor.execute(query, (customerid, firstname, lastname, phonenumber, address, email))
        conn.commit()
        return "Customer ID "+str(customerid)+" added."

    @app.post('/consultations')
    async def add_consultation(customerid: int, shoeid: int):
        global consultationid

        query = ("SELECT * FROM consultations")
        cursor.execute(query)
        result = cursor.fetchall()
        if not result :
            consultationid = 1

        query = ("SELECT * FROM consultations WHERE customerid = %s AND shoeid = %s")
        cursor.execute(query, (customerid, shoeid))
        result = cursor.fetchall()
        if result :
            return "Consultation for Customer ID "+str(customerid)+" and Shoe ID "+str(shoeid)+" exists."
        else :
            query = ("SELECT * FROM customers WHERE customerid = %s")
            cursor.execute(query, (customerid,))
            result = cursor.fetchall()
            if not result :
                return "Customer ID "+str(customerid)+" does not exist."
            else :
                query = ("SELECT * FROM shoes WHERE shoeid = %s")
                cursor.execute(query, (shoeid,))
                result = cursor.fetchall()
                if not result :
                    return "Shoe ID "+str(shoeid)+" does not exist."
                else :
                    shoe_type = result[0][1]
                    query = ("SELECT * FROM products WHERE producttype = %s")
                    cursor.execute(query, (shoe_type,))
                    result = cursor.fetchall()
                    if not result :
                        return "No matching products found for the shoe type."
                    else :
                        for product in result:
                            productid = product[0]
                            consultdate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            query = ("INSERT INTO consultations (consultationid, customerid, shoeid, productid, consultdate) VALUES (%s, %s, %s, %s, %s)")
                            cursor.execute(query, (consultationid, customerid, shoeid, productid, consultdate))
                            conn.commit()
                            consultationid += 1
                        return "Consultation for Customer ID "+str(customerid)+" and Shoe ID "+str(shoeid)+" added."

    @app.post('/products')
    async def add_product(productname: str, productdescription: str, price: float, stock: int, producttype: str):
        query = ("SELECT * FROM products")
        cursor.execute(query)
        result = cursor.fetchall()
        if not result :
            productid = 1
        else :
            query = ("SELECT MAX(productid) FROM products")
            cursor.execute(query)
            result = cursor.fetchall()
            productid = result[0][0] + 1

        query = ("INSERT INTO products (productid, productname, productdescription, price, stock, producttype) VALUES (%s, %s, %s, %s, %s, %s)")
        cursor.execute(query, (productid, productname, productdescription, price, stock, producttype))
        conn.commit()
        return "Product ID "+str(productid)+" added."
        
    @app.post('/shoes')
    async def add_shoe(shoetype: str, shoesize: int, shoecolor: str, shoebrand: str, initialcondition: str):
        query = ("SELECT * FROM shoes")
        cursor.execute(query)
        result = cursor.fetchall()
        if not result :
            shoeid = 1
        else :
            query = ("SELECT MAX(shoeid) FROM shoes")
            cursor.execute(query)
            result = cursor.fetchall()
            shoeid = result[0][0] + 1

        query = ("INSERT INTO shoes (shoeid, shoetype, shoesize, shoecolor, shoebrand, initialcondition) VALUES (%s, %s, %s, %s, %s, %s)")
        cursor.execute(query, (shoeid, shoetype, shoesize, shoecolor, shoebrand, initialcondition))
        conn.commit()
        return "Shoe ID "+str(shoeid)+" added."
        
    @app.put('/products')
    async def update_product(productid: int, productname: str, productdescription: str, price: float, stock: int, producttype: str):
        query = ("SELECT * FROM products WHERE productid = %s")
        cursor.execute(query, (productid,))
        result = cursor.fetchall()
        if result :
            query = ("UPDATE products SET productname = %s, productdescription = %s, price = %s, stock = %s, producttype = %s WHERE productid = %s")
            cursor.execute(query, (productname, productdescription, price, stock, producttype, productid))
            conn.commit()
            return "Product ID "+str(productid)+" updated."
        else :
            return "Product ID "+str(productid)+" does not exist."
    
    @app.delete('/products/{productid}')
    async def delete_product(productid: int):
        query = ("SELECT * FROM products WHERE productid = %s")
        cursor.execute(query, (productid,))
        result = cursor.fetchall()
        if result :
            query = ("DELETE FROM products WHERE productid = %s")
            cursor.execute(query, (productid,))
            conn.commit()
            return "Product ID "+str(productid)+" deleted."
        else :
            return "Product ID "+str(productid)+" does not exist."
        
