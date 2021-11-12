import sys
from api.routes import run_server_one
from api.state import State

def main():
  print("""\u001b[32m
 _____                                                    
/  __ \                                                   
| /  \/ ___  _ __ ___  _ __  _ __ ___  ___ ___  ___  _ __ 
| |    / _ \| '_ ` _ \| '_ \| '__/ _ \/ __/ __|/ _ \| '__|
| \__/\ (_) | | | | | | |_) | | |  __/\__ \__ \ (_) | |   
 \____/\___/|_| |_| |_| .__/|_|  \___||___/___/\___/|_|   
                      | |                                 
                      |_|                                 
\u001b[0m""")

  print("Versi 1.0.0 / Backend", end="\n\n")

  print("--------")
  print()

  state = State()

  if len(sys.argv) > 1:
    run_server_one(state, int(sys.argv[1]))
  else:
    run_server_one(state)

if __name__ == "__main__":
  main()