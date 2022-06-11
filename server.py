from flask import Flask,request,jsonify
import numpy as np
from flaskext.mysql import MySQL


app = Flask(__name__)
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']='root1234'
app.config['MYSQL_DATABASE_DB']='smartparking'
app.config['MYSQL_DATABASE_HOST']='localhost'
mysql=MySQL(app)
con=mysql.connect()

@app.route('/pred/slot', methods=['GET'])
def pred_slot():
	token=request.get_json()['token']
	if(token!='atharva123'):
		return 'invalid token'
	start=request.get_json()['start']
	end=request.get_json()['end']
	cur=con.cursor()
	cur.execute('SELECT data FROM slot')
	data=list(cur.fetchall())
	cur.close()
	x1=[]
	for i in range(len(data)):
		data[i]=data[i][0].split(',')
		for j in range(len(data[i])-1):
			data[i][j]=int(data[i][j])
		data[i][-1]=float(data[i][-1])
		#x1.append(data[i][-1])
	d=[]
	for i in data:
		if(i[-1]>=start and i[-1]<end):
			d.append(i)
			x1.append(i[-1])
	x=np.array(x1)

	#print(data)
	y=[]
	for i in range(len(d[0])-1):
		t=[]
		for j in d:
			t.append(j[i])
		y.append(t)
	#print(y,x1)
	b=[]
	n=np.size(x)
	m_x=np.mean(x)
	for i in y:
		i=np.array(i)
		m_y=np.mean(i)
		SS_xy=np.sum(i*x) - n*m_y*m_x
		SS_xx = np.sum(x*x) - n*m_x*m_x
		b_1 = SS_xy / SS_xx
		b_0 = m_y - b_1*m_x
		b.append([b_0,b_1])
	return(jsonify([x1,y,b]))

@app.route('/pred/cust', methods=['GET'])
def pred_cust():
	token=request.get_json()['token']
	if(token!='atharva123'):
		return 'invalid token'
	start=request.get_json()['start']
	end=request.get_json()['end']
	cur=con.cursor()
	cur.execute('SELECT data FROM cust')
	data=list(cur.fetchall())
	cur.close()
	for i in range(len(data)):
		data[i]=data[i][0].split(',')
		data[i][-1]=float(data[i][-1])
	c=[]
	t=[]
	for i in data:
		if(i[-1]>=start and i[-1]<end):
			c.append(i[0])
			t.append(i[-1])
	#print(data)
	c1=list(set(c))
	t1=[]
	for i in c1:
		t2=0
		t3=0
		s=0
		c2=0
		for j in range(len(c)):
			if(i==c[j]):
				if(c2==0):
					t2=t[j]
					c2+=1
				elif(c2>0):
					t3=t[j]
					s=s+t3-t2
					t2=0
					t3=0
					c2=0
		t1.append(s)
	return(jsonify([c1,t1]))

@app.route('/customer', methods=['POST'])
def cust():
	token=request.get_json()['token']
	if(token!='atharva123'):
		return 'invalid token'
	print(request.get_json('customer')['customer'])
	cur=con.cursor()
	cur.execute("INSERT INTO cust(data) VALUES(%s)",(request.get_json('customer')['customer']))
	con.commit()
	cur.close()
	return 'ok'

@app.route('/slot', methods=['POST'])
def slot():
	token=request.get_json()['token']
	if(token!='atharva123'):
		return 'invalid token'
	print(request.get_json('slot')['slot'])
	cur=con.cursor()
	cur.execute("INSERT INTO slot(data) VALUES(%s)",(request.get_json('slot')['slot']))
	con.commit()
	cur.close()
	return 'ok'


if __name__ =='__main__':
	app.run(debug = True,host='0.0.0.0')