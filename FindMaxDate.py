# -*- coding: UTF-8 -*-
import arcpy, datetime,


def find_newest_date(table, field):
    newestdate = datetime.datetime(2017, 1, 1)
    with arcpy.da.SearchCursor(table, field) as cursor:
        for row in cursor:
            date = row[0]
            if (date > newestdate):
                newestdate = date
            print(date)

    print (" ")
    print(newestdate)





