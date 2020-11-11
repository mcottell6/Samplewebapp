from flask import Flask, render_template, request
import pymysql

def secondlower(tpl):
    return tpl[1].lower()

def third(tpl):
    return tpl[2]

app = Flask(__name__, static_url_path='/static')
hostdb = '' #host database ip goes here
dbuser = '' #mysql username
dbpass = '' #password
dbname = '' #name of database

@app.route('/')
def homepage():
    return render_template('home.html')

@app.route('/addthings')
def addthingpage():
    return render_template('entryform.html')

@app.route('/listthings', methods = ['POST','GET'])
def listthingspage():
    tconn = pymysql.connect(hostdb, dbuser, dbpass, dbname)
    tcurs = tconn.cursor()
    tcurs.execute('select * from thinglist where not number = 0')
    list = tcurs.fetchall()
    if request.method == 'POST':
        srt = request.form['sort']
        print(srt)
        if srt == 'idasc':
            list = sorted(list)
        elif srt == 'iddsc':
            list = sorted(list, reverse = True)
        elif srt == 'thasc':
            list = sorted(list, key = secondlower)
        elif srt == 'thdsc':
            list = sorted(list, key = secondlower, reverse = True)
        elif srt == 'noasc':
            list = sorted(list, key = third)
        elif srt == 'nodsc':
            list = sorted(list, key = third, reverse = True)
    return render_template('outputlist.html', db = list)

@app.route('/thanks', methods = ['POST','GET'])
def thankuser():
    if request.method == 'POST':
        thing = request.form['thing']
        #print('thing', thing)
        try: thno = int(request.form['thno'])
        except: thno = 1
        #print('thing number', thno)
        tconn = pymysql.connect(hostdb, dbuser, dbpass, dbname)
        tcurs = tconn.cursor()
        tcurs.execute('select name from thinglist where name = %(thing)s', {'thing': thing})
        list = tcurs.fetchall()
        if (thing,) in list:
            tcurs.execute('select number from thinglist where name = %(thing)s', {'thing': thing})
            oldno = tcurs.fetchall()[0][0]
            total = oldno + thno
            #print('total', total)
            tcurs.execute('update thinglist set number = %(total)s where name = %(thing)s', {'total': total, 'thing': thing})
        else:
            tcurs.execute('select id from thinglist')
            maxid = int(max(tcurs.fetchall())[0])
            tcurs.execute('insert into thinglist values (%(id)s, %(thing)s, %(thno)s)', {'id': maxid+1, 'thing': thing, 'thno':thno})
        tconn.commit()
        tconn.close()

    return render_template('thankyoupage.html')

if __name__ == '__main__':
   app.run(host = "0.0.0.0", port = "80" )
