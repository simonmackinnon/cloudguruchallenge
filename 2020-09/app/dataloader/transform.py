import logging
import numpy
import pandas

from datetime import datetime

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%d-%m-%Y %H:%M:%S')

def mergeCsvFiles(usaCovidDataFilename, johnHopkinsRecoveryDataFilename):
    logger.info('Merging: ' + usaCovidDataFilename + ' and: ' + johnHopkinsRecoveryDataFilename)
    usaCovidData = pandas.read_csv(usaCovidDataFilename) 
    johnHopkinsData = pandas.read_csv(johnHopkinsRecoveryDataFilename)
    return(mergeCsvData(usaCovidData, johnHopkinsData))

def mergeCsvData(usaCovidData, johnHopkinsData):
    logger.info('Merging usaCovidData and johnHopkinsData')
    usaJohnHopkinsData = filterForUsaData(johnHopkinsData)
    mergedData = mergeData(usaCovidData, usaJohnHopkinsData)
    mergedSelectedData = selectColumns(mergedData)
    return(mergedSelectedData)
    
def filterForUsaData(johnHopkinsData):
    return(johnHopkinsData[johnHopkinsData['Country/Region'].isin(['US'])])
    
def mergeData(usaCovidData, usaJohnHopkinsData):
    mergedData = pandas.merge(usaCovidData, usaJohnHopkinsData, left_on='date', right_on='Date')
    return(mergedData)
    
def selectColumns(data):
    selectedData = data[["date", "cases", "deaths", "Recovered"]]
    selectedData.rename(columns={'Recovered': 'recovered'}, inplace=True)
    return(selectedData)