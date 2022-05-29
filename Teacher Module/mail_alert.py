def send_mail():
    test_append = str(request.form['folder_name'])
    teacher_name = str(session.get('user'))
    excel_dir = APP_ROOT+"/excel/"+test_append+"/"+teacher_name+"/"
    excel_date = request.form['fname']
    time = request.form['ftime']
    time = time[:2]
    final_send = glob(excel_dir + "/" + excel_date+ "@" + time +"*.xlsx")[0]
    print(final_send)
    df = pd.read_excel(final_send)
    roll_id = list(df['Roll Id'])
    print(type(roll_id))
    print(roll_id)
    cursor = conn.cursor()
    for i in range(len(roll_id)):
        cursor.execute("SELECT student_email,parent_email from student_login where binary roll_id=%s",[roll_id[i]])
        email = list(cursor.fetchone())
        print(type(email[1]))
        print(email[0])
        print(email[1])
        msg = Message('GCT-IT Attendance',recipients= [email[0],email[1]])
        msg.body = "Hi.. " + str(roll_id[i]) + " is present for the lecture of " + "Prof. " +str(teacher_name.split('.',1)[0]) + ", which is held on " + excel_date + "@" + time + "hrs"
        msg.html = "Hi.. " + str(roll_id[i]) + " is present for the lecture of " + "Prof. " +str(teacher_name .split('.',1)[0])+ ", which is held on " + excel_date + "@" + time + "hrs"
        mail.send(msg)
    return "<h1>mail sent<h1>"