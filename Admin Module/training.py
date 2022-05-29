def train(train_dir, model_save_path = "", n_neighbors = None, knn_algo = 'ball_tree', verbose=True):
    id_folder=str(session.get('id_folder'))
    X = []
    y = []
    z = 0
    for class_dir in listdir(train_dir):
        if not isdir(join(train_dir, class_dir)):
            continue
        for img_path in image_files_in_folder(join(train_dir, class_dir)):
            image = face_recognition.load_image_file(img_path)
            faces_bboxes = face_locations(image)
            if len(faces_bboxes) != 1:
                if verbose:
                    print("image {} not fit for training: {}".format(img_path, "didn't find a face" if len(faces_bboxes) < 1 else "found more than one face"))
                    os.remove(img_path)
                    z = z + 1
                continue
            X.append(face_recognition.face_encodings(image, known_face_locations=faces_bboxes)[0])
            y.append(class_dir)
    print(listdir(train_dir+"/"+id_folder))
    train_dir_f = listdir(train_dir+"/"+id_folder)
    for i in range(len(train_dir_f)):
    	if(train_dir_f[i].startswith('.')):
    		os.remove(train_dir+"/"+id_folder+"/"+train_dir_f[i])

    print(listdir(train_dir+"/"+id_folder))
    
    if(listdir(train_dir+"/"+id_folder)==[]):
    	return render_template("upload.html",msg1="training data empty, upload again")
    elif(z >= 1):
    	return render_template("upload.html",msg1="Data trained for "+id_folder+", But one of the image not fit for trainning")
    if n_neighbors is None:
        n_neighbors = int(round(sqrt(len(X))))
        if verbose:
            print("Chose n_neighbors automatically as:", n_neighbors)

    knn_clf = neighbors.KNeighborsClassifier(n_neighbors=n_neighbors, algorithm=knn_algo, weights='distance')
    knn_clf.fit(X, y)

    if model_save_path != "":
        with open(model_save_path, 'wb') as f:
            pickle.dump(knn_clf, f)

    return render_template("upload.html",msg1="Data trained for "+ id_folder)