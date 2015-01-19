# This script reads a table named FISH_ADVISORY to generate a file geodatabase. 
import sys, arcpy, os, zipfile, time
reload(sys)
sys.setdefaultencoding("latin-1")

import cx_Oracle
from datetime import date
start_time = time.time()
def createFeatureClass(featureName, featureData, featureFieldList, featureInsertCursorFields):
	print "Create " + featureName + " feature class"
	featureNameNAD83 = featureName + "_NAD83"
	featureNameNAD83Path = arcpy.env.workspace + "\\"  + featureNameNAD83
	arcpy.CreateFeatureclass_management(arcpy.env.workspace, featureNameNAD83, "POINT", "", "DISABLED", "DISABLED", "", "", "0", "0", "0")
	# Process: Define Projection
	arcpy.DefineProjection_management(featureNameNAD83Path, "GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]")
	# Process: Add Fields	
	for featrueField in featureFieldList:
		arcpy.AddField_management(featureNameNAD83Path, featrueField[0], featrueField[1], featrueField[2], featrueField[3], featrueField[4], featrueField[5], featrueField[6], featrueField[7], featrueField[8])
	# Process: Append the records
	cntr = 1
	try:
		with arcpy.da.InsertCursor(featureNameNAD83, featureInsertCursorFields) as cur:
			for rowValue in featureData:
				cur.insertRow(rowValue)
				cntr = cntr + 1
	except Exception as e:
		print "\tError: " + featureName + ": " + e.message
	# Change the projection to web mercator
	arcpy.Project_management(featureNameNAD83Path, arcpy.env.workspace + "\\" + featureName, "PROJCS['WGS_1984_Web_Mercator_Auxiliary_Sphere',GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Mercator_Auxiliary_Sphere'],PARAMETER['False_Easting',0.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',0.0],PARAMETER['Standard_Parallel_1',0.0],PARAMETER['Auxiliary_Sphere_Type',0.0],UNIT['Meter',1.0]]", "NAD_1983_To_WGS_1984_5", "GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]")
	#arcpy.FeatureClassToShapefile_conversion([featureNameNAD83Path], OUTPUT_PATH + "\\Shapefile")
	arcpy.Delete_management(featureNameNAD83Path, "FeatureClass")
	print "Finish " + featureName + " feature class."

def createTextFile(fileName, rows, featureFieldList):
	f = open (fileName,"w")
	f.write("\t".join(map(lambda field: field[0], featureFieldList)) + "\r\n")
	f.write("\r\n".join(map(lambda row: "\t".join(map(lambda item: str(item), row[1:])), rows)))
	f.close()

OUTPUT_PATH = "output"
INPUT_PATH = "input"
if arcpy.Exists(OUTPUT_PATH + "\\PGMN.gdb"):
	os.system("rmdir " + OUTPUT_PATH + "\\PGMN.gdb /s /q")
os.system("del " + OUTPUT_PATH + "\\*PGMN*.*")
arcpy.CreateFileGDB_management(OUTPUT_PATH, "PGMN", "9.3")
arcpy.env.workspace = OUTPUT_PATH + "\\PGMN.gdb"

# Read password file to get the password. 
file = open("password.txt")
password = file.readline()
file.close()
connection = cx_Oracle.connect('EMRB_PGMN/' + password + '@sde')
cursor = connection.cursor()


# Generate PGMN_WELLS_SAMPLES_RESULTS feature class. 
featureName = "PGMN_WELLS_SAMPLES_RESULTS"
featureFieldList = [["SAMPLENUM", "TEXT", "", "", "", "", "NON_NULLABLE", "REQUIRED", ""], ["LISTID", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", ""], ["MATRIX", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", ""], ["PARMNAME", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", ""], ["DILUTION", "DOUBLE", "", "", "", "", "NULLABLE", "REQUIRED", ""], ["REPORT_VALUE", "DOUBLE", "", "", "", "", "NULLABLE", "REQUIRED", ""], ["UNITS", "TEXT", "", "", "", "", "NULLABLE", "REQUIRED", ""], ["VALQUALIFIER", "TEXT", "", "", "", "", "NULLABLE", "REQUIRED", ""], ["REMARK1", "TEXT", "", "", "", "", "NULLABLE", "REQUIRED", ""], ["REMARK2", "TEXT", "", "", "", "", "NULLABLE", "REQUIRED", ""], ["PGMN_WELL", "TEXT", "", "", "", "", "NULLABLE", "REQUIRED", ""], ["SAMPLE_DAT", "TEXT", "", "", "", "", "NULLABLE", "REQUIRED", ""], ["CONFIDENCE", "TEXT", "", "", "", "", "NULLABLE", "REQUIRED", ""], ["COMMENTS", "TEXT", "", "", "", "", "NULLABLE", "REQUIRED", ""], ["IONIC_BALA", "TEXT", "", "", "", "", "NULLABLE", "REQUIRED", ""], ["LAB", "TEXT", "", "", "", "", "NULLABLE", "REQUIRED", ""], ["LAB_ID", "TEXT", "", "", "", "", "NULLABLE", "REQUIRED", ""]]
featureInsertCursorFields = tuple(["SHAPE@XY"] + map(lambda field: field[0], featureFieldList))
cursor.execute('SELECT PGMN_WELL, SAMPLENUM, SAMPLE_DAT, CONFIDENCE, COMMENTS, IONIC_BALA, LAB, LAB_ID  FROM PGMN_WELLS_SAMPLES')
rows = cursor.fetchall()
samplesDict = {}
for row in rows:
	samplesDict[row[1]] = row
cursor.execute('SELECT SAMPLENUM, LISTID, MATRIX, PARMNAME, DILUTION, REPORT_VALUE, UNITS, VALQUALIFIER, REMARK1, REMARK2 FROM PGMN_WELLS_RESULTS')
rows = cursor.fetchall()
rows = map(lambda row: [(0, 0)] + list(row) + [samplesDict[row[0]][0]] + list(samplesDict[row[0]][2:]), rows)
createFeatureClass(featureName, rows, featureFieldList, featureInsertCursorFields)





elapsed_time = time.time() - start_time
print elapsed_time
