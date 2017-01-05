from bottle import route, run, request, template, static_file
from lib import helper
import json, datetime, os

@route('/')
def home():
    return static_file('index.html', root='app/')

@route('/api/countries', method='GET')
def get_countires():
    res = helper.get_all_countries()
    return res

@route('/api/db', method='GET')
def get_databases():
    res = helper.get_all_dbs()
    return res

@route('/api/db/:v', method='GET')
def is_available(v):
    v = helper.clean(v).replace('/','').replace('\\','')
    dbs = json.loads(helper.get_all_dbs())
    dbnames = [db['dbname'].lower() for db in dbs]
    res = { 'available' : v.lower() not in dbnames }
    return json.dumps(res)

@route('/api/search/:v', method='GET')
def search(v):
    v = helper.clean(v).replace('/','').replace('\\','')
    res = helper.search(v)
    return res

@route('/api/generate_report/', method='POST')
def generate_report():
    since = request.forms.get('fromDate')
    since = since[:since[:since.find(':')].rfind(' ')]
    since = datetime.datetime.strptime(since,'%a %b %d %Y').strftime('%Y-%m-%d')
    until = request.forms.get('toDate')
    until = until[:until[:until.find(':')].rfind(' ')]
    until = datetime.datetime.strptime(until,'%a %b %d %Y').strftime('%Y-%m-%d')

    data = { 'COUNTRY' : request.forms.get('country'),
             'KEYWORD1': request.forms.get('keyword1'),
             'KEYWORD2': request.forms.get('keyword2'),
             'SINCE'   : since,
             'UNTIL'   : until,
             'DBName'  : request.forms.get('dbname'),
             'CACHE'   : 'TRUE',
             'PORT'    : '8000' }
    info = json.loads(is_available(request.forms.get('dbname')))
    print(info['available'])
    if info['available']==True:
        res = spwan_generation_sequence(data)
    else:
        res = json.dumps({'message':'database already in use !'})
    return str(res)

@route('/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='app/')

def spwan_generation_sequence(data):
    if not os.path.exists('./data/pickle/'+data['DBName']):
        os.mkdir('./data/pickle/'+data['DBName'])
    f = open('./data/pickle/'+data['DBName']+'/input.in','w')
    f.write(data['KEYWORD1']+'\n')
    f.write(data['KEYWORD2']+'\n')
    f.write(data['SINCE']+'\n')
    f.write(data['UNTIL']+'\n')
    f.write(data['DBName']+'\n')
    f.write(data['COUNTRY']+'\n')
    f.write(data['CACHE']+'\n')
    f.write(data['PORT']+'\n')
    f.close()
    retvalue = True
    try:
        path = './data/pickle/'+data['DBName']
        os.execv('./run.py',['./run.py', path])
    except Exception as e:
        print("Execution failed:", e)
        retvalue = json.dumps({'message':'something went wrong !'})
    return retvalue

run(host='160.153.128.6', port=8080, debug=True)
