def match():
    destination = str(session.get('destination'))
    print(destination)
    if os.path.isfile(destination):
        test_append = str(session.get('test_append'))
        session['test_append'] = test_append
        id_folder = str(session.get('id_folder'))

        train_dir = APP_ROOT1[0]+"admin_site/train/"+ test_append
        try:
            model = APP_ROOT1[0]+"admin_site/model/"+test_append+"/" + id_folder + "/" +"model"
            print(model)
            return predict1(model)
        except FileNotFoundError:
            os.remove(APP_ROOT1[0]+"teachers_site/image.jpeg")
            return render_template("upload.html",msg="trained model not present for " + test_append + ": "+id_folder)
        

def predict(X_img_path, knn_clf = None, model_save_path ="", DIST_THRESH = .45):
    if knn_clf is None and model_save_path == "":
        raise Exception("must supply knn classifier either thourgh knn_clf or model_save_path")

    if knn_clf is None:
        with open(model_save_path, 'rb') as f:
            knn_clf = pickle.load(f)

    X_img = face_recognition.load_image_file(X_img_path)
    X_faces_loc = face_locations(X_img)
    if len(X_faces_loc) == 0:
        return []

    faces_encodings = face_recognition.face_encodings(X_img, known_face_locations=X_faces_loc)


    closest_distances = knn_clf.kneighbors(faces_encodings, n_neighbors=1)

    is_recognized = [closest_distances[0][i][0] <= DIST_THRESH for i in range(len(X_faces_loc))]
    

    return [(pred) if rec else ("unknown") for pred, rec in zip(knn_clf.predict(faces_encodings), is_recognized)]

def predict1(model):
    test_append = str(session.get('test_append'))
    test_dir = APP_ROOT1[0]+"teachers_site/test/" + test_append
    f_preds = []
    for img_path in listdir(test_dir):
        preds = predict(join(test_dir, img_path) ,model_save_path=model)
        f_preds.append(preds)
        print(f_preds)
    print(len(preds))
    print(len(f_preds))
    for i in range(len(f_preds)):
        if(f_preds[i]==[]):
            os.remove(APP_ROOT1[0]+"teachers_site/image.jpeg")
            return render_template("upload.html",msg="upload again, face not found")
        else:
            os.remove(APP_ROOT1[0]+"teachers_site/image.jpeg")
    if f_preds[0][0] == 'unknown':
        return render_template("upload.html",msg= "Student Not Matched")
    excel = os.path.join(APP_ROOT,"excel/")
    if not os.path.isdir(excel):
        os.mkdir(excel)
    excel1 = os.path.join(excel,test_append)
    if not os.path.isdir(excel1):
        os.mkdir(excel1)
    teacher_name = str(session.get('teacher_name'))
    excel2 = os.path.join(excel1,teacher_name)
    if not os.path.isdir(excel2):
        os.mkdir(excel2)
    session['excel2'] = excel2
    excel3 = excel2+"/"+date+'.xlsx'
    if not os.path.isfile(excel3):
        workbook = xlsxwriter.Workbook(excel2+"/"+date+'.xlsx')
        worksheet = workbook.add_worksheet()
        worksheet.set_column(0,0,20)
        worksheet.write('A1','Roll Id')
        f_preds.sort()
        row = 1
        col = 0
        print(f_preds[0][0], type(f_preds[0][0]))
        for i in range(len(f_preds)):
            for j in range(len(f_preds[i])):
                worksheet.write_string(row,col,f_preds[i][j])
                row += 1
        workbook.close()
        return render_template("upload.html",msg= f_preds[0][0] + " present")
    else:
        df = pd.read_excel(excel2+"/"+date+'.xlsx')
        writer = pd.ExcelWriter(excel2 + "/" + date+'.xlsx')
        df.to_excel(writer,sheet_name="Sheet1",index=False)
        workbook  = writer.book
        worksheet = writer.sheets['Sheet1']
        rows=df.shape[0]
        worksheet.write_string(rows+1,0,f_preds[0][0])
        writer.save()
        df = pd.read_excel(excel2+"/"+date+'.xlsx')
        df.drop_duplicates(['Roll Id'],keep='first',inplace=True)
        # result = df.sort_values("Roll Id")
        writer = pd.ExcelWriter(excel2 + "/" + date+'.xlsx')
        df.to_excel(writer,'Sheet1',index=False)
        workbook = writer.book
        worksheet = writer.sheets['Sheet1']
        worksheet.set_column(0,0,20)
        writer.save()
        return render_template("upload.html",msg= f_preds[0][0] + " present")