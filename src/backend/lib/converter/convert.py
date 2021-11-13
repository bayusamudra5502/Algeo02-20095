from PIL import Image
import numpy as np
import io

def convertFileToArray(file):
  with Image.open(file) as im:
    return np.array(im.convert("RGBA")), im.mode

def convertArrayToIO(array: np.ndarray, md:str, mime:str="image/png"):
  im = Image.fromarray(array)
  im = im.convert(md)
  f = io.BytesIO()

  if mime == "image/png":
    im.save(f, format="PNG")
  else:
    im = im.convert("RGB")
    im.save(f, "JPEG")

  f.seek(0)
  return f

