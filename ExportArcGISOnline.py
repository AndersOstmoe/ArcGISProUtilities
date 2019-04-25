# -*- coding: UTF-8 -*-

from arcgis.gis import *
import os
from zipfile import ZipFile

# public_data_item_id = 'a04933c045714492bda6886f355416f2'
#
# anon_gis = GIS()
#
# data_item = anon_gis.content.get(public_data_item_id)
# # print(data_item)
#
# data_item.download(save_path='c:/disktemp')
#
# zf = ZipFile('c:/disktemp/LA_Hub_Datasets.zip')
# zf.extractall(path='c:/disktemp/LA_Hub_datasets')
#
# file_list = os.listdir('c:/disktemp/LA_Hub_datasets/')
# print(file_list)

from arcgis.gis import GIS
from arcgis.mapping import WebMap


gis = GIS(username="agostmoe",password="1Fairlane1")


# Finn kartet
mapItemID = '7d48a11ae8f943ed96338ba9b904cda8'
mapItem = gis.content.get(mapItemID)
mapObject = WebMap(mapItem)

for layer in mapObject.layers:
    print(layer.title)
    if (layer.layerType == "ArcGISFeatureLayer"):
        try:
            layerItem = gis.content.get(layer.itemId)
            tagFound = False
            for tag in layerItem.tags:
                if (tag == "E18DGEksport"):
                    tagFound = True
                    break
                print(tag)
            if (tagFound):
                nedlastingsnavn = layerItem.name
                print("Eksporterer " + nedlastingsnavn)
                exportItem = layerItem.export(nedlastingsnavn, "Shapefile")
                print("Laster ned")
                print(exportItem.download(save_path="C:\DiskTemp"))
                print("Sletter")
                print(exportItem.delete())
        except:
            pass



    # ItemID = 'd2b98af66a5b4433ae3ed34bdeb323b2'
# dataItem = gis.content.get(ItemID)
# nedlastingsnavn = dataItem.name
# print("Eksporterer " + nedlastingsnavn)
#
# exportItem = dataItem.export(nedlastingsnavn, "Shapefile")
#
# print("Laster ned")
# print(exportItem.download(save_path="C:\DiskTemp"))
# print("Sletter")
# print(exportItem.delete())

