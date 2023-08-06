from ticsummary import DataTIC
from dataclasses import dataclass
import json
from mysql.connector import Error
import mysql.connector
from numpy import ndarray
from typing import Final
from wrapt_timeout_decorator import *


#import array
TABLE_1FIELD_NAME:Final = "id_RUN"
TABLE_2FIELD_NAME:Final = "ACSN"
TABLE_3FIELD_NAME:Final = "Date_Time"
TABLE_4FIELD_NAME:Final = "Thresholds_X_JSON"
TABLE_5FIELD_NAME:Final = "Thresholds_Y_JSON"
TABLE_6FIELD_NAME:Final = "TimeSlice_B1"
TABLE_7FIELD_NAME:Final = "Delay_B1"
TABLE_8FIELD_NAME:Final = "TimeSlice_B2"
TABLE_9FIELD_NAME:Final = "Delay_B2"
TABLE_10FIELD_NAME:Final = "DATA_X1_JSON"
TABLE_11FIELD_NAME:Final = "DATA_Y1_JSON"
TABLE_12FIELD_NAME:Final = "DATA_X2_JSON"
TABLE_13FIELD_NAME:Final = "DATA_Y2_JSON"
TABLE_14FIELD_NAME:Final = "Thresholds_GS_JSON"
TABLE_15FIELD_NAME:Final = "DATA_GS1_JSON"
TABLE_16FIELD_NAME:Final = "DATA_GS2_JSON"

@dataclass
class ParameterConnection:
    user: str = ""
    password: str = ""
    host: str = ""
    database: str = ""
    table: str = ""
    port: int = 0
    
    def getConfig(self):
        return {
            'user': self.user,
            'password': self.password,
            'host': self.host,
            'database': self.database,
            'port': self.port,
            'raise_on_warnings': True
            }

def openConnection(parameters):
    config = parameters.getConfig()
    return mysql.connector.connect(**config)
    
def getRecordByIdFirstbank(parameters, connector, id):
    select_record_query = "SELECT " + TABLE_3FIELD_NAME + "," + TABLE_6FIELD_NAME + "," + TABLE_7FIELD_NAME + "," + TABLE_10FIELD_NAME + "," + TABLE_11FIELD_NAME + "," + TABLE_15FIELD_NAME + " FROM " + parameters.table + " WHERE " + TABLE_1FIELD_NAME + " = " + str(id)
    with connector.cursor() as cursor:
        try:
            cursor.execute(select_record_query)
            result = cursor.fetchall()
            resultArray = ndarray()
            for i in range(0,result[0][3].size()):
                resultArray[i] = result[0][3][i] + result[0][4][i] + result[0][5][i]
            return DataTIC.DownloadData(
                id=id,
                dateTime=result[0][0],
                delay=result[0][2],
                timeslice=result[0][1],
                matrix=resultArray
                )
            #data = json.loads(result[0][0])
            #print (data[0])
            #print(data)
            #data = json.loads(result)
            
        except Error as e:
            print("Error while connecting to MySQL:", e)

def getRecordByIdSecondBank(parameters, connector, id):
    select_record_query = "SELECT " + TABLE_3FIELD_NAME + "," + TABLE_6FIELD_NAME + "," + TABLE_7FIELD_NAME + "," + TABLE_12FIELD_NAME + "," + TABLE_13FIELD_NAME + "," + TABLE_16FIELD_NAME + " FROM " + parameters.table + " WHERE " + TABLE_1FIELD_NAME + " = " + str(id)
    with connector.cursor() as cursor:
        try:
            cursor.execute(select_record_query)
            result = cursor.fetchall()
            resultArray = ndarray()
            for i in range(0,result[0][3].size()):
                resultArray[i] = result[0][3][i] + result[0][4][i] + result[0][5][i]
            return DataTIC.DownloadData(
                id=id,
                dateTime=result[0][0],
                delay=result[0][2],
                timeslice=result[0][1],
                matrix=resultArray
                )
            #data = json.loads(result[0][0])
            #print (data[0])
            #print(data)
            #data = json.loads(result)
            
        except Error as e:
            print("Error while connecting to MySQL:", e)
@timeout(1)
def parametersIsValid(parameters):
    config = parameters.getConfig()
    try:
        with mysql.connector.connect(**config) as connector:
            print(connector)
            return getCountRecords(parameters, connector) > 0
    except Error as e:
        print("Error while connecting to MySQL:", e)
        return 0
    
def getCountRecords(parameters, connector):
    cursor = connector.cursor()
    query = "SELECT COUNT(*) FROM " + parameters.table
    #print(query)
    cursor.execute(query)
    result = cursor.fetchall()
    print("Count:",result[0][0])
    cursor.close()
    return result[0][0]
        
if __name__ == "__main__":
    parameters = ParameterConnection(
        user = "viewer",
        password = "HereJustToSee",
        host = "ma-s.jinr.ru",
        database = "TIC",
        table = "session_test2",
        port = 3306
        )
    print(parametersIsValid(parameters))