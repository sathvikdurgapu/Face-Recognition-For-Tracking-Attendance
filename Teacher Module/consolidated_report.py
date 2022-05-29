def calculate():
    test_append = str(request.form['final_class'])
    print(test_append)
    teacher_name = str(session.get('user'))
    print(teacher_name)
    excel_root = APP_ROOT + "/excel/" + test_append + "/" + teacher_name + "/"
    print(excel_root)
    excel_names = os.listdir(excel_root)
    print(excel_names) 
    for i in range(len(excel_names)):
        if excel_names[i].startswith("."):
            os.remove(excel_root+excel_names[i])
        else:
            if os.path.isdir(excel_root+excel_names[i]):
                shutil.rmtree(excel_root+excel_names[i], ignore_errors=False, onerror=None)
    excel_names = os.listdir(excel_root)

    if(excel_names==[]):
        return render_template("excel.html",msg1="No excel files found")

    for i in range(len(excel_names)):
        excel_names[i] = excel_root + excel_names[i]
    print(type(excel_names))
    # read them in
    excels = [pd.ExcelFile(name) for name in excel_names]
    # turn them into dataframes
    frames = [x.parse(x.sheet_names[0], header=None,index_col=None) for x in excels]
    # delete the first row for all frames except the first
    # i.e. remove the header row -- assumes it's the first
    frames[1:] = [df[1:] for df in frames[1:]]
    # concatenate them..
    combined = pd.concat(frames)
    if not os.path.isdir(excel_root+"final/"):
        os.mkdir(excel_root + "final/")
    final = excel_root + "final/"
    print(final)
    # write it out
    combined.to_excel(final+"final.xlsx", header=False, index=False)

    # below code is to find actual repetative blocks

    workbook = pd.ExcelFile(final+"final.xlsx")
    df = workbook.parse('Sheet1')
    sample_data = df['Roll Id'].tolist()
    print (sample_data)
    #a dict that will store the poll results
    results = {}
    for response in sample_data:
        results[response] = results.setdefault(response, 0) + 1
    finaldf = (pd.DataFrame(list(results.items()), columns=['Roll Id', 'Total presenty']))
    #finaldf = finaldf.sort_values("Roll Id")
    print (finaldf)
    writer = pd.ExcelWriter(final+"final.xlsx")
    finaldf.to_excel(writer,'Sheet1',index=False)
    workbook  = writer.book
    worksheet = writer.sheets['Sheet1']
    worksheet.set_column(0,1,20)
    writer.save()
    final = final + "final.xlsx"
    session['final']=final
    final = final[91:]
    return viewfinal(final)

def viewfinal(final):
    test_append = str(session.get('test_append'))
    final_path = str(session.get('final'))
    df = pd.read_excel(final_path)
    df.index += 1
    return render_template("files.html",msg=final,course=test_append,df=df)