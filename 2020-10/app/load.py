import boto3
import numpy
import pandas
import logging
import notify

from datetime import date, datetime, timedelta

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%d-%m-%Y %H:%M:%S')

from botocore.exceptions import ClientError

def put_record(date, cases, deaths, recovered, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")

    table = dynamodb.Table('covidData')
    
    put_response = None
    
    try:
        logger.info("putting record: " + date)
        put_response = table.put_item(
            Item={
                'date': datetime.strptime(date, '%Y-%m-%d').date().isoformat(),
                'cases': int(cases),
                'deaths': int(deaths),
                'recovered': int(recovered)
            }
        )
    except ClientError as e:
        notify.notify("Error loading data into DB", "There was an error loading data for {} {}".format(date, e))
        # Ignore the ConditionalCheckFailedException, bubble up
        # other exceptions.
        if e.response['Error']['Code'] != 'ConditionalCheckFailedException':
            raise
    
    return put_response
    
def load_data(data, latestDateStr, dynamodb=None, initial=False):
    if initial == True:
        logger.info("loading initial data")
        rows_added=0
        for index, row, in data.iterrows():
            if validateRow(row):
                put_record(row['date'], row['cases'], row['deaths'], row['recovered'], dynamodb)
                rows_added += 1
            else:
                notify.notify("Error reading data", "There was an reading data. Got {}".format(row))
        if rows_added > 0:        
            notify.notify("Inital Data Load Successful. Added {} rows".format(rows_added), "Inital load of Covid Data into DB was successful. {} rows were added".format(rows_added))
    else:
        latestDate = datetime.strptime(latestDateStr, '%Y-%m-%d').date()
        check_date = latestDate + timedelta(days=1)
        maxDateAvailable = datetime.strptime(data['date'].max(), '%Y-%m-%d').date()
        
        logger.info("maxDate in data {}".format(maxDateAvailable))
        
        rows_added=0
        
        while check_date <= maxDateAvailable:
            logger.info("check_date {}".format(check_date.isoformat()))
            try:
                records = data.loc[data['date'] == check_date.isoformat()]
            except KeyError:
                records = None
                logger.info("cant find date for {}".format(check_date))
                #alert there's not data matching that date, and there should be!
            if not records.empty:
                for index, row, in records.iterrows():
                    if validateRow(row):
                        put_record(row['date'], row['cases'], row['deaths'], row['recovered'], dynamodb)
                        rows_added += 1
            check_date += timedelta(days=1)
            
        if rows_added > 0:        
            notify.notify("Successfully added {} rows".format(rows_added), "Subsequent load of Covid Data into DB was successful. {} rows were added".format(rows_added))
        
def validateRow(row):
    return(validateDate(row['date']) and validateNumber(row['cases']) and validateNumber(row['deaths']) and validateNumber(row['recovered']))
            
def validateDate(date_text):
    try:
        datetime.strptime(date_text, '%Y-%m-%d')
        return(True)
    except ValueError:
        logger.exception("Incorrect data format, should be YYYY-MM-DD")
        return(False)
        
def validateNumber(input):
    try:
       val = int(input)
       return(True)
    except ValueError:
       logger.exception("Incorrect data format, expected number input, got {}".format(input))
       return(False)
    
    