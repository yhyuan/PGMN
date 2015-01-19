# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# PGMN2.py
# Created on: 2015-01-19 11:17:55.00000
#   (generated by ArcGIS/ModelBuilder)
# Description: 
# ---------------------------------------------------------------------------

# Import arcpy module
import arcpy, os
import sys, zipfile, time

reload(sys)
sys.setdefaultencoding("latin-1")

from datetime import date
start_time = time.time()

OUTPUT_PATH = "output"
INPUT_PATH = "input"
if arcpy.Exists(OUTPUT_PATH + "\\PGMN.gdb"):
	os.system("rmdir " + OUTPUT_PATH + "\\PGMN.gdb /s /q")
os.system("del " + OUTPUT_PATH + "\\*PGMN*.*")
arcpy.CreateFileGDB_management(OUTPUT_PATH, "PGMN", "9.3")
arcpy.env.workspace = OUTPUT_PATH + "\\PGMN.gdb"


# Local variables:
PGMN_WELLS = "input\\PGMN.gdb\\PGMN_WELLS_1107"
PGMN_WELLS_Layer = "PGMN_WELLS_Layer"
PGMN_WELLS_OUTPUT = "output\\PGMN.gdb\\PGMN_WELLS"

# Process: Add Fields
arcpy.AddField_management(PGMN_WELLS, "X", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddField_management(PGMN_WELLS, "Y", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")

# Process: Calculate Fields
arcpy.CalculateField_management(PGMN_WELLS, "Y", "float(!LAT!)", "PYTHON", "")
arcpy.CalculateField_management(PGMN_WELLS, "X", "float(!LONG_!)", "PYTHON", "")

# Process: Make XY Event Layer
arcpy.MakeXYEventLayer_management(PGMN_WELLS, "x", "y", PGMN_WELLS_Layer, "GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]];-400 -400 1000000000;-100000 10000;-100000 10000;8.98315284119521E-09;0.001;0.001;IsHighPrecision", "")

# Process: Copy Features
arcpy.CopyFeatures_management(PGMN_WELLS_Layer, PGMN_WELLS_OUTPUT, "", "0", "0", "0")

# Process: Delete Field
arcpy.DeleteField_management(PGMN_WELLS, "X;Y")

arcpy.AddField_management(PGMN_WELLS, "ELVA_GROUN", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddField_management(PGMN_WELLS, "NO_RECORD", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.CalculateField_management(PGMN_WELLS, "ELVA_GROUN", "!ELEV_GROUND!", "PYTHON", "")
arcpy.CalculateField_management(PGMN_WELLS, "NO_RECORD", "!NO_RECORD_!", "PYTHON", "")

# Process: Delete Field
arcpy.DeleteField_management(PGMN_WELLS_OUTPUT, "ELEV_GROUND;NO_RECORD_")
arcpy.DeleteField_management(PGMN_WELLS_OUTPUT, "X;Y")



# Local variables:
PGMN_WELLS_RESULTS_TABLE = "PGMN_WELLS_RESULTS_1107"
PGMN_WELLS_SAMPLES_TABLE = "PGMN_WELLS_SAMPLES_1107"
PGMN_WELLS_RESULTS = "input\\PGMN.gdb\\" + PGMN_WELLS_RESULTS_TABLE
PGMN_WELLS_SAMPLES = "input\\PGMN.gdb\\" + PGMN_WELLS_SAMPLES_TABLE
PGMN_WELLS_RESULTS_View = "PGMN_WELLS_RESULTS_View"
PGMN_WELLS_SAMPLES_View = "PGMN_WELLS_SAMPLES_View"
PGMN_WELLS_RESULTS_Layer = "PGMN_WELLS_RESULTS_Layer"
PGMN_WELLS_SAMPLES_RESULTS_OUTPUT = "output\\PGMN.gdb\\PGMN_WELLS_SAMPLES_RESULTS"

PGMN_WELLS_OLD = "input\\PGMN.gdb\\PGMN_WELLS"  # Old PGMN WELLS. Since there is no update for preciptation and water level. Use it 

chemDict = {}
fields = ["PGMN_WELL", "SAMPLE_DAT"]
with arcpy.da.SearchCursor(PGMN_WELLS_SAMPLES, fields) as cursor:
    for row in cursor:
		if row[0] in chemDict:
			chemDict[row[0]].append(row[1])
		else:
			chemDict[row[0]] = [row[1]]

levelDict = {}
prepDict = {}
fields = ["PGMN_WELL", "Level_Avai", "Prep_Avai"]
with arcpy.da.SearchCursor(PGMN_WELLS_OLD, fields) as cursor:
    for row in cursor:
		levelDict[row[0]] = row[1]
		prepDict[row[0]] = row[2]

# Process: Add Fields
arcpy.AddField_management(PGMN_WELLS_OUTPUT, "Chem_Avai", "SHORT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddField_management(PGMN_WELLS_OUTPUT, "Level_Avai", "SHORT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddField_management(PGMN_WELLS_OUTPUT, "Prep_Avai", "SHORT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddField_management(PGMN_WELLS_OUTPUT, "CHEM_CONTE", "TEXT", "", "", "5000", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddField_management(PGMN_WELLS_OUTPUT, "SiteID", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddField_management(PGMN_WELLS_OUTPUT, "ID", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddField_management(PGMN_WELLS_OUTPUT, "Site_ID", "LONG", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")

fields = ('PGMN_WELL', 'Chem_Avai', 'CHEM_CONTE', "Level_Avai", "Prep_Avai", "SiteID", "ID", "Site_ID")
with arcpy.da.UpdateCursor(PGMN_WELLS_OUTPUT, fields) as cursor:
	for row in cursor:
		if row[0] in chemDict:
			row[1] = 1
			aList = sorted(chemDict[row[0]])
			row[2] = ', '.join(map(lambda x: str(x).split(' ')[0], aList))
		else:
			row[1] = 0
			row[2] = ''
		if row[0] in levelDict:
			row[3] = levelDict[row[0]]
		else:
			row[3] = 0
		if row[0] in prepDict:
			row[4] = prepDict[row[0]]
		else:
			row[4] = 0
		row[5] = row[0][5:8]
		row[6] = row[0][:8]
		row[7] = int(row[0][5:8])
		cursor.updateRow(row)
#print chemDict
#arcpy.AddIndex_management(PGMN_WELLS_OUTPUT, "PGMN_WELLS", "PGMN_WELLSIndex", "NON_UNIQUE", "NON_ASCENDING")
arcpy.Project_management(PGMN_WELLS_OUTPUT, arcpy.env.workspace + "\\PGMNWELLS", "PROJCS['WGS_1984_Web_Mercator_Auxiliary_Sphere',GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Mercator_Auxiliary_Sphere'],PARAMETER['False_Easting',0.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',0.0],PARAMETER['Standard_Parallel_1',0.0],PARAMETER['Auxiliary_Sphere_Type',0.0],UNIT['Meter',1.0]]", "NAD_1983_To_WGS_1984_5", "GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]")
arcpy.Delete_management(PGMN_WELLS_OUTPUT, "FeatureClass")


# Process: Make Table View
arcpy.MakeTableView_management(PGMN_WELLS_RESULTS, PGMN_WELLS_RESULTS_View, "", "", "OBJECTID OBJECTID VISIBLE NONE;SAMPLENUM SAMPLENUM VISIBLE NONE;LISTID LISTID VISIBLE NONE;MATRIX MATRIX VISIBLE NONE;PARMNAME PARMNAME VISIBLE NONE;DILUTION DILUTION VISIBLE NONE;REPORT_VALUE REPORT_VALUE VISIBLE NONE;UNITS UNITS VISIBLE NONE;VALQUALIFIER VALQUALIFIER VISIBLE NONE;REMARK1 REMARK1 VISIBLE NONE;REMARK2 REMARK2 VISIBLE NONE")

# Process: Add Fields
arcpy.AddField_management(PGMN_WELLS_RESULTS_View, "X", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddField_management(PGMN_WELLS_RESULTS_View, "Y", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")

# Process: Calculate Fields
arcpy.CalculateField_management(PGMN_WELLS_RESULTS_View, "X", "0.0", "PYTHON", "")
arcpy.CalculateField_management(PGMN_WELLS_RESULTS_View, "Y", "0.0", "PYTHON", "")

# Process: Add Attribute Index
#arcpy.AddIndex_management(PGMN_WELLS_RESULTS_View, "SAMPLENUM", "sampleNumIndex", "NON_UNIQUE", "NON_ASCENDING")

# Process: Make Table View (2)
arcpy.MakeTableView_management(PGMN_WELLS_SAMPLES, PGMN_WELLS_SAMPLES_View, "", "", "OBJECTID OBJECTID VISIBLE NONE;PGMN_WELL PGMN_WELL VISIBLE NONE;SAMPLENUM SAMPLENUM VISIBLE NONE;SAMPLE_DAT SAMPLE_DAT VISIBLE NONE;CONFIDENCE CONFIDENCE VISIBLE NONE;COMMENTS COMMENTS VISIBLE NONE;IONIC_BALA IONIC_BALA VISIBLE NONE;LAB LAB VISIBLE NONE;LAB_ID LAB_ID VISIBLE NONE")

# Process: Add Join
arcpy.AddJoin_management(PGMN_WELLS_RESULTS_View, "SAMPLENUM", PGMN_WELLS_SAMPLES_View, "SAMPLENUM", "KEEP_ALL")
		
# Process: Make XY Event Layer
arcpy.MakeXYEventLayer_management(PGMN_WELLS_RESULTS_View, PGMN_WELLS_RESULTS_TABLE + ".X", PGMN_WELLS_RESULTS_TABLE + ".Y", PGMN_WELLS_RESULTS_Layer, "", "")

# Process: Copy Features
arcpy.CopyFeatures_management(PGMN_WELLS_RESULTS_Layer, PGMN_WELLS_SAMPLES_RESULTS_OUTPUT, "", "0", "0", "0")

# Process: Delete Field
arcpy.DeleteField_management(PGMN_WELLS_SAMPLES_RESULTS_OUTPUT, PGMN_WELLS_RESULTS_TABLE + '_X;' + PGMN_WELLS_RESULTS_TABLE + '_Y;' + PGMN_WELLS_SAMPLES_TABLE + '_OBJECTID;' + PGMN_WELLS_SAMPLES_TABLE + '_SAMPLENUM')

fieldList = arcpy.ListFields(PGMN_WELLS_SAMPLES_RESULTS_OUTPUT)  #get a list of fields for each feature class
removedFieldNames = []
fiedNameTypeDict = {}
for field in fieldList:
	#print field.type
	if ((PGMN_WELLS_RESULTS_TABLE in field.name)  or (PGMN_WELLS_SAMPLES_TABLE in field.name)):
		removedFieldNames.append(field.name)
		if field.type == 'String':
			fiedNameTypeDict[field.name] = 'TEXT'
		if field.type == 'Double':
			fiedNameTypeDict[field.name] = 'DOUBLE'
		if field.type == 'Date':
			fiedNameTypeDict[field.name] = 'DATE'

for fieldname in removedFieldNames:
	newFieldName = ''
	if (PGMN_WELLS_RESULTS_TABLE in fieldname):
		newFieldName = fieldname[len(PGMN_WELLS_RESULTS_TABLE) + 1:]
	if (PGMN_WELLS_SAMPLES_TABLE in fieldname):
		newFieldName = fieldname[len(PGMN_WELLS_SAMPLES_TABLE) + 1:]
	#print newFieldName
	#print fiedNameTypeDict[fieldname]
	# Process: Add Field
	arcpy.AddField_management(PGMN_WELLS_SAMPLES_RESULTS_OUTPUT, newFieldName, fiedNameTypeDict[fieldname], "", "", "", "","NULLABLE", "NON_REQUIRED", "")
	# Process: Calculate Field                            
	arcpy.CalculateField_management(PGMN_WELLS_SAMPLES_RESULTS_OUTPUT, newFieldName, "!" + fieldname + "!", "PYTHON", "")

arcpy.DeleteField_management(PGMN_WELLS_SAMPLES_RESULTS_OUTPUT, ";".join(removedFieldNames))	
#arcpy.AddIndex_management(PGMN_WELLS_SAMPLES_RESULTS_OUTPUT, "PGMN_WELLS", "PGMN_WELLSIndex2", "NON_UNIQUE", "NON_ASCENDING")
arcpy.Project_management(PGMN_WELLS_SAMPLES_RESULTS_OUTPUT, arcpy.env.workspace + "\\PGMN_WELLS_SAMPLES_RESULTS_OUTPUT", "PROJCS['WGS_1984_Web_Mercator_Auxiliary_Sphere',GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Mercator_Auxiliary_Sphere'],PARAMETER['False_Easting',0.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',0.0],PARAMETER['Standard_Parallel_1',0.0],PARAMETER['Auxiliary_Sphere_Type',0.0],UNIT['Meter',1.0]]", "NAD_1983_To_WGS_1984_5", "GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]")
arcpy.Delete_management(PGMN_WELLS_SAMPLES_RESULTS_OUTPUT, "FeatureClass")


# Prepare the msd, mxd, and readme.txt
os.system("copy " + INPUT_PATH + "\\PGMN.msd " + OUTPUT_PATH)
os.system("copy " + INPUT_PATH + "\\PGMN.mxd " + OUTPUT_PATH)
f = open (INPUT_PATH + "\\readme_PGMN.txt","r")
data = f.read()
f.close()
import time
dateString = time.strftime("%Y/%m/%d", time.localtime())
data = data.replace("[DATE]", dateString)
f = open (OUTPUT_PATH + "\\readme_PGMN.txt","w")
f.write(data)
f.close()

# Compress the msd, mxd, readme.txt and file geodatabase together into a zip file named PGMN.zip, which will be send to web service publisher. 
'''
target_dir = OUTPUT_PATH + '\\PGMN.gdb'
zip = zipfile.ZipFile(OUTPUT_PATH + '\\PGMN.zip', 'w', zipfile.ZIP_DEFLATED)
rootlen = len(target_dir) + 1
for base, dirs, files in os.walk(target_dir):
   for file in files:
      fn = os.path.join(base, file)
      zip.write(fn, "PGMN.gdb\\" + fn[rootlen:])
zip.write(OUTPUT_PATH + '\\PGMN.msd', "PGMN.msd")
zip.write(OUTPUT_PATH + '\\PGMN.mxd', "PGMN.mxd")
zip.write(OUTPUT_PATH + '\\readme_PGMN.txt', "readme_PGMN.txt")
zip.close()
'''
elapsed_time = time.time() - start_time
print elapsed_time	