# -*- coding: UTF-8 -*-
import arcpy


def slettdata(featurelayer):

    Logger = SykehusbyggUtils.Logging()

    # Logger.SkrikTilLog('Kopierer')
    # arcpy.CopyRows_management(featurelayer, "C:\Users\anders.ostmoe\OneDrive - Asplan Viak\Prosjekter\616283_Sykehusbygg\616283 Sykehusbygg\Testbase.gdb\PunkterSykehusDPS2")
    Logger.SkrikTilLog("Sletter")
    arcpy.DeleteRows_management(featurelayer)


def oppdaterdata(inputFeaturelayer, featurelayer):

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

    fieldmap_point_x = arcpy.FieldMap()
    definefieldmapping(inputFeaturelayer, fieldmappings, fieldmap_point_x, "POINT_X", "POINT_X", "POINT_X", "DOUBLE")
    fieldmap_point_y = arcpy.FieldMap()
    definefieldmapping(inputFeaturelayer, fieldmappings, fieldmap_point_y, "POINT_Y", "POINT_Y", "POINT_Y", "DOUBLE")

    Logger = SykehusbyggUtils.Logging()
    Logger.SkrikTilLog('Oppdaterer ' + featurelayer)
    arcpy.Append_management(inputFeaturelayer, featurelayer, "NO_TEST", fieldmappings)
    Logger.SkrikTilLog('Ferdig med å oppdatere ' + featurelayer)


def PubliseringsAvDataHoved(inputFeaturelayer):

    featurelayer = "https://services.arcgis.com/whQdER0woF1J7Iqk/arcgis/rest/services/PunkterSykehusDPSTest/FeatureServer/0"
    slettdata(featurelayer)
    oppdaterdata(inputFeaturelayer, featurelayer)