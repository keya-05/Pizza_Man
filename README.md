# 🍕 Pizza Man - AI-Powered Pizza Agent

**Pizza Man** is a full-stack AI agent application designed to handle customer enquiries for a pizza shop. Unlike standard ordering forms, it uses an intelligent agent architecture to understand user intent ("What is the price of...") and dynamically fetches real-time data from a MySQL database.


## 🏗️ Architecture & Workflow

1.  **Frontend (React):** Captures user natural language (e.g., "Price of Pepperoni?").
2.  **API Layer (FastAPI):** Receives the message via a POST request.
3.  **The Brain (Agent):**  Dynamically fetches the current menu from the Database to understand valid items and detects intent (e.g., specific pizza inquiry).
4.  **Tools Layer:** Connects to MySQL to execute specific queries (Price check).
5.  **Database (MySQL):** Stores the source-of-truth for the menu and prices.

```mermaid
graph LR
    A[User/React Frontend<br/>Hungry_Agent] -- "POST /a2a/message" --> B[FastAPI Backend]
    B --> C{Agent Brain<br/>MCP Host}

    %% Subgraph for MCP Tooling
    subgraph MCP ["MCP Layer (shop_tools.py)"]
        direction TB
        T1[Tool: get_menu_items]
        T2[Tool: check_price]
        D[(MySQL DB)]
        
        T1 -- "2. SELECT pizza_name..." --> D
        T2 -- "6. SELECT price..." --> D
    end

    %% Agent calls the tools, not the DB directly
    C -- 1. Fetch Context --> T1
    C -- 5. Intent Match --> T2

    %% Data flows back
    D -- 3. Result --> T1
    D -- 7. Result --> T2
    T2 -- "8. ₹ Price" --> C
    T1 -- "4. ['Margherita', ...]" --> C

    C -- Final Response --> B
    B -- JSON Response --> A

    %% Style
    style MCP stroke-dasharray: 5 5, stroke:#666, rounded:true
```

## Install dependencies:
```pip install fastapi uvicorn mysql-connector-python python-dotenv```

## Create .env file:
```
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password_here
DB_NAME=pizzashop
```

## Frontend Configuration: 
```
npm install
# Ensure you are in the frontend directory
npm start
# OR if using Vite
npm run dev
```

## Backend Configuration: 
```
# Ensure you are in the backend directory
python shop_agent.py
# Output: 🟢 Shop Agent is ONLINE on Port 8000

```
