WTF_CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

# Upload Configuration
#
UPLOAD_FOLDER = 'app/upload/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
# Default max 2mb filesize
MAX_CONTENT_LENGTH = 2 * 1024 * 1024
