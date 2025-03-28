
from flask import Flask,render_template,request,redirect,url_for, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SubmitField
from wtforms.validators import DataRequired
from flask_mysqldb import MySQL



app = Flask(__name__)

app.config['SECRET_KEY'] = ""



app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='teste_api'
#app.config['MYSQL_CURSORCLASS']= 'DictCursor'

mysql = MySQL(app)

#Formulario FLask-WTF
class AlunoForm(FlaskForm):
	name = StringField('Name',validators=[DataRequired()])
	birth = DateField('BirthDay',format="%Y-%m-%d",validators=[DataRequired()])
	submit = SubmitField('Add Aluno')

@app.route('/',methods=['GET','POST'])
def index():
	form = AlunoForm()
	if form.validate_on_submit():
		name = form.name.data
		birth = form.birth.data

		cur = mysql.connection.cursor()
		cur.execute("insert into alunos (name,birth) values (%s, %s)",(name,birth))
		mysql.connection.commit()
		cur.close()

		return redirect(url_for('index'))

	cur = mysql.connection.cursor()
	cur.execute("select * from alunos")
	alunos = cur.fetchall()
	cur.close()
	return render_template('index.html',form=form, alunos=alunos)



@app.route('/users')
@app.route('/users/<string:nomealuno>',methods=['GET'])
def get_users(nomealuno=None):
	cur = mysql.connection.cursor()
	if nomealuno:
		query = f"select * from alunos where name like '%{nomealuno}%'"

	else:
		query = f"select * from alunos"

	cur.execute(query)
	alunos = cur.fetchall()
	cur.close()
	return jsonify(alunos)



@app.route('/delete/<int:id>')
def delete_user(id):
	cur = mysql.connection.cursor()
	cur.execute("delete from alunos where id =%s",(id,))
	mysql.connection.commit()
	cur.close()
	return redirect(url_for('index'))




if __name__== '__main__':
	app.run(host='0.0.0.0', port=5000, debug=True)
