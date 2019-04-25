# -*- coding: UTF-8 -*-
import arcpy
import datetime
import os


def create_adhoc_file_geodatabase(path, name):
    rightnow = datetime.datetime.now()
    database_name = name + "_" + str(rightnow.year) + str(rightnow.month) + str(rightnow.day) + "_" + str(
        rightnow.hour) + "_" + str(rightnow.minute) + "_" + str(rightnow.second)
    arcpy.CreateFileGDB_management(path, database_name, "10.0")
    return os.path.join(path, database_name + ".gdb")


InputPath = arcpy.GetParameterAsText(0)
InputName = arcpy.GetParameterAsText(1)

Newest_date = create_adhoc_file_geodatabase(InputPath, InputName)

arcpy.SetParameterAsText(2, Newest_date)