import arcpy
from arcpy import da
import os

inTable = r'C:\Users\anders.ostmoe\OneDrive - Asplan Viak\Prosjekter\616937 Dordal Grimstad\Data\Innspill\20190626\Planoppstart\e6950ed840cc423c91ee9a31aed87c09.gdb\TilbakemeldingerEksternt__ATTACH'
InnspillTable = r'C:\Users\anders.ostmoe\OneDrive - Asplan Viak\Prosjekter\616937 Dordal Grimstad\Data\Innspill\20190626\Planoppstart\e6950ed840cc423c91ee9a31aed87c09.gdb\TilbakemeldingerEksternt'
fileLocation = r'C:\Users\anders.ostmoe\OneDrive - Asplan Viak\Prosjekter\616937 Dordal Grimstad\Data\Innspill\20190626\Planoppstart\Vedlegg'



with da.SearchCursor(inTable,['DATA', 'ATT_NAME', 'REL_GLOBALID', 'ATTACHMENTID']) as cursor:
    for item in cursor:
        attachment = item[0]
        attachmentname = str(item[1])
        globalid = item[2]
        objectID = item[3]

        dotposition = attachmentname.rfind(".")
        attachmentdocname = attachmentname[:dotposition][:60]
        attachmentextension = attachmentname[dotposition:]


        InnspillRows = da.SearchCursor(InnspillTable, ['GLOBALID', 'NAVN'])

        for InnspillRow in InnspillRows:
            globalIDInnspill = InnspillRows[0]
            navn = InnspillRows[1]
            if globalIDInnspill == globalid:
                break

        filename = ("Vdlg_" + str(objectID) + "_" + navn + "_" + attachmentdocname).replace(" ","_").replace("-","_").replace(",","_").replace(";","_").replace("/","_").replace("\\","_").replace("(","_").replace(")","_").replace(".","_") + attachmentextension
        path_and_filename = fileLocation + os.sep + filename

        try:
            open(path_and_filename, 'wb').write(attachment.tobytes())
            print("Lagret " + path_and_filename)
        except:
            print("Kunne ikke lagre " + path_and_filename)
        del item
        del filename
        del attachment