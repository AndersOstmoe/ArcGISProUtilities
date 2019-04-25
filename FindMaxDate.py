# -*- coding: UTF-8 -*-
import arcpy


def find_max_date(table, field):
    with arcpy.da.SearchCursor(feature_class, Field) as cursor:
        for row in cursor:
            row[0]



def test_find_max_date():
    find_max_date()