#sends the question and pays.

import httpx
import asyncio
import json
import time

#-----A2A wallet -simuleted -----

def create_intent_mandate(item,amount):
    return {
        "protocol":"AP2-Simulated",
        "type":"Intentmandate",
        "authorized_for":item,
        "amount":amount,
        "timetamp":time.time(),
        "status":"signed"
    }

#----workflow------

async def run_client():
    print("🤖 Hungry Agent: Started.")
    user_request="I want Margherita pizza"

    #1, connect to the shop
    shop_url="http://localhost:8000/a2a/message"
    print("📡 Connecting to Shop Agent...")

    async with httpx.AsyncClient() as client:
        try:
            #2. Send Message
            response=await client.post(shop_url, json={
                "sender": "HungryAgent",
                "content": user_request
            })

            shop_reply=response.json()['content']
            print(f"📨 Shop Replied: '{shop_reply}'")

            #3,. pay if price is good
            if "₹12" in shop_reply:
                print("\n✅ Price confirmed. Authorizing Payment...")
                mandate = create_intent_mandate("Margherita", 12.00) 
                print(f"💳 AP2 MANDATE:\n{json.dumps(mandate, indent=2)}")

        except Exception as e:
            print(f" Error :{e}")

if __name__ == "__main__":
    asyncio.run(run_client())