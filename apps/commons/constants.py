BASE_URL ='/'
STUDENTS_LOGIN_URL ='/students/login/'
STUDENTS_REGISTER_URL ='/students/register/'
TEACHERS_LOGIN_URL = '/teachers/login/'

TEACHERS_ACTION = '/teachers/'
STUDENTS_ACTION = '/students/'

STATIC_URL = '/static/'
SKIP_AUTH_URL = [BASE_URL,
                STUDENTS_LOGIN_URL,
                STUDENTS_REGISTER_URL,
                TEACHERS_LOGIN_URL,
                 '/uploads',
                 '/favicon.ico']
