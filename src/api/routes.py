import uvicorn
from fastapi import FastAPI
from api.state import *
from api.state import State

app = FastAPI()
state:State = None

@app.get("/")
def root_path():
  return {"status": "success"}

@app.get("/status")
def ping():
  return {"status": "success", "isReady" : state.getState("isReady")}

def run_server(state_data: State):
  global state
  state = state_data

  uvicorn.run(app, port=5502)
