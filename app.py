import pickle
import numpy as np
from flask import Flask, render_template,request 
import requests
from bs4 import BeautifulSoup

def do(s,s1):
    r = requests.get(s)

    # Parsing the HTML
    soup = BeautifulSoup(r.content, 'html.parser')
    table = soup.find('table',class_=s1)
    #print(table)
    #df = pd.DataFrame(columns=['Name','Price'])
    for row in table.find_all('tr'):
        columns= row.find_all('td')
        if((columns !=[])and(len(columns)>2)):
            name= columns[1].text.strip()
            price= columns[2].text.strip()
            dic[name]=price


app= Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')



@app.route('/page1',methods=['POST','GET'])
def page1():
    return render_template('page1.html')

@app.route('/price',methods=['POST','GET'])
def price():

    return render_template('price.html')

@app.route('/select_value',methods=['POST'])
def select_value():
    do('https://www.livechennai.com/Vegetable_price_chennai.asp','table-price1')
    do('https://www.livechennai.com/Rice_dal_price_chennai.asp','rice')
    do('https://www.livechennai.com/spices_plantation_crops_pricelist.asp','rice')
    sl= request.form['veges']
    if(sl in dic):
        print(sl,dic[sl])
        p1=dic[sl]
    s2= request.form['dals']
    if(s2 in dic):
        print(s2,dic[s2])
        p2=dic[s2]
    s3= request.form['spices']
    if(s3 in dic):
        print(s3,dic[s3])
        p3=dic[s3]

    return render_template('price.html',veg=p1,dal=p2,spice=p3) 


@app.route('/get_value',methods=['POST'])
def get_value():
    n = request.form['nitro']
    p = request.form['phos']
    k= request.form['npk']
    rf = request.form['rain']
    t = 28
    h= 70.3
    ph = 7.0
    print(n,p,k)
    model = pickle.load(open('model.pkl','rb'))
    #83 45 60 150.9
    dat = np.array([[n,p,k, t,h,ph, rf]])
    ans     = model.predict(dat)
    print(ans)
    return render_template('result.html',n=n,p=p,k=k,t=t,h=h,ph=ph,rf=rf,a=ans)
if __name__ == '__main__':
    dic ={}
    app.run(debug=True)

