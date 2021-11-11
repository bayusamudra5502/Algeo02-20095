import threading
import sys
from api.routes import run_server
from api.socket import run_ws
from api.state import State


def main():
  print("""\u001b[32m
 _____                             _____                                                    
|_   _|                           /  __ \                                                   
  | | _ __ ___   __ _  __ _  ___  | /  \/ ___  _ __ ___  _ __  _ __ ___  ___ ___  ___  _ __ 
  | || '_ ` _ \ / _` |/ _` |/ _ \ | |    / _ \| '_ ` _ \| '_ \| '__/ _ \/ __/ __|/ _ \| '__|
 _| || | | | | | (_| | (_| |  __/ | \__/\ (_) | | | | | | |_) | | |  __/\__ \__ \ (_) | |   
 \___/_| |_| |_|\__,_|\__, |\___|  \____/\___/|_| |_| |_| .__/|_|  \___||___/___/\___/|_|   
                       __/ |                            | |                                 
                      |___/                             |_|                                 
\u001b[0m""")

  print("Versi 1.0.0 / Backend", end="\n\n")

  print("--------")
  print()

  state = State()

  web_server = threading.Thread(target=run_server, args=(state,), daemon=True)
  web_server.start()

  ws_server = threading.Thread(target=run_ws, args=(state,), daemon=True)
  ws_server.start()

  try:
    web_server.join()
  except KeyboardInterrupt:
    print()
    print("Server dimatikan.")
    sys.exit()

if __name__ == "__main__":
  main()