def update():
    test_append = str(request.form['excel_folder'])
    print(test_append)
    teacher_name = str(session.get('user'))
    print(teacher_name)
    excel_dir = APP_ROOT + "/excel/" + test_append + "/" + teacher_name + "/"
    print(excel_dir)
    for file in request.files.getlist("updated_excel"):
        print(file)
        filename = file.filename
        print(filename)
        destination = "/".join([excel_dir,filename])
        print(destination)
        file.save(destination)
    return render_template("excel.html",msg="updated successfully")