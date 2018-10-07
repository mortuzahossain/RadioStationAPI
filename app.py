from flask import Flask
from flask_restplus import Api,Resource,fields
import json

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
class Language(Resource):
    def get(self):
        return counrtyAvailable()
    
    @api.expect(country)
    def post(self):
        return findCounrty(api.payload['countryName'])




if __name__ == '__main__':
    app.run(debug=True)

