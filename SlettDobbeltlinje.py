import arcpy


Road_feature_class = r"C:\Users\ander\OneDrive - Asplan Viak\Prosjekter\616937 Dordal Grimstad\Data\Trafikkberegninger\JoinTrafikkberegning.gdb\SpatialJoin_Subset"
Status_Table = r"C:\Users\ander\OneDrive - Asplan Viak\Prosjekter\616937 Dordal Grimstad\Data\Trafikkberegninger\JoinTrafikkberegning.gdb\Slettes"

TARGETIDs_to_be_deleted = []
IDS_found = []
with arcpy.da.SearchCursor(Road_feature_class, ['OBJECTID', 'TARGET_FID', 'JOIN_FID']) as cursor:
    for row in cursor:
        if (row[1] not in TARGETIDs_to_be_deleted) and (row[2] not in TARGETIDs_to_be_deleted):
            TARGETIDs_to_be_deleted.append(row[1])
            TARGETIDs_to_be_deleted.append(row[2])
            IDS_found.append(row[0])
            print(row[0])



# Create 25 new rows. Set the initial row ID and distance values
# Create insert cursor for table
cursor = arcpy.da.InsertCursor(Status_Table, ["FID", "Slettes"])
for i in IDS_found:
    cursor.insertRow([i, 1])

