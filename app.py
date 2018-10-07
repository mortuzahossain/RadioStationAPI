from flask import Flask
from flask_restplus import Api,Resource,fields


app = Flask(__name__)
api = Api(app)

# For sql connection
import sqlite3 as sql
con = sql.connect("database/mydb.db",check_same_thread=False)
cur = con.cursor()
con.row_factory = sql.Row

def counrtyAvailable():
    global cur
    return cur.execute("SELECT DISTINCT countryname FROM radio").fetchall()

def findCounrty(countryName):
    global cur
    searchStr = "SELECT DISTINCT countryname FROM radio WHERE countryname = '%s'" % countryName
    return len(cur.execute(searchStr).fetchall()) > 0
    


country = api.model('Country',{'countryName':fields.String('Provide Country Name To Search For')})
@api.route('/SearchCountry')
class SearchCountry(Resource):
    def get(self):
        return counrtyAvailable()
    
    @api.expect(country)
    def post(self):
        return findCounrty(api.payload['countryName'])


# Geting Countries radio station list

def getStation(countryName):
    global cur
    searchStr = "SELECT id,station,img,url FROM radio WHERE countryname = '%s'" % countryName
    return cur.execute(searchStr).fetchall()

@api.route('/RadioStations')
class RadioStation(Resource):
    @api.expect(country)
    def post(self):
        countryName = api.payload['countryName']
        return getStation(countryName)


# Update Radio Station
def updateStation(_id,name,image,url):
    global cur,con
    sql = "UPDATE radio SET station = '%s',img = '%s',url = '%s' WHERE id = %d"%(name,image,url,_id)
    cur.execute(sql)
    try:
        con.commit()
        return True
    except:
        return False

stationDetails = api.model('StationDetails',
    {
        'id':fields.Integer('ID'),
        'stationName':fields.String('Provide Station Name'),
        'imageURL':fields.String('Thumbnail Image URL'),
        'streamURL':fields.String('Valid Stream URL')
    })
@api.route('/UpdateRadioStation')
class UpdateRadioStation(Resource):
    @api.expect(stationDetails)
    def post(self):
        _id = api.payload['id']
        _stationName = api.payload['stationName']
        _imageURL = api.payload['imageURL']
        _streamURL = api.payload['streamURL']

        return updateStation(_id,_stationName,_imageURL,_streamURL)


# All Stations
def allStations():
    global cur
    sql = "SELECT * FROM radio"
    return cur.execute(sql).fetchall()

@api.route('/ShowAll')
class ShowAll(Resource):
    def get(self):
        return allStations()

# if __name__ == '__main__':
#     app.run(debug=True)

