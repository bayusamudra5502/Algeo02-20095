class State:
  __data = {}

  def __init__(self) -> None:
    self.reset()

  def getState(self,stateName):
    return self.__data[stateName]
  
  def setState(self, name, value):
    self.__data[name] = value

  def reset(self):
    self.__data["isReady"] = True
    self.__data["SVDDecomp"] = None
    self.__data["subscribeSID"] = None
    self.__data["ws"] = None
    self.__data["imageMatrix"] = None
  
  # Socket Handler
  async def sendUpdateState(self, processId, comment):
    payload = {"processId": processId, "comment": comment}
    await self.__data["ws"].emit("progress", data=payload, to=self.__data["subscribeSID"])
  
  def isSubscribed(self):
    return self.__data["subscribeSID"] != None