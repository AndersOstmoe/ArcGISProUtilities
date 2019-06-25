import arcpy
from arcpy import da
import os

inTable = r'C:\Users\anders.ostmoe\OneDrive - Asplan Viak\Prosjekter\616937 Dordal Grimstad\Data\Innspill\TilbakemeldingerEksternt_20190620\eb3800053c534e0f8e35c0c8a691b12c.gdb\TilbakemeldingerEksternt__ATTACH'
InnspillTable = r'C:\Users\anders.ostmoe\OneDrive - Asplan Viak\Prosjekter\616937 Dordal Grimstad\Data\Innspill\TilbakemeldingerEksternt_20190620\eb3800053c534e0f8e35c0c8a691b12c.gdb\TilbakemeldingerEksternt'
fileLocation = r'C:\Users\anders.ostmoe\OneDrive - Asplan Viak\Prosjekter\616937 Dordal Grimstad\Data\Innspill\20190617\Vedlegg3'



with da.SearchCursor(inTable,['DATA', 'ATT_NAME', 'REL_GLOBALID', 'ATTACHMENTID']) as cursor:
    for item in cursor:
        attachment = item[0]
        globalid = item[2]
        objectID = item[3]

        InnspillRows = da.SearchCursor(InnspillTable, ['GLOBALID', 'NAVN'])

        for InnspillRow in InnspillRows:
            globalIDInnspill = InnspillRows[0]
            navn = InnspillRows[1]
            if globalIDInnspill == globalid:
                break

        filename = ("Vdlg_" + str(objectID) + "_" + navn + "_" + str(item[1])).replace(" ","_").replace("-","_").replace(",","_").replace(";","_").replace("/","_")[:145]
        open(fileLocation + os.sep + filename, 'wb').write(attachment.tobytes())
        del item
        del filename
        del attachment