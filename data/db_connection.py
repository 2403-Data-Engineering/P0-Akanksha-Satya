import mysql.connector




def get_connection():
    return mysql.connector.connect(
        host="revature-2403.cs1m8i0ouruo.us-east-1.rds.amazonaws.com",        
        user="admin",             
        password="revature",
        database="Akanksha_Satya_P0",
        port=3306    
    )