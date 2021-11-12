from typing import Optional
from starlette.responses import RedirectResponse, Response
from lib.converter.convert import *
from fastapi.datastructures import UploadFile
from fastapi.params import File, Form
from fastapi.responses import StreamingResponse
from fastapi import FastAPI, HTTPException
from api.state import *
from api.state import State
from lib.processing.imgprocess import compress_image_by_cache
from fastapi.middleware.cors import CORSMiddleware
from api.socket import setState, getSocketApp

import uvicorn

app = FastAPI()
state:State = None

origin = [
  "http://localhost:3000",
  "http://localhost:5502",
  "http://localhost",
  "https://compress.bayusamudra.my.id"
]

app.add_middleware(
  CORSMiddleware, 
  allow_origins=origin,
  allow_methods=["GET","POST"],
  allow_headers=["*"],
  allow_credentials=True
)

@app.get("/")
async def root_path():
  return {"status": "success"}

@app.get("/status")
async def ping():
  return {"status": "success", "isReady" : state.getState("isReady")}

@app.post("/upload")
async def upload(token:str = Form(...), file: UploadFile = File(...)):
  if file.content_type.lower() != "image/png" and \
      file.content_type.lower() != "image/jpg" and \
      file.content_type.lower() != "image/jpeg":
    print(file.content_type.lower())
    raise HTTPException(status_code=400, detail="Tipe data gambar tidak diizinkan")

  if token == state.getState("subscribeSID"):
    imageFile = file.file
    matrix = convertFileToArray(imageFile)

    
    state.setState("imageReady", False)
    state.setState("imageLoaded", True)
    state.setState("imageMatrix", matrix)
    state.setState("format", file.content_type.lower())

    filename = file.filename.split(".")

    state.setState("filename", ".".join(filename[:-1]))
    state.setState("extension",filename[-1])
    return {"success": True}
  else:
    raise HTTPException(status_code=403, detail="Anda tidak memiliki akses untuk upload")

@app.get("/compress/{level}/download/")
async def downloadCompressedImage(level: int, alpha: Optional[bool] = False):
  if not state.getState("imageReady"):
    raise HTTPException(status_code=404, detail="Gambar belum diproses")
  else:
    res, _ = await compress_image_by_cache(state, level, alpha=alpha)
    f = convertArrayToIO(res, state.getState("format"))

    filename = state.getState("filename") + "." + str(level) + "." + state.getState("extension")

    return Response(f.read(), 
      headers={"Content-Disposition": f'attachment; filename="{filename}"'}, 
      media_type="application/octet-stream")

@app.get("/compress/{level}/level/")
async def getLevel(level: int, alpha: Optional[bool] = False):
  _, level = await compress_image_by_cache(state, round(level, 3), alpha=alpha)

  return {"success": True, "compress": level}

@app.get("/compress/{level}")
async def compressImage(level: int, alpha: Optional[bool] = False):
  if not state.getState("imageReady"):
    raise HTTPException(status_code=404, detail="Gambar belum diproses")
  else:
    res,_ = await compress_image_by_cache(state, level, alpha=alpha)
    f = convertArrayToIO(res, state.getState("format"))

    return StreamingResponse(f, media_type=state.getState("format"))

def run_server_one(state_data: State, port=80):
  global state
  state =  state_data

  setState(state_data)
  socket = getSocketApp()

  app.mount("/ws", socket, "Socket")

  uvicorn.run("api.routes:app", host="0.0.0.0",port=port)
  
