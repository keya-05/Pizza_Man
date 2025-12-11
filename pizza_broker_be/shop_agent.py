#runs on Port 8000 and waits for questions.

from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from shop_tools import check_price_logic
from fastapi.middleware.cors import CORSMiddleware
from shop_tools import get_menu_items

app=FastAPI(title="Pizza Shop Agent")

#CORS, so that FE can trust BE
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (good for development)
    allow_credentials=True,
    allow_methods=["POST"],  #if all -> *
    allow_headers=["*"],  # Allows all headers
)

#---- the brain -----
class ShopBrain:

    def process_order(self, order_text):
        print(f" ShopBrain processing: '{order_text}'")

        menu_items=get_menu_items()
        print(menu_items)

        for item in menu_items:
            print(item,order_text.lower())
            if item in order_text.lower():
                print(item)
                print("   ↳ Using tool: check_price")
                return check_price_logic(item)
        return "I didn't understand. Please ask about our menu items."

agent = ShopBrain()

#-----A2A communication -----
class AgentMessage(BaseModel):
    sender:str
    content:str


@app.post("/a2a/message")
async def receive_message(msg: AgentMessage):
    print(f"\n📞 A2A CALL from {msg.sender}")
    response_text = agent.process_order(msg.content)
    return {"sender": "ShopAgent", "content": response_text}

if __name__ == "__main__":
    print("🟢 Shop Agent is ONLINE on Port 8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)