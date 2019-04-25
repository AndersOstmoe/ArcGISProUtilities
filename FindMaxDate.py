# -*- coding: UTF-8 -*-
import arcpy


def find_max_date(table, field):
    var newestdate = ''
    with arcpy.da.SearchCursor(feature_class, Field) as cursor:
        for row in cursor:
            date = row[0]
            print(date)



def test_find_max_date():
    find_max_date()