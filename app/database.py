import mysql.connector
from mysql.connector import errorcode

config = {
    'host' : 'shoewizardsdb.mysql.database.azure.com',
    'user' : 'sqladmin',
    'password' : '**********',
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