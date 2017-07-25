import pandas as pd
import serial
import os
from time import sleep

class language:
    def __init__(self, lang = "en"):
        self.lang_pack = {"heading":None, "change_name":None, "refresh_name":None}
        self.table_column_names = [0,1,2,3]
        if lang == "lt":
            self.lang_pack["heading"] = "Duomenys"
            self.lang_pack["change_name"] = "keisti"
            self.lang_pack["refresh_name"] = "Paleisti iš naujo"
            self.table_column_names = ["id", "pavadinimas","riba","atstumas"]
        else:
            self.lang_pack["heading"] = "Sensor data"
            self.lang_pack["change_name"] = "Change"
            self.lang_pack["refresh_name"] = "Refresh"
            self.table_column_names = ["id", "name", "threshold", "value"]

class table_class:
    def __init__(self,
                 table_path = "table.csv", 
                 table_column_names = [0,1,2,3]):
        '''column[0] id
        columns[1] name #any column_name
        column[-2] threshold #any column_name
        column[-1] value #any column_name'''
        

        self.table_path = table_path
        self.table_column_names = table_column_names
        self.id_column= 0
    
    def send_df(self):
        df = pd.read_csv(self.table_path,header = None, names = self.table_column_names)
        print(df)
        return df



    def update_table(self, id, column_number, value):
        df = pd.read_csv(self.table_path,header = None, names = None)
        index = df[df[self.id_column] == id].index[0] #get row index
        df.iloc[index, column_number] = value #change table value
        df.to_csv(self.table_path, index = None, header=None)

       

class sensor:
    def __init__(self,
                 path_name,
                 request_id = b'i',
                 request_get = b'g'):
        self.request_get = request_get

        self.ser = serial.Serial(path_name)
        sleep(0.1)

        self.ser.write(request_id)
        self.id = self.ser.readline().decode().strip()

    def get(self):
        self.ser.write(self.request_get)

        return int(self.ser.readline().decode().strip())


class sensor_data:

    def __init__(self, path_name = "/dev/serial/by-path/"):
        try:
            serial_files = os.listdir(path_name)
        except:
            serial_files = []
        print(serial_files)

        self.sensors = {}

        for file in serial_files:
            sense = sensor(path_name + file)
            self.sensors[sense.id] = sense

    def get(self, id):
        try:
            distance = self.sensors[id].get()
        except:
            distance = 0
        return distance

