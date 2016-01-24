#!/usr/bin/python
import datetime
import cgi
import cgitb; cgitb.enable()
import csv
import urllib
from decimal import Decimal
import mysql.connector
from mysql.connector import errorcode

print "Content-type:text/html\n"

#class to determine price date ranges and performance / Taken from collect.py
class historical_pricing:

    def __init__(self):
        self.Months = [[0,31],[1,28],[2,31],[3,30],[4,31],[5,30],[6,31],[7,31],[8,30],[9,31],[10,30],[11,31]]


    def DateAdjustment(self,date):

        DateObject = datetime.date(int(date[0]),int(date[1]),int(date[2]))
        RefWeekDay = int(datetime.date.weekday(DateObject))
        RefDay = int(date[2])
        RefMonth = int(date[1])

        #Check if Reference week day is a business day
        if RefWeekDay > 4:
            if (date[2] + (4 - int(RefWeekDay))) < 1:
                date[2] = self.Months[(RefMonth-2)][1] + (date[2] + (4 - int(RefWeekDay)))
                date[1] -= 1
            else:
                date[2] += (4 - int(RefWeekDay))

        self.Previous_Day = date[2]
        self.Previous_Year = date[0]
        self.Previous_Month = date[1]
        self.Previous_Date_string = str(datetime.date(date[0],date[1],date[2]))
        return self.Previous_Date_string


    def PriceChange(self,Ticker,current_date,prev_date):

        BasePage = 'http://real-chart.finance.yahoo.com/table.csv?s='
        Yesterday_Date = datetime.datetime(int(CurrentDate[0]),int(CurrentDate[1]),int(CurrentDate[2])-1)
        Previous_Date = datetime.datetime.strptime(prev_date,'%Y-%m-%d')


        #Create URL to fetch price changes
        file = BasePage + Ticker +'&d='+ str(int(current_date[1])-1)+'&e='+str(current_date[2])+'&f='+str(current_date[0])+'&g=d&a='+str(self.Previous_Month-1)+'&b='+ str(self.Previous_Day) + '&c=' + str(self.Previous_Year) + '&ignore=.csv'
        file_object = urllib.urlopen(file)
        pricereader = csv.DictReader(file_object)

        z = 0
        pricedict = {}

        #Read CSV, take first line as current price, search for previous date string to find previous price
        for row in pricereader:
            try:
                pricedict[datetime.datetime.strptime(row['Date'],'%Y-%m-%d')] = row['Adj Close']
            except KeyError:
                pass
        try:
            CurrentPrice = Decimal(pricedict[Yesterday_Date])
        except KeyError:
            pass
        try:
            PreviousPrice = Decimal(pricedict[Previous_Date])
        except KeyError:
            pass

        try:
            Percent_change = round(Decimal(((CurrentPrice - PreviousPrice)/PreviousPrice)*100),2)
            return Percent_change
        except UnboundLocalError:
            print 'Previous Price not found'

exchng = raw_input('Enter Exchange [caps]')


ExchangeDict = {'NYSE': '%5ENYA','TSX': '%5EGSPTSE'}

#Required for login:
#usr = 
#pswd = 
#hst = 
#hst = 
#dtb = 



#Declare 2d list to store daily performance
daily_tickers = []
daily_performance = []
performance = []
index = []
#Connect to Database
cnx = mysql.connector.connect(user=usr, password=pswd,host=hst,database=dtb)
#Create Cursor
cursor = cnx.cursor()

#Show Tables
t = cursor.execute("SHOW TABLES")
#Fetch Tables Data
data = cursor.fetchall()

#Loop through each table(day), append data to daily results ticker performance
for table in data:

    sql = "SELECT * FROM %s WHERE 1" %(table)
    response = cursor.execute(sql)
    table_data = cursor.fetchall()

    local_tickers = []

    CurrentDate = str(datetime.date.today()).split('-')
    data_date = str(table).split("'")
    ref_date = (data_date[1]).split("_")
    ref_date = [int(ref_date[0]),int(ref_date[1]),int(ref_date[2])]

    instant = historical_pricing()
    prev_date = instant.DateAdjustment(ref_date)
    CompanyPerformance = 0
    print prev_date

    for row in table_data:

        local_tickers.append(row[0])
        Ticker = row[0]

        price_change = instant.PriceChange(Ticker,CurrentDate,prev_date)
        try:
            CompanyPerformance += price_change
        except TypeError:
                break

    SetPerformance = Decimal(CompanyPerformance / 25)
    IndexPerformance = (instant.PriceChange(ExchangeDict[exchng],CurrentDate,prev_date))


    if SetPerformance != 0:
        performance.append(round(SetPerformance,3))
    daily_tickers.append(local_tickers)
    if IndexPerformance !=0:
        try:
            index.append(round(Decimal(IndexPerformance),3))
        except TypeError:
            continue

print performance
print index



