# Import arcpy module
import arcpy, os
import sys, zipfile, time

reload(sys)
sys.setdefaultencoding("latin-1")

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

	
from datetime import date
start_time = time.time()

OUTPUT_PATH = "output"
INPUT_PATH = "input"
if arcpy.Exists(OUTPUT_PATH + "\\PGMN.gdb"):
	os.system("rmdir " + OUTPUT_PATH + "\\PGMN.gdb /s /q")
os.system("del " + OUTPUT_PATH + "\\*PGMN*.*")
os.system("del " + OUTPUT_PATH + "\\Chemistry\\*.txt")
os.system("del " + OUTPUT_PATH + "\\Shapefile\\*PGMN.*")

arcpy.CreateFileGDB_management(OUTPUT_PATH, "PGMN", "9.3")
arcpy.env.workspace = OUTPUT_PATH + "\\PGMN.gdb"


# Local variables:
PGMN_WELLS_TABLE = "PGMN_WELLS_1107"
PGMN_WELLS_SAMPLES_TABLE = "PGMN_WELLS_SAMPLES_1107"
PGMN_WELLS_RESULTS_TABLE = "PGMN_WELLS_RESULTS_1107"
PGMN_WELLS_OLD_TABLE = "PGMN_WELLS"  # Old PGMN WELLS. Since there is no update for preciptation and water level. Use it
PGMN_WELLS_SAMPLES = "input\\PGMN.gdb\\" + PGMN_WELLS_SAMPLES_TABLE
PGMN_WELLS_OLD = "input\\PGMN.gdb\\" + PGMN_WELLS_OLD_TABLE  # Old PGMN WELLS. Since there is no update for preciptation and water level. Use it 
PGMN_WELLS_RESULTS = "input\\PGMN.gdb\\" + PGMN_WELLS_RESULTS_TABLE

########################Start Generating PGMN_WELLS layer########################
PGMN_WELLS = "input\\PGMN.gdb\\" + PGMN_WELLS_TABLE
PGMN_WELLS_Layer = "PGMN_WELLS_Layer"
PGMN_WELLS_Layer_SHAPE = "PGMN_WELLS_Layer_SHAPE"
PGMN_WELLS_OUTPUT = "output\\PGMN.gdb\\PGMN_WELLS_OUTPUT"
PGMN_WELLS_SHAPE_OUTPUT = "output\\PGMN.gdb\\PGMN_WELLS"
# Process: Add Fields
arcpy.AddField_management(PGMN_WELLS, "X", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddField_management(PGMN_WELLS, "Y", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")

# Process: Calculate Fields
arcpy.CalculateField_management(PGMN_WELLS, "Y", "float(!LAT!)", "PYTHON", "")
arcpy.CalculateField_management(PGMN_WELLS, "X", "float(!LONG_!)", "PYTHON", "")

# Process: Make XY Event Layer
arcpy.MakeXYEventLayer_management(PGMN_WELLS, "x", "y", PGMN_WELLS_Layer, "GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]];-400 -400 1000000000;-100000 10000;-100000 10000;8.98315284119521E-09;0.001;0.001;IsHighPrecision", "")

arcpy.MakeXYEventLayer_management(PGMN_WELLS, "LONGITUDE", "LATITUDE", PGMN_WELLS_Layer_SHAPE, "GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]];-400 -400 1000000000;-100000 10000;-100000 10000;8.98315284119521E-09;0.001;0.001;IsHighPrecision", "")
arcpy.CopyFeatures_management(PGMN_WELLS_Layer_SHAPE, PGMN_WELLS_SHAPE_OUTPUT, "", "0", "0", "0")
arcpy.DeleteField_management(PGMN_WELLS_SHAPE_OUTPUT, "LAT;LONG_;X;Y")
arcpy.FeatureClassToShapefile_conversion([PGMN_WELLS_SHAPE_OUTPUT], OUTPUT_PATH + "\\Shapefile")
arcpy.Delete_management(PGMN_WELLS_SHAPE_OUTPUT, "FeatureClass")

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
arcpy.Project_management(PGMN_WELLS_OUTPUT, arcpy.env.workspace + "\\PGMN_WELLS", "PROJCS['WGS_1984_Web_Mercator_Auxiliary_Sphere',GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Mercator_Auxiliary_Sphere'],PARAMETER['False_Easting',0.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',0.0],PARAMETER['Standard_Parallel_1',0.0],PARAMETER['Auxiliary_Sphere_Type',0.0],UNIT['Meter',1.0]]", "NAD_1983_To_WGS_1984_5", "GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]")
arcpy.Delete_management(PGMN_WELLS_OUTPUT, "FeatureClass")
arcpy.AddIndex_management(arcpy.env.workspace + "\\PGMN_WELLS", "PGMN_WELL", "PGMN_WELLSIndex", "NON_UNIQUE", "NON_ASCENDING")
########################Finish Generating PGMN_WELLS layer########################

########################Start Generating PGMN_WELLS_SAMPLES_RESULTS layer########################
samplesDict = {}
samplesTEXTDict = {}
fields = ["PGMN_WELL", "SAMPLENUM", "SAMPLE_DAT", "CONFIDENCE", "COMMENTS", "IONIC_BALA", "LAB", "LAB_ID"]
with arcpy.da.SearchCursor(PGMN_WELLS_SAMPLES, fields) as cursor:
    for row in cursor:
		if row[1] in chemDict:
			print "SAMPLENUM is not unique. Something must be wrong."
		else:
			samplesDict[row[1]] = [row[0]] + [row[2], row[3], row[4], row[5], row[6], row[7]]
		if row[0] in samplesTEXTDict:
			samplesTEXTDict[row[0]].append(row)
		else:
			samplesTEXTDict[row[0]] = [row]

resultsTEXTDict = {}
rows = []
fields = ["SAMPLENUM", "LISTID", "MATRIX", "PARMNAME", "DILUTION", "REPORT_VALUE", "UNITS", "VALQUALIFIER", "REMARK1", "REMARK2"]
with arcpy.da.SearchCursor(PGMN_WELLS_RESULTS, fields) as cursor:
    for row in cursor:
		rows.append([(0, 0)] + list(row) + samplesDict[row[0]])
		if row[0] in resultsTEXTDict:
			resultsTEXTDict[row[0]].append(row)
		else:
			resultsTEXTDict[row[0]] = [row]

featureName = "PGMN_WELLS_SAMPLES_RESULTS"
featureFieldList = [["SAMPLENUM", "TEXT", "", "", "", "", "NON_NULLABLE", "REQUIRED", ""], ["LISTID", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", ""], ["MATRIX", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", ""], ["PARMNAME", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", ""], ["DILUTION", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", ""], ["REPORT_VALUE", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", ""], ["UNITS", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", ""], ["VALQUALIFIER", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", ""], ["REMARK1", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", ""], ["REMARK2", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", ""]]
featureFieldList = featureFieldList + [["PGMN_WELL", "TEXT", "", "", "", "", "NON_NULLABLE", "REQUIRED", ""], ["SAMPLE_DAT", "DATE", "", "", "", "", "NULLABLE", "NON_REQUIRED", ""], ["CONFIDENCE", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", ""], ["COMMENTS", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", ""], ["IONIC_BALA", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", ""], ["LAB", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", ""], ["LAB_ID", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", ""]]
featureInsertCursorFields = tuple(["SHAPE@XY"] + map(lambda field: field[0], featureFieldList))
createFeatureClass(featureName, rows, featureFieldList, featureInsertCursorFields)
arcpy.AddIndex_management(arcpy.env.workspace + "\\" + featureName, "PGMN_WELL", "PGMN_WELLSIndex", "NON_UNIQUE", "NON_ASCENDING")
########################Finish Generating PGMN_WELLS_SAMPLES_RESULTS layer########################
########################Start Generating Chemistry text files ########################
def compare(x, y):
	inorganics = ["Aluminum", "Antimony", "Arsenic", "Barium", "Beryllium", "Boron", "Cadmium", "Chromium", "Cobalt", "Copper", "Iron", "Lead", "Manganese", "Molybdenum", "Nickel", "Selenium", "Silver", "Strontium", "Thallium", "Titanium", "Uranium", "Vanadium", "Zinc", "Fluoride", "Sulphate", "Solids; dissolved", "Anions", "Cations", "Conductivity Estimated", "Ion balance calculation", "Solids; Dissolved Estimated", "Calcium", "Hardness", "Magnesium", "Potassium", "Sodium", "Alkalinity; total fixed endpt", "Conductivity", "pH", "Langeliers index calculation", "Saturation pH Estimated", "Nitrogen; ammonia+ammonium", "Nitrogen; nitrate+nitrite", "Nitrogen; nitrite", "Phosphorus; phosphate", "Nitrogen; total Kjeldahl", "Phosphorus; total", "Carbon; dissolved inorganic", "Carbon; dissolved organic", "Silicon; reactive silicate", "Chloride", "Bromide", "Iodide (I-)", "Nitrogen; nitrate"]
	PARMNAME1 = x[1]
	PARMNAME2 = y[1]
	if PARMNAME1 == PARMNAME2:
		return (x[2] - y[2]).days
	else:
		if (PARMNAME1 in inorganics and PARMNAME2 in inorganics) or (not(PARMNAME1 in inorganics) and not(PARMNAME2 in inorganics)):
			if PARMNAME1 > PARMNAME2:
				return 1
			elif PARMNAME1 == PARMNAME2:
				return 0
			else:
				return -1
		elif (PARMNAME1 in inorganics) and (not (PARMNAME2 in inorganics)):
			return -1
		else:
			return 1

txtHead = "PGMN_WELL\tParameterName\tSampleDate\tValue\tUnits\tQualifiers\tRemark1\tRemark2\tConfidenceLevel\tComments\tIonbalance\tLabName\tSampleNumber\n"
for PGMN_WELL, rows in samplesTEXTDict.iteritems():
	aList = []
	for row in rows:
		SAMPLENUM = row[1]
		SAMPLE_DAT = row[2]
		CONFIDENCE = row[3]
		COMMENTS = row[4]
		IONIC_BAL =row[5]
		LAB = row[6]
		aList = aList + map(lambda x: [PGMN_WELL, x[3], SAMPLE_DAT, x[5], x[6], x[7], x[8], x[9], CONFIDENCE, COMMENTS, IONIC_BAL, LAB, SAMPLENUM], resultsTEXTDict[SAMPLENUM])
		'''
		for x in resultsTEXTDict[SAMPLENUM]:
			PARMNAME = x[3]
			REPORT_VALUE = x[5]
			UNITS = x[6]
			VALQUALIFIER = x[7]
			REMARK1 = x[8]
			REMARK2 = x[9]
		'''
	aList = sorted(aList, cmp=compare)
	aList = map(lambda xs: xs[:2] + [str(xs[2])[:10]] + xs[3:], aList) # convert date type to string
	aList = map(lambda xs: map(lambda x: "" if (x is None) else x, xs), aList)  # convert None to empty string
	aList = map(lambda xs: map(lambda x: str(x) if (isinstance(x, float)) else x, xs), aList) # convert number to string
	aList = map(lambda xs: "\t".join(xs), aList) # create each line
	chemistryFile = open(OUTPUT_PATH + "\\Chemistry\\" + PGMN_WELL + ".txt",'w+')
	chemistryFile.write(txtHead)
	for line in aList:
		chemistryFile.write(line.encode('utf-8') + '\n')
	#chemistryFile.write(txtHead + "\n".join(aList))
	chemistryFile.close();
########################Finish Generating Chemistry text files ########################


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

elapsed_time = time.time() - start_time
print elapsed_time	