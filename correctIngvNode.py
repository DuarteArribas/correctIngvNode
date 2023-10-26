from dbConnection import *
from configparser import ConfigParser
from getopt       import getopt

def main():
  # Config file
  config = ConfigParser()
  config.read("conf.cfg")
  # Command-line args
  argumentList = sys.argv[1:]
  options      = "hd"
  long_options = ["Help","Delete"]
  try:
    arguments,values = getopt(argumentList, options, long_options)
  except Exception as err:
    print(err)
    print(f"Unknown option  ")
    exit(-1)
  # Handle options
  deleteFiles = False
  for currentArgument,currentValue in arguments:
    if currentArgument in ("-h", "--Help"):
      print("Usage: python3 deleteRepeated.py [-h] [-d]\n\nh | Help : Display help and usage\nd | Delete : Remove files (Default is to display the planned removal only)")
      exit(0)
    elif currentArgument in ("-d", "--Delete"):
      deleteFiles = True
  # Connect to DB
  print("Connecting to DGW")
  dgw  = DBConnection(
    config.get("DEFAULT","DGW_IP"),
    config.get("DEFAULT","DGW_PORT"),
    config.get("DEFAULT","DGW_DB_NAME"),
    config.get("DEFAULT","DGW_DB_USER"),
    config.get("DEFAULT","DGW_DB_PWD")
  )
  dgw.connect()
  print("Connecting to ingv")
  ingv  = DBConnection(
    config.get("DEFAULT","INGV_IP"),
    config.get("DEFAULT","INGV_PORT"),
    config.get("DEFAULT","INGV_DB_NAME"),
    config.get("DEFAULT","INGV_DB_USER"),
    config.get("DEFAULT","INGV_DB_PWD")
  )
  ingv.connect()
  print("--------")
  commands        = []
  commandsChanged = False
  # Start script
  ingv.cursor.execute("SELECT id FROM station;")
  ingvStationIds = ingv.cursor.fetchall()
  for ingvStationId in ingvStationIds:
    dgw.cursor.execute("SELECT id FROM station_item WHERE id_station = %s",(ingvStationId[0],))
    dgwItems = dgw.cursor.fetchall()
    ingv.cursor.execute("SELECT id FROM station_item WHERE id_station = %s",(ingvStationId[0],))
    ingvItems = ingv.cursor.fetchall()
    if dgwItems != ingvItems:
      if not commandsChanged:
        commandsChanged = True
      print("STATION ID",ingvStationId[0])
      print("DGW ITEMS",[item[0] for item in dgwItems])
      print("INGV ITEMS",[item[0] for item in ingvItems])
      for ingvRow in ingvItems:
        if ingvRow[0] not in [item[0] for item in dgwItems]:
          if deleteFiles:
            ingv.cursor.execute("DELETE FROM station_item WHERE id = %s",(ingvRow[0],))
            ingv.conn.commit()
          s = "Command to be executed: " if not deleteFiles else "Command executed: "
          s += f"DELETE FROM station_item WHERE id = {ingvRow[0]};"
          commands.append(s)
          print(s)
      print("--------")

  if commandsChanged:
    with open("commands","w") as f:
      for command in commands:
        f.write(command)
        f.write("\n")
            
if __name__ == "__main__":
    main()