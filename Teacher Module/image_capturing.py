def upload():
    if not os.path.isfile(APP_ROOT+"/image.jpeg"):
        return render_template("upload.html",msg="spoof detected")
    id_folder = str(request.form['id_folder'])
    session['id_folder']= id_folder
    target = os.path.join(APP_ROOT,"test/")
    if not os.path.isdir(target):
        os.mkdir(target)
    target1 = os.path.join(target,str(request.form["folder_name"])+"/")
    test_append = str(request.form["folder_name"])
    session['test_append']= test_append
    print(target1)
    if not os.path.isdir(target1):
        os.mkdir(target1)
    shutil.copyfile(APP_ROOT+"/"+"image.jpeg",target1+"image.jpeg")
    destination = APP_ROOT + "/" + "test/" + test_append + "/" + "image.jpeg"
    
    session['destination'] = destination
    teacher_name = str(session.get('user'))
    session['teacher_name'] = teacher_name
    #return render_template("upload.html",msg="uploaded successfully")
    return match()