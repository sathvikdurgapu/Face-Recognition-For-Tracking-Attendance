def view():
    test_append = str(request.form['folder_name'])
    session['test_append']=test_append
    teacher_name = str(session.get('user'))
    excel_dir = APP_ROOT+"/excel/"+test_append+"/"+teacher_name+"/"
    excel_date = request.form['fname']
    time = request.form['ftime']
    time = time[:2]
    print(time)
    final_excel=glob(excel_dir + "/" + excel_date+ "@" + time +"*.xlsx")[0]
    print(final_excel)

    df = pd.read_excel(final_excel)
    df.index += 1
    return render_template("files.html",msg=final_excel,df=df,date=excel_date+"@"+time+"hrs")