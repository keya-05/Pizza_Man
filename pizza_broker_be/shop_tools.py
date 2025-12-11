from fastmcp import FastMCP
import mysql.connector
from dotenv import load_dotenv
import os

# 1. Load the environment variables from .env file
load_dotenv()

# Define the server name
mcp = FastMCP("PizzaShopTools") 

# MySQL Configuration
db_config = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME")
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

def get_menu_items():
    conn= None
    cur=None
    try: 
        conn=get_db_connection()
        cur=conn.cursor()
        cur.execute("SELECT pizza_name FROM menu")
        results=cur.fetchall()

        return [item[0].lower() for item in results] 
    except Exception as e:
        print(f"Error fetching items: {e}")
        return []
    finally:
        if cur: cur.close()
        if conn: conn.close()

def check_price_logic(pizza_name: str) -> str:
    conn = None
    cur = None
    try:
        conn = get_db_connection()
        cur = conn.cursor() # Fixed typo

        
        query = "SELECT price FROM menu WHERE pizza_name = %s" 
        
        # Fixed: Added comma to make it a tuple
        cur.execute(query, (pizza_name.lower(), ))
        
        # Fixed: Must fetch the result after executing
        result = cur.fetchone() 

        if result: 
            # result is a tuple like (12.00,), so we grab index [0]
            return f"The price of {pizza_name} is ₹{result[0]}."
        else:
            return f"{pizza_name} is not on the menu."

    except Exception as e:
        print(f"Error connecting to database: {e}")
        return "System Error: Database unavailable."

    finally:
        if cur: cur.close()
        if conn: conn.close()
    
    
#the tool function
@mcp.tool() #decorate the function as a tool-decorator
def check_price(pizza_name:str)->str:
    return check_price_logic(pizza_name) #calling the logic function not directly coz the the 
                                         #@mcp.tool makes it an object instead of a function

if __name__ == "__main__":
    mcp.run()