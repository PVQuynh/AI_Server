ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'wmv'}

def allowedFile(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
