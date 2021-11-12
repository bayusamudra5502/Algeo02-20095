import socketio
from api.state import State as st
from lib.processing.imgprocess import build_decom_state
from threading import Thread

sio = socketio.AsyncServer(async_mode='asgi')
        
app = socketio.ASGIApp(sio)
state: st = None

@sio.event
async def connect(sid, _):
  print(f"INFO:\tUser dengan {sid} berhasil tersambung")
  await sio.emit("response", data=sid, to=sid)

@sio.event
async def subscribe(sid, _):
  if state.getState("subscribeSID") == None:
    state.setState("subscribeSID", sid)
    state.setState("isReady", False)
    await sio.emit("response", data={"success": True}, to=state.getState("subscribeSID"))
  else:
    await sio.emit("response", data={"success": False}, to=sid)

@sio.on("build-matrix")
async def buildMatrix(sid, _):
  if state.getState("subscribeSID") == sid and state.getState("imageLoaded"):
    B = Thread(target=build_decom_state, args=(state,), daemon=True)
    B.start()

    await sio.emit("response", data={"success": True}, to=sid)
  else:
    await sio.emit("response", data={"success": False}, to=sid)

@sio.event
async def unsubscribe(sid, _):
  if state.getState("subscribeSID") == sid:
    state.reset()
    await sio.emit("response", data={"success": True}, to=sid)
  else:
    await sio.emit("response", data={"success": False}, to=sid)

@sio.event
async def disconnect(sid):
  print(f"INFO:\tUser dengan {sid} berhasil disconnect")
  if state.getState("subscribeSID") == sid:
    state.reset()

def setState(State: st):
  global state
  state = State
  state.setState("ws", sio)

def getSocketApp():
  return app