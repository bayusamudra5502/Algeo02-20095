from starlette.responses import FileResponse, Response
from lib.converter.convert import *
from fastapi.datastructures import UploadFile
from fastapi.params import File, Form
from fastapi.responses import StreamingResponse
import uvicorn
from fastapi import FastAPI, HTTPException
from api.state import *
from api.state import State

app = FastAPI()
state:State = None

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
    state.setState("imageMatrix", matrix)
    state.setState("format", file.content_type.lower())

    filename = file.filename.split(".")

    state.setState("filename", ".".join(filename[:-1]))
    state.setState("extension",filename[-1])

    state.setState("imageReady", True)
    return {"success": True}
  else:
    raise HTTPException(status_code=403, detail="Anda tidak memiliki akses untuk upload")

@app.get("/compress/{level}/download/")
async def downloadCompressedImage(level: int):
  if not state.getState("imageReady"):
    raise HTTPException(status_code=404, detail="Gambar belum diproses")
  else:
    res = state.getState("imageMatrix")
    f = convertArrayToIO(res, state.getState("format"))

    filename = state.getState("filename") + "." + str(level) + "." + state.getState("extension")

    # return FileResponse("./.tmp/cache", media_type="application/octet-stream", filename=f"")
    return Response(f.read(), 
      headers={"Content-Disposition": f'attachment; filename="{filename}"'}, 
      media_type="application/octet-stream")

@app.get("/compress/{level}")
async def compressImage(level: int):
  if not state.getState("imageReady"):
    raise HTTPException(status_code=404, detail="Gambar belum diproses")
  else:
    res = state.getState("imageMatrix")
    f = convertArrayToIO(res, state.getState("format"))

    return StreamingResponse(f, media_type=state.getState("format"))

def run_server(state_data: State):
  global state
  state = state_data

  uvicorn.run(app, port=5502)
