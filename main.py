from database.db import init_db, close_db
from handler.tools import MCPTools
from agent import OMSAgent

DB_PATH = "database/oms.db"


def main():
    conn = init_db(DB_PATH)
    tools = MCPTools(conn)
    agent = OMSAgent(tools.db)

    print("OMS Agent started. Type commands:\n")

    while True:
        user_input = input(">> ")
        if user_input in {"exit", "quit"}:
            break

        try:
            response = agent.handle(user_input)
            print(response)
        except Exception as e:
            print({"status": "error", "message": str(e)})

    close_db(conn)


if __name__ == "__main__":
    main()

