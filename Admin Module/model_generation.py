def call_train():
	id_folder = str(session.get('id_folder'))
	model=str(session.get('model'))
	if not os.path.isdir(model + id_folder):
		os.mkdir(model + id_folder)
	model = model + id_folder + "/"
	model = model + "model"
	target1=str(session.get('target1'))
	print(id_folder)
	print (target1)
	target1 = target1 +id_folder 
	print(target1)
	print(model)
	return train(train_dir=target1,model_save_path=model)