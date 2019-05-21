# -*- coding: UTF-8 -*-
import arcpy
import datetime
import os


def find_newest_date(table, field):
    newest_date = datetime.datetime(2017, 1, 1)
    with arcpy.da.SearchCursor(table, field) as cursor:
        for row in cursor:
            date = row[0]
            if date is not None:
                if date > newest_date:
                    newest_date = date
                # print(date)

    return newest_date


def create_adhoc_file_geodatabase(path, name):
    rightnow = datetime.datetime.now()
    database_name = name + "_" + str(rightnow.year) + str(rightnow.month) + str(rightnow.day) + "_" + str(
        rightnow.hour) + "_" + str(rightnow.minute) + "_" + str(rightnow.second)
    arcpy.CreateFileGDB_management(path, database_name, "10.0")
    return os.path.join(path, database_name + ".gdb")


def oppdaterdata(input_feature_layer, featurelayer):

    def definefieldmapping(inputfeatureclass, fieldmappings, fieldmap, infieldname, outfieldname, fieldaliasname, fieldtype):
        fieldmap.addInputField(inputfeatureclass, infieldname)
        outputfield = fieldmap.outputField
        outputfield.name = outfieldname
        outputfield.aliasname = fieldaliasname
        outputfield.type = fieldtype
        fieldmap.outputField = outputfield
        fieldmappings.addFieldMap(fieldmap)

    fieldmappings = arcpy.FieldMappings()
    fieldmappings.addTable(featurelayer)

    fieldmap_1 = arcpy.FieldMap()
    definefieldmapping(input_feature_layer, fieldmappings, fieldmap_1, "Tilbakemelding", "Tilbakemelding", "Tilbakemelding", "TEXT")
    fieldmap_2 = arcpy.FieldMap()
    definefieldmapping(input_feature_layer, fieldmappings, fieldmap_2, "Tilbakemelder", "Tilbakemelder", "Tilbakemelder", "SHORT")
    fieldmap_3 = arcpy.FieldMap()
    definefieldmapping(input_feature_layer, fieldmappings, fieldmap_3, "Navn", "Navn", "Navn", "TEXT")
    fieldmap_4 = arcpy.FieldMap()
    definefieldmapping(input_feature_layer, fieldmappings, fieldmap_4, "Adresse", "Adresse", "Adresse", "TEXT")
    fieldmap_5 = arcpy.FieldMap()
    definefieldmapping(input_feature_layer, fieldmappings, fieldmap_5, "Postnummer", "Postnummer", "Postnummer", "SHORT")
    fieldmap_6 = arcpy.FieldMap()
    definefieldmapping(input_feature_layer, fieldmappings, fieldmap_6, "Poststed", "Poststed", "Poststed", "TEXT")
    fieldmap_7 = arcpy.FieldMap()
    definefieldmapping(input_feature_layer, fieldmappings, fieldmap_7, "Epost", "Epost", "Epost", "TEXT")
    fieldmap_8 = arcpy.FieldMap()
    definefieldmapping(input_feature_layer, fieldmappings, fieldmap_8, "Organisasjon", "Organisasjon", "Organisasjon", "TEXT")
    fieldmap_9 = arcpy.FieldMap()
    definefieldmapping(input_feature_layer, fieldmappings, fieldmap_9, "GlobalID", "GlobalID", "GlobalID", "GlobalID")
    fieldmap_10 = arcpy.FieldMap()
    definefieldmapping(input_feature_layer, fieldmappings, fieldmap_10, "Status", "Status", "Status", "SHORT")

    fieldmap_11 = arcpy.FieldMap()
    definefieldmapping(input_feature_layer, fieldmappings, fieldmap_11, "CreationDate", "OpprettetDato", "OpprettetDato", "DATE")


    arcpy.Append_management(input_feature_layer, featurelayer, "NO_TEST", fieldmappings)


print("Oppretter database")
AdHoc_database = create_adhoc_file_geodatabase(r"C:\Users\ander\OneDrive - Asplan Viak\Prosjekter\616937 Dordal Grimstad\Innspillsoverforing", "TempInnspill")

print("Henter ut informasjon")
arcpy.FeatureClassToFeatureClass_conversion("https://services.arcgis.com/whQdER0woF1J7Iqk/arcgis/rest/services/TilbakemeldingerEksterntVer3_Redigering/FeatureServer/0",
                                            AdHoc_database,
                                            "InnspillRedigert")

arcpy.FeatureClassToFeatureClass_conversion("https://services.arcgis.com/whQdER0woF1J7Iqk/arcgis/rest/services/E18DG_TilbakemeldingerEksternt_Ver3_20190404/FeatureServer/0",
                                            AdHoc_database,
                                            "Innspill")

print("Finner siste dato")
Last_message_date =  find_newest_date(os.path.join(AdHoc_database, "InnspillRedigert"), "OpprettetDato") + \
                     datetime.timedelta(seconds=1)

Selection_expression = "CreationDate > timestamp '" + Last_message_date.strftime("%Y.%m.%d %H:%M:%S") + "'"
print("Henter ut siste innspill. " + Selection_expression)
arcpy.FeatureClassToFeatureClass_conversion(os.path.join(AdHoc_database, "Innspill"),
                                            AdHoc_database,
                                            "InnspillUtvalgt",
                                            Selection_expression)

print("Legger til statusfelt")
arcpy.AddField_management(os.path.join(AdHoc_database, "InnspillUtvalgt"), "Status", "SHORT")

print("Setter status til ny og 0! :-)")
arcpy.CalculateField_management(os.path.join(AdHoc_database, "InnspillUtvalgt"), "Status", "0", "PYTHON3")
# arcpy.CalculateField_management(os.path.join(AdHoc_database, "InnspillUtvalgt"), "PStoy", "0", "PYTHON3")
# arcpy.CalculateField_management(os.path.join(AdHoc_database, "InnspillUtvalgt"), "PTrafikk", "0", "PYTHON3")
# arcpy.CalculateField_management(os.path.join(AdHoc_database, "InnspillUtvalgt"), "PVeg", "0", "PYTHON3")
# arcpy.CalculateField_management(os.path.join(AdHoc_database, "InnspillUtvalgt"), "IPKulturarv", "0", "PYTHON3")
# arcpy.CalculateField_management(os.path.join(AdHoc_database, "InnspillUtvalgt"), "IPNaturmangfold", "0", "PYTHON3")
# arcpy.CalculateField_management(os.path.join(AdHoc_database, "InnspillUtvalgt"), "IPByOgBygd", "0", "PYTHON3")
# arcpy.CalculateField_management(os.path.join(AdHoc_database, "InnspillUtvalgt"), "IPLandkkap", "0", "PYTHON3")
# arcpy.CalculateField_management(os.path.join(AdHoc_database, "InnspillUtvalgt"), "IPNaturressurs", "0", "PYTHON3")
# arcpy.CalculateField_management(os.path.join(AdHoc_database, "InnspillUtvalgt"), "ROS", "0", "PYTHON3")


print("Oppdaterer Online")
oppdaterdata(os.path.join(AdHoc_database, "InnspillUtvalgt"), "https://services.arcgis.com/whQdER0woF1J7Iqk/arcgis/rest/services/TilbakemeldingerEksterntVer3_Redigering/FeatureServer/0" )