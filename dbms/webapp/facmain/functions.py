def handle_upload_file(assignment_file):
    with open('webapp/webapp/static/upload/'+assignment_file,'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)