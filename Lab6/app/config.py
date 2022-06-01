import os

ECRET_KEY = 'bc19682532d598bee940dfd34c91380ddde73580d16de643cce645b8cb100384'
SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://std_1611_lab6:stepbrohelpme@std-mysql.ist.mospolytech.ru/std_1611_lab6'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = False

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'media', 'images')