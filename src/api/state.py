import asyncio

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