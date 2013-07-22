# -*- coding: utf-8 -*-
import cx_Oracle
from datetime import date
 
class Sample:
    def __init__(self, PGMN_WELL, SAMPLENUM, SAMPLE_DAT, CONFIDENCE, COMMENTS, IONIC_BALA, LAB, LAB_ID):
        self.PGMN_WELL = PGMN_WELL
        self.SAMPLENUM = SAMPLENUM
        self.SAMPLE_DAT = SAMPLE_DAT
        self.CONFIDENCE = CONFIDENCE
        self.COMMENTS = COMMENTS
        self.IONIC_BALA = IONIC_BALA
        self.LAB = LAB
        self.LAB_ID = LAB_ID
 
class Result:
    def __init__(self, SAMPLENUM, LISTID, MATRIX, PARMNAME, DILUTION, REPORT_VAL, UNITS, VALQUALIFI, REMARK1, REMARK2):
        self.SAMPLENUM = SAMPLENUM
        self.LISTID = LISTID
        self.MATRIX = MATRIX
        self.PARMNAME = PARMNAME
        self.DILUTION = DILUTION
        self.REPORT_VAL = REPORT_VAL
        self.UNITS = UNITS
        self.VALQUALIFI = VALQUALIFI
        self.REMARK1 = REMARK1
        self.REMARK2 = REMARK2
EN_FR_Dict = {"Aluminum": "Aluminium","Antimony": "Antimoine","Arsenic": "Arsenic","Barium": "Baryum","Beryllium": "B&eacute;ryllium","Boron": "Bore","Cadmium": "Cadmium","Chromium": "Chrome","Cobalt": "Cobalt","Copper": "Cuivre","Iron": "Fer","Lead": "Plomb","Manganese": "Mangan&egrave;se","Molybdenum": "Molybd&egrave;ne","Nickel": "Nickel","Selenium": "S&eacute;l&eacute;nium","Silver": "Argent","Strontium": "Strontium","Thallium": "Thallium","Titanium": "Titane","Uranium": "Uranium","Vanadium": "Vanadium","Zinc": "Zinc","Fluoride": "Fluorure","Sulphate": "Sulfate","Solids; dissolved": "Solides; dissous","Anions": "Anions","Cations": "Cations","Conductivity Estimated": "Estimation de la conductivit&eacute; ","Ion balance calculation": "Calcul de l'&eacute;quilibre ionique","Solids; Dissolved Estimated": "Solides; estimation des solides dissous ","Calcium": "Calcium","Hardness": "Titre hydrotim&eacute;trique","Magnesium": "Magn&eacute;sium","Potassium": "Potassium","Sodium": "Sodium","Alkalinity; total fixed endpt": "Alcalinit&eacute;; point limite d'alcalinit&eacute; totale","Conductivity": "Conductivit&eacute;","pH": "pH","Langeliers index calculation": "Calcul de l'index de Langelier","Saturation pH Estimated": "Estimation du pH de saturation","Nitrogen; ammonia+ammonium": "Nitrog&egrave;ne; ammoniac+ammonium","Nitrogen; nitrate+nitrite": "Nitrog&egrave;ne; nitrate+nitrite","Nitrogen; nitrite": "Nitrog&egrave;ne; nitrite","Phosphorus; phosphate": "Phosphore; phosphate","Nitrogen; total Kjeldahl": "Nitrog&egrave;ne; azote total Kjeldahl","Phosphorus; total": "Phosphore; total","Carbon; dissolved inorganic": "Carbone; carbone inorganique dissous","Carbon; dissolved organic": "Carbone; carbone organique dissous","Silicon; reactive silicate": "Silicium; silicate r&eacute;actif","Chloride": "Chlorure","Bromide": "Bromure","Iodide (I-)": "Ion iodure (I-)","Nitrogen; nitrate": "Nitrog&egrave;ne; nitrate"}
Chem_EN = ["Aluminum", "Antimony", "Arsenic", "Barium", "Beryllium", "Boron", "Cadmium", "Chromium", "Cobalt", "Copper", "Iron", "Lead", "Manganese", "Molybdenum", "Nickel", "Selenium", "Silver", "Strontium", "Thallium", "Titanium", "Uranium", "Vanadium", "Zinc", "Fluoride", "Sulphate", "Solids; dissolved", "Anions", "Cations", "Conductivity Estimated", "Ion balance calculation", "Solids; Dissolved Estimated", "Calcium", "Hardness", "Magnesium", "Potassium", "Sodium", "Alkalinity; total fixed endpt", "Conductivity", "pH", "Langeliers index calculation", "Saturation pH Estimated", "Nitrogen; ammonia+ammonium", "Nitrogen; nitrate+nitrite", "Nitrogen; nitrite", "Phosphorus; phosphate", "Nitrogen; total Kjeldahl", "Phosphorus; total", "Carbon; dissolved inorganic", "Carbon; dissolved organic", "Silicon; reactive silicate", "Chloride", "Bromide", "Iodide (I-)", "Nitrogen; nitrate"]
 
def calculateHeadTable(resultDict, isEnglish):
    head_EN = "<table class='fishTable'  border='1'><tr>"
    i = 0
    for PARMNAME in Chem_EN:
        if resultDict.has_key(PARMNAME):
            if isEnglish:
                head_EN = head_EN + "<td><a href=\"#index" + str(i) + "\">" + PARMNAME + "</a></td>"
            else:
                head_EN = head_EN + "<td><a href=\"#index" + str(i) + "\">" + EN_FR_Dict[PARMNAME] + "</a></td>"
            if i % 3 == 2:
                head_EN = head_EN + "</tr><tr>"
            i = i + 1
    if isEnglish:
        otherParameters = "Pesticides, Volatile Organic Compounds, and other parameters"
    else:
        otherParameters = "Pesticides, compos&eacute;s organiques volatiles et autres param&egrave;tres"
    if i % 3 == 1:
        head_EN = head_EN + "<td><a href=\"#index" + str(i + 1) + "\"></a></td><td><a href=\"#index" + str(i + 2) + "\"></a></td></tr><tr><td colspan=\"3\"><center><a href=\"#indexOther\">" + otherParameters + "</a></center></td></tr></table>"
    if i % 3 == 2:
        head_EN = head_EN + "<td><a href=\"#index" + str(i + 1) + "\"></a></td></tr><tr><td colspan=\"3\"><center><a href=\"#indexOther\">" + otherParameters + "</a></center></td></tr></table>"
    if i % 3 == 0:
        head_EN = head_EN + "<td colspan=\"3\"><center><a href=\"#indexOther\">" + otherParameters + "</a></center></td></tr></table>"
    return head_EN
 
def calculateResultDict(well_id, sampleList, resultList):
    def f(x): return x.PGMN_WELL == well_id
    samplesInWell = filter(f, sampleList)
 
    SAMPLENUMList = []
    for sample in samplesInWell:
        SAMPLENUMList.append(sample.SAMPLENUM)
 
    def g(x): return x.SAMPLENUM in SAMPLENUMList
    resultsInWell = filter(g, resultList)
 
    resultDict = {}
    for result in resultsInWell:
        if resultDict.has_key(result.PARMNAME):
            resultDict[result.PARMNAME].append(result)
        else:
            resultDict[result.PARMNAME] = [result]
    return resultDict
 
def calculateChartURL(results, sampleDict):
    #<img src='http://chart.apis.google.com/chart?cht=s&chd=t:21.30,42.13,45.85,86.8|33.33,42.86,100.00,19.0&chxt=x,y&chs=500x200&chxl=|0:|2002|2003|2004|2005|2006|2007|2008|2009|2010|2011|1:|0|1.05|2.10(ug/L)'/>
    UNITS = results[0].UNITS
    max = 0.02
    for result in results:
        if result.REPORT_VAL > max :
            max = result.REPORT_VAL
    if len(results) == 1:
          max = 2*max;
 
    valueString = ""
    for result in results:
        if result.REPORT_VAL is not None:
            if result.REPORT_VAL < 0.000001:
                valueString = valueString + "0,"
            else:
                valueString = valueString + ('%.2f' % (result.REPORT_VAL * 100.0 / max)) + ","
        else:
            valueString = valueString + "0,"
 
    beginDate = date(2002, 1, 1)
    endDate = date(2013, 1, 1)
    dateDiff = endDate - beginDate
    dateString = ""
    for result in results:
        sample = sampleDict[result.SAMPLENUM]
        sampleDate = date(sample.SAMPLE_DAT.year, sample.SAMPLE_DAT.month, sample.SAMPLE_DAT.day)
        sampleDelta = (sampleDate - beginDate).days
        sampleDeltaPercent = sampleDelta * 100.0 / dateDiff.days
        dateString = dateString + ('%.2f' % sampleDeltaPercent) + ","
    return "<img src='http://chart.apis.google.com/chart?cht=s&chd=t:" + dateString[:-1] + "|" + valueString[:-1] + "&chxt=x,y&chs=500x200&chxl=|0:|2002|2003|2004|2005|2006|2007|2008|2009|2010|2011|2012|2013|1:|0|" + str(max*0.5) + "|" + str(max) + "(" + UNITS + ")'/>";
 
def calculateDateString(SAMPLE_DAT):
    res = ""
    if SAMPLE_DAT.day < 10:
        res = res + "0" + str(SAMPLE_DAT.day)
    else:
        res = res + str(SAMPLE_DAT.day)
    res = res + "/"
    if SAMPLE_DAT.month < 10:
        res = res + "0" + str(SAMPLE_DAT.month)
    else:
        res = res + str(SAMPLE_DAT.month)
    res = res + "/"
    return res + str(SAMPLE_DAT.year)
 
def removeNone(val):
    if val is not None:
        return str(val)
    else:
        return ""
def calculateTable(results, sampleDict, isEnglish):
    if isEnglish:
        returnString = "<table class='fishTable'  border='1'><tr><th class=\"shaded\"><center>Date</center></th><th class=\"shaded\"><center>Value</center></th><th class=\"shaded\"><center>Units</center></th><th class=\"shaded\"><center>Qualifiers</center></th><th class=\"shaded\"><center>Remark 1</center></th><th class=\"shaded\"><center>Remark 2</center></th><th class=\"shaded\"><center>Confidence Level</center></th><th class=\"shaded\"><center>Comments</center></th><th class=\"shaded\"><center>Sample Number</center></th></tr>"
    else:
        returnString = "<table class='fishTable'  border='1'><tr><th class=\"shaded\"><center>Date</center></th><th class=\"shaded\"><center>Valeur</center></th><th class=\"shaded\"><center>Unit&eacute;</center></th><th class=\"shaded\"><center>Qualificateurs</center></th><th class=\"shaded\"><center>Observation 1</center></th><th class=\"shaded\"><center>Observation 2</center></th><th class=\"shaded\"><center>Niveau de confiance</center></th><th class=\"shaded\"><center>Commentaires</center></th><th class=\"shaded\"><center>Num&eacute;ro d'&eacute;chantillon</center></th></tr>"
    for result in results:
        sample = sampleDict[result.SAMPLENUM]
        returnString =  returnString  + "<tr><td>" + calculateDateString(sample.SAMPLE_DAT) + "</td><td>" + str(result.REPORT_VAL) + "</td><td>" + removeNone(result.UNITS) + "</td><td>" + removeNone(result.VALQUALIFI) + "</td><td>" + removeNone(result.REMARK1) + "</td><td>" + removeNone(result.REMARK2) + "</td><td>" + removeNone(sample.CONFIDENCE) + "</td><td>" + removeNone(sample.COMMENTS) + "</td><td>" + removeNone(sample.SAMPLENUM) + "</td></tr>"
    if isEnglish:
        returnString =  returnString  + "</table>\n<div align=\"right\"><a href=\"#top\">Back to top</a></div><br><br>"
    else:
        returnString =  returnString  + "</table>\n<div align=\"right\"><a href=\"#top\">Haut de la page</a></div><br><br>"
    return returnString
 
def generateCSV(well_id, resultDict, sampleDict, OtherParameters):
    csv = "PGMN_WELL\tParameterName\tSampleDate\tValue\tUnits\tQualifiers\tRemark1\tRemark2\tConfidenceLevel\tComments\tIonbalance\tLabName\tSampleNumber\n"
    for PARMNAME in Chem_EN:
        if resultDict.has_key(PARMNAME):
            results = resultDict[PARMNAME]
            def compare(x, y): return (sampleDict[x.SAMPLENUM].SAMPLE_DAT - sampleDict[y.SAMPLENUM].SAMPLE_DAT).days
            results = sorted(results, cmp=compare)
            for result in results:
                sample = sampleDict[result.SAMPLENUM]
                csv =  csv  + well_id + "\t" + PARMNAME + "\t" + calculateDateString(sample.SAMPLE_DAT) + "\t" + str(result.REPORT_VAL) + "\t" + removeNone(result.UNITS) + "\t" + removeNone(result.VALQUALIFI) + "\t" + removeNone(result.REMARK1) + "\t" + removeNone(result.REMARK2) + "\t" + removeNone(sample.CONFIDENCE) + "\t" + removeNone(sample.COMMENTS)  + "\t" + removeNone(sample.IONIC_BALA)  + "\t" + removeNone(sample.LAB) + "\t" + removeNone(sample.SAMPLENUM) + "\n"
    for PARMNAME in OtherParameters:
        results = resultDict[PARMNAME]
        def compare(x, y): return (sampleDict[x.SAMPLENUM].SAMPLE_DAT - sampleDict[y.SAMPLENUM].SAMPLE_DAT).days
        results = sorted(results, cmp=compare)
        for result in results:
            sample = sampleDict[result.SAMPLENUM]
            csv =  csv  + well_id + "\t" + PARMNAME + "\t" + calculateDateString(sample.SAMPLE_DAT) + "\t" + str(result.REPORT_VAL) + "\t" + removeNone(result.UNITS) + "\t" + removeNone(result.VALQUALIFI) + "\t" + removeNone(result.REMARK1) + "\t" + removeNone(result.REMARK2) + "\t" + removeNone(sample.CONFIDENCE) + "\t" + removeNone(sample.COMMENTS)  + "\t" + removeNone(sample.IONIC_BALA)  + "\t" + removeNone(sample.LAB) + "\t" + removeNone(sample.SAMPLENUM) + "\n"
    handle1 = open("Y:\\PGMN\\WaterChemistry\\" + well_id + ".txt",'w+')
    handle1.write(csv)
    handle1.close();
 
def generateHTML(isEnglish, well_id, resultDict, sampleDict):
    html = ""
    if isEnglish:
        html = "<h2>Water Chemistry  in PGMN Well: " + well_id + "</h2>\n<a name=\"top\"></a><a href=\"../" + well_id + ".txt\">Water Chemistry Data Download (Tab Separated Text File)</a>\n" + calculateHeadTable(resultDict, isEnglish)
    else:
        html = "<h2>Composition chimique de l'eau des puits du R&eacute;seau provincial de contr&ocirc;le des eaux souterraines: " + well_id + "</h2>\n<a name=\"top\"></a><a href=\"../" + well_id + ".txt\">T&eacute;l&eacute;chargement des donn&eacute;es hydro-chimiques (Fichier texte s&eacute;par&eacute;)</a>\n" + calculateHeadTable(resultDict, isEnglish)
    i = 0
    for PARMNAME in Chem_EN:
        if resultDict.has_key(PARMNAME):
            if isEnglish:
                html = html + "<h3><a name=\"index" + str(i) + "\">" + PARMNAME + "</a></h3>\n"
            else:
                html = html + "<h3><a name=\"index" + str(i) + "\">" + EN_FR_Dict[PARMNAME] + "</a></h3>\n"
            results = resultDict[PARMNAME]
            def compare(x, y): return (sampleDict[x.SAMPLENUM].SAMPLE_DAT - sampleDict[y.SAMPLENUM].SAMPLE_DAT).days
            results = sorted(results, cmp=compare)
            html = html + calculateChartURL(results, sampleDict) + "\n"
            html = html + calculateTable(results, sampleDict, isEnglish) + "\n"
            i = i + 1
    if isEnglish:
        html = html + "<h3><a name=\"indexOther\">Pesticides, Volatile Organic Compounds, and other parameters</a></h3>"
    else:
        html = html + "<h3><a name=\"indexOther\">Pesticides, compos&eacute;s organiques volatiles et autres param&egrave;tres</a></h3>"
    OtherParameters = []
    for PARMNAME in sorted(resultDict.iterkeys()):
        if not PARMNAME in Chem_EN:
            OtherParameters.append(PARMNAME)
    for PARMNAME in OtherParameters:
        html = html + "<h3>" + PARMNAME + "</h3>\n"
        results = resultDict[PARMNAME]
        def compare(x, y): return (sampleDict[x.SAMPLENUM].SAMPLE_DAT - sampleDict[y.SAMPLENUM].SAMPLE_DAT).days
        results = sorted(results, cmp=compare)
        html = html + calculateTable(results, sampleDict, isEnglish) + "\n"
    if isEnglish:
        text_file = open("PGMNChemistryEN.htm", "r")
    else:
        text_file = open("PGMNChemistryFR.htm", "r")
    template = text_file.read()
    text_file.close()
    template = template.replace("${CONTENT}", html)
    if isEnglish:
        handle1 = open("Y:\\PGMN\\WaterChemistry\\EN\\" + well_id + ".htm",'w+')
    else:
        handle1 = open("Y:\\PGMN\\WaterChemistry\\FR\\" + well_id + ".htm",'w+')
    handle1.write(template)
    handle1.close();
    if isEnglish:
        generateCSV(well_id, resultDict, sampleDict, OtherParameters)
connection = cx_Oracle.connect('EMRB_PGMN/xxxxxxx@sde')
cursor = connection.cursor()
cursor.execute('SELECT * FROM PGMN_WELLS_SAMPLES')
rows = cursor.fetchall()
sampleDict = {}
sampleList = []
PGMN_WELLList = []
for row in rows:
    sample = Sample(row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])
    sampleList.append(sample)
    PGMN_WELLList.append(row[1])
    if sampleDict.has_key(sample.SAMPLENUM):
        raise ValueError("Sample table should use sample number as unique key. ")
    else:
        sampleDict[sample.SAMPLENUM] = sample
PGMN_WELLSet = set(PGMN_WELLList)
 
cursor.execute('SELECT * FROM PGMN_WELLS_RESULTS')
rows = cursor.fetchall()
 
resultList = []
for row in rows:
    result = Result(row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10])
    resultList.append(result)
 
CHEM_CONTE = "PGMN_WELL\tCHEM_CONTE\n"
for well_id in PGMN_WELLSet:
#for well_id in ["W0000271-1"]:
    resultDict = calculateResultDict(well_id, sampleList, resultList)
    generateHTML(True, well_id, resultDict, sampleDict)
    generateHTML(False, well_id, resultDict, sampleDict)
    def f(x): return x.PGMN_WELL == well_id
    def g(x): return x.SAMPLE_DAT
    def h(x): return calculateDateString(x)
    CHEM_CONTE = CHEM_CONTE + well_id + "\t" + ", ".join(map(h, sorted(map(g, filter(f, sampleList))))) + "\n"
    #print well_id + ", " + str(len(resultDict))
    #print html
handle1 = open("Y:\\PGMN\\WaterChemistry\\CHEM_CONTE.txt",'w+')
handle1.write(CHEM_CONTE)
handle1.close();
#print len(set(PGMN_WELLList))
#print len(sampleList)
connection.close()