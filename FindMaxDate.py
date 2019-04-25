# -*- coding: UTF-8 -*-
import arcpy
import datetime


def find_newest_date(table, field):
    newest_date = datetime.datetime(2017, 1, 1)
    with arcpy.da.SearchCursor(table, field) as cursor:
        for row in cursor:
            date = row[0]
            if date > newest_date:
                newest_date = date
            print(date)

    return newest_date


InputTable = arcpy.GetParameterAsText(0)
InputField = arcpy.GetParameterAsText(1)

Newest_date = find_newest_date(InputTable, InputField)

arcpy.SetParameterAsText(2, Newest_date)


