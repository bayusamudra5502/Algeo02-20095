import asyncio

class Updater:
  def __init__(self, ws, id) -> None:
      self.__ws = ws
      self.__id = id
      self.__loop = asyncio.new_event_loop()
    
  def sendUpdateState(self, value, comment):
    payload = {"value": value, "comment": comment}
    lastLoop = None

    try:
      lastLoop = asyncio.get_event_loop()
    except Exception:
      pass

    if lastLoop != None and lastLoop.is_running():
      lastLoop.create_task(
        self.__ws.emit("progress", 
          data=payload, 
          to=self.__id)
      )
    else:
      asyncio.set_event_loop(self.__loop)
      
      if not self.__loop.is_running():
        self.__loop.run_until_complete(
          self.__ws.emit("progress", 
                data=payload, 
                to=self.__id)
        )
      else:
        self.__loop.create_task(
          self.__ws.emit("progress", 
            data=payload, 
            to=self.__id)
        )

      if lastLoop != None:
        asyncio.set_event_loop(lastLoop)


class State:
  __data = {}

  def __init__(self) -> None:
    self.reset()
    self.__loop = asyncio.new_event_loop()
    self.__data["ws"] = None

  def getState(self,stateName):
    return self.__data[stateName]
  
  def setState(self, name, value):
    self.__data[name] = value

  def reset(self):
    self.__data["isReady"] = True
    self.__data["SVDDecomp"] = None
    self.__data["subscribeSID"] = None
    self.__data["imageMatrix"] = None
    self.__data["imageReady"] = False
    self.__data["format"] = None
    self.__data["filename"] = None
    self.__data["imageLoaded"] = False
    self.__data["imageMode"] = None
    self.__data["execTime"] = None
    self.__data["isAlphaAvailable"] = True
  
  # Socket Handler
  def sendUpdateState(self, value, comment):
    payload = {"value": value, "comment": comment}
    lastLoop = None

    try:
      lastLoop = asyncio.get_event_loop()
    except Exception:
      pass

    if lastLoop != None and lastLoop.is_running():
      lastLoop.create_task(
        self.__data["ws"].emit("progress", 
          data=payload, 
          to=self.__data["subscribeSID"])
      )
    else:
      asyncio.set_event_loop(self.__loop)
      
      if not self.__loop.is_running():
        self.__loop.run_until_complete(
          self.__data["ws"].emit("progress", 
                data=payload, 
                to=self.__data["subscribeSID"])
        )
      else:
        self.__loop.create_task(
          self.__data["ws"].emit("progress", 
            data=payload, 
            to=self.__data["subscribeSID"])
        )

      if lastLoop != None:
        asyncio.set_event_loop(lastLoop)

  def isSubscribed(self):
    return self.__data["subscribeSID"] != None

  # Util
  def counter_calc(self, number, start, end, cnt):
    return start+ number/cnt * (end-start)
  
  def getUpdater(self):
    return Updater(self.__data["ws"], self.__data["subscribeSID"])