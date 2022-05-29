app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
print(APP_ROOT)

conn = MySQLdb.connect(host="localhost",user="root",password="Arasii@5670",db="login_info")

@app.route('/')
def index():
	return render_template("index.html",title="Admin Login")
@app.after_request
def set_response_headers(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/login',methods=['POST'])
def login():
	user = str(request.form["user"])
	paswd = str(request.form["password"])
	cursor = conn.cursor()
	result = cursor.execute("SELECT * from admin_login where binary username=%s and binary password=%s",[user,paswd])
	if(result==1):
		return render_template("task.html")
	else:
		return render_template("index.html",title="Admin Login",msg="The username or password is incorrect")


@app.route('/register_teacher',methods=['POST'])
def register_teacher():
	return render_template("signup.html",title="SignUp")
@app.after_request
def set_response_headers(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response


@app.route('/student',methods=['POST'])
def file_upload():
	return render_template("upload.html")


@app.route('/signup_teacher',methods=['POST'])
def signup():
	user = str(request.form["user"])
	paswd = str(request.form["password"])
	email = str(request.form["email"])
	cursor = conn.cursor()
	result = cursor.execute("SELECT * from teacher_login where binary username=%s",[user])
	print (result)
	if(result == 1):
		return render_template("signup.html",title="SignUp",uname=user,msg="already present")
	cursor.execute("INSERT INTO teacher_login (username,password,email) VALUES(%s, %s, %s)",(user,paswd,email))
	conn.commit()
	return render_template("signup.html",title="SignUp",msg="successfully signup",uname=user) 


@app.route('/signup_student',methods=['POST'])
def signup_student():
	user = str(request.form["student_name"])
	email = str(request.form["student_email"])
	roll_id = str(request.form["roll_id"])
	email1 = str(request.form["parent_email"])
	cursor = conn.cursor()
	result = cursor.execute("SELECT * from student_login where binary roll_id=%s",[roll_id])
	print (result)
	if(result == 1):
		return render_template("upload.html",uname=user,msg=" already present")
	cursor.execute("INSERT INTO student_login (username,student_email,parent_email,roll_id) VALUES(%s, %s, %s, %s)",(user,email,email1,roll_id))
	conn.commit()
	return render_template("upload.html",uname=user,msg=" successfully signup")


@app.route("/upload", methods=['POST']) 
def upload():
	target = os.path.join(APP_ROOT,"train/")
	if not os.path.isdir(target):
		os.mkdir(target)
	classfolder = str(request.form['class_folder'])
	session['classfolder'] = classfolder
	target1 = os.path.join(target,str(request.form["class_folder"])+"/")
	session['target1']=target1
	print(target1)
	model = os.path.join(APP_ROOT,"model/")
	if not os.path.isdir(model):
		os.mkdir(model)
	classname = str(request.form['class_folder']+"/")
	model = os.path.join(model,classname)
	if not os.path.isdir(model):
		os.mkdir(model)
	session['model']=model
	session['classname'] = classname
	if not os.path.isdir(target1):
		os.mkdir(target1)
	id_folder = str(request.form["id_folder"])
	session['id_folder']= id_folder
	target2 = os.path.join(target1,id_folder+"/")
	if not os.path.isdir(target2):
		os.mkdir(target2)
	target3 = os.path.join(target2,id_folder+"/")
	if not os.path.isdir(target3):
		os.mkdir(target3)
	for file in request.files.getlist("file"):
		print(file)
		filename = file.filename
		destination = "/".join([target3,filename])
		print(destination)
		file.save(destination)
	return call_train()