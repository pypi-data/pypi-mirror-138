import os
import json

class bal:
  def start(foldername, userdatajsonfilename, template):
    foldername = str(foldername)
    template = dict(template)
    userdatajsonfilename = str(userdatajsonfilename)
    if os.path.isfile(f"{foldername}/{userdatajsonfilename}"):
      return "invalid file exist"
    else:
      if os.path.exists(foldername):
        f = open(f"{foldername}/{userdatajsonfilename}", "x")
        f.write(json.dumps(template))
        return "created[file]"
      else:
        folder = os.mkdir(foldername)
        f = open(f"{foldername}/{userdatajsonfilename}", "x")
        f.write(json.dumps(template))
        return "created[file, folder]"

class instance:
  def addinstance(foldername, userdatajsonfilename, valuename, value):
    userdatajsonfilename = str(userdatajsonfilename)
    foldername = str(foldername)
    valuename = str(valuename)
    value = str(value)
    f = open(f"{foldername}/{userdatajsonfilename}", "rt").read()
    unloadf = json.loads(f)
    unloadf.update({valuename: value})
    os.remove(f"{foldername}/{userdatajsonfilename}")
    f = open(f"{foldername}/{userdatajsonfilename}","x")
    f.write(json.dumps(unloadf))
  
  def subtractinstance(foldername, userdatajsonfilename, valuename):
    userdatajsonfilename = str(userdatajsonfilename)
    foldername = str(foldername)
    valuename = str(valuename)
    f = open(f"{foldername}/{userdatajsonfilename}", "rt").read()
    unloadf = json.loads(f)
    unloadf.pop(valuename)
    os.remove(f"{foldername}/{userdatajsonfilename}")
    f = open(f"{foldername}/{userdatajsonfilename}","x")
    f.write(json.dumps(unloadf))

class value:
  def newvalue(foldername, userdatajsonfilename, valuename, value):
    userdatajsonfilename = str(userdatajsonfilename)
    foldername = str(foldername)
    valuename = str(valuename)
    value = int(value)
    f = open(f"{foldername}/{userdatajsonfilename}", "rt").read()
    unloadf = json.loads(f)
    unloadf.update({valuename: value})
    os.remove(f"{foldername}/{userdatajsonfilename}")
    f = open(f"{foldername}/{userdatajsonfilename}","x")
    f.write(json.dumps(unloadf))
  
  def changevalue(foldername, userdatajsonfilename, valuename, value):
    userdatajsonfilename = str(userdatajsonfilename)
    foldername = str(foldername)
    valuename = str(valuename)
    value = int(value)
    f = open(f"{foldername}/{userdatajsonfilename}", "rt").read()
    fw = open(f"{foldername}/{userdatajsonfilename}", "w")
    unloadf = json.loads(f)
    if valuename in unloadf:
      unloadf.update({valuename: value})
      fw.write(json.dumps(unloadf))

  def getvalue(foldername, userdatajsonfilename,valuename):
    userdatajsonfilename = str(userdatajsonfilename)
    foldername = str(foldername)
    valuename = str(valuename)

    f = open(f"{foldername}/{userdatajsonfilename}", "rt").read()
    unloadf = json.loads(f)
    return str(unloadf[valuename])

  def addvalue(foldername, userdatajsonfilename,valuename, value):
    userdatajsonfilename = str(userdatajsonfilename)
    foldername = str(foldername)
    value = int(value)
    valuename = str(valuename)

    f = open(f"{foldername}/{userdatajsonfilename}", "rt").read()
    fw = open(f"{foldername}/{userdatajsonfilename}", "w")
    unloadf = json.loads(f)
    unloadf[valuename] = unloadf[valuename] + value
    fw.write(json.dumps(unloadf))
    
  def subtractvalue(foldername, userdatajsonfilename,valuename, value):
    userdatajsonfilename = str(userdatajsonfilename)
    foldername = str(foldername)
    value = int(value)
    valuename = str(valuename)

    f = open(f"{foldername}/{userdatajsonfilename}", "rt").read()
    fw = open(f"{foldername}/{userdatajsonfilename}","w")
    unloadf = json.loads(f)
    unloadf[valuename] = unloadf[valuename] - value
    fw.write(json.dumps(unloadf))

