import socketio
import uvicorn
from api.state import State as st

sio = socketio.AsyncServer(async_mode='asgi')
app = socketio.ASGIApp(sio)
state: st = None

@sio.event
async def connect(sid, _):
  print(f"INFO:\tUser dengan {sid} berhasil tersambung")
  await sio.emit("response", data=sid, to=sid)

@sio.event
async def subscribe(sid, _):
  if state.getState("subscribeSID") != None:
    state.setState("subscribeSID", sid)
    await sio.emit("response", data={"success": True}, to=state.getState("subscribeSID"))
  else:
    await sio.emit("response", data={"success": False}, to=sid)

@sio.on("build-matrix")
async def buildMatrix(sid, _):
  pass

@sio.event
async def unsubscribe(sid, _):
  state.setState("subscribeSID", None)
  await sio.emit("response", data={"success": True}, to=sid)

@sio.event
async def disconnect(sid):
  print(f"INFO:\tUser dengan {sid} berhasil disconnect")

def run_ws(State:st):
  global state
  state = State

  state.setState("ws", sio)

  uvicorn.run(app, port=5503)