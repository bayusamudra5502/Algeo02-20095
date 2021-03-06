from typing import Optional
from starlette.requests import Request
from starlette.responses import Response
from lib.converter.convert import *
from fastapi.datastructures import UploadFile
from fastapi.params import File, Form
from fastapi.responses import StreamingResponse
from fastapi import FastAPI, HTTPException
from api.socket import build_socket
from api.state import State
from lib.processing.imgprocess import compress_image_by_cache
from fastapi.middleware.cors import CORSMiddleware

import uvicorn

def build_api(state):
  app = FastAPI()

  origin = [
    "http://localhost:3000",
    "http://localhost",
    "http://compress.bayusamudra.my.id",
    "https://compress.bayusamudra.my.id",
  ]

  app.add_middleware(
    CORSMiddleware, 
    allow_origins=origin,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
  )

  app.mount("/ws", build_socket(state), "Socket")

  @app.middleware("http")
  async def add_addition_cors(req: Request, call_next):
    response = await call_next(req)
    response.headers["Access-Control-Allow-Private-Network"] = "true"
    return response

  @app.get("/")
  async def root_path():
    return {"status": "success"}

  @app.get("/status")
  async def ping():
    return {"status": "success", "isReady" : state.getState("isReady")}

  @app.post("/upload")
  async def upload(token:str = Form(...), file: UploadFile = File(...), alpha: bool = Form(...)):
    if file.content_type.lower() != "image/png" and \
        file.content_type.lower() != "image/jpg" and \
        file.content_type.lower() != "image/jpeg":
      raise HTTPException(status_code=400, detail="Tipe data gambar tidak diizinkan")

    if token == state.getState("subscribeSID"):
      imageFile = file.file
      matrix, mode = await convertFileToArray(imageFile)
      
      state.setState("imageReady", False)
      state.setState("imageLoaded", True)
      state.setState("imageMatrix", matrix)
      state.setState("imageMode", mode)

      formatFile = file.content_type.lower()
      state.setState("format", formatFile)

      if formatFile != "image/png":
        state.setState("isAlphaAvailable", False)
      else:
        state.setState("isAlphaAvailable", alpha)

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
      f = await convertArrayToIO(res, state.getState("imageMode") ,state.getState("format"))

      filename = state.getState("filename") + "." + str(level) + "." + state.getState("extension")

      return Response(f.read(), 
        headers={"Content-Disposition": f'attachment; filename="{filename}"'}, 
        media_type="application/octet-stream")

  @app.get("/compress/{level}/status/")
  async def getLevel(level: int, alpha: Optional[bool] = False):
    _, level = await compress_image_by_cache(state, round(level, 3), alpha=alpha)

    return {"success": True, "compress": level, "isAlphaAvailable": state.getState("isAlphaAvailable"), "executionTime": state.getState("execTime")}

  @app.get("/compress/{level}")
  async def compressImage(level: int, alpha: Optional[bool] = False):
    if not state.getState("imageReady"):
      raise HTTPException(status_code=404, detail="Gambar belum diproses")
    else:
      res,_ = await compress_image_by_cache(state, level, alpha=alpha)
      f = await convertArrayToIO(res, state.getState("imageMode"), state.getState("format"))

      return StreamingResponse(f, media_type=state.getState("format"))

  return app

def run_server_one(port=80):
  app = build_api(State())
  uvicorn.run(app, host="0.0.0.0", port=port, reload=False, workers=1)
  
