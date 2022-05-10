import re

def validate_password(password: str):
    #(?=.{8,128}$)(?=.*[A-ZА-Я])(?=.*[0-9])[a-zA-Zа-яА-Я0-9~!?@#$%^&*_\-+()[\]{}></\\|\"\'.,:;]+
    lenp = re.compile(r'.{8,128}')
    uppercharp = re.compile(r'.*[A-ZА-Я]')
    digitp = re.compile(r'.*[0-9]')
    symbolsp = re.compile(r'[a-zA-Zа-яА-Я0-9~!?@#$%^&*\_\-+()[\]{}></\\|\"\'.,:;]+')
    msg = 'Ok'
    if not lenp.match(password):
        msg = 'Пароль должен быть длиной от 8 до 128 символов!' 
    
    if not uppercharp.match(password): 
        msg = 'В пароле должна быть хотя бы одна заглавная буква!'
    
    if not digitp.match(password):
        msg = 'В пароле должна быть хотя бы одна цифра!'

    if not symbolsp.match(password):
        msg = 'В пароле допускаются латинские и кирилические буквы, цифры и символы ~ ! ? @ # $ % ^ & * _ - + ( ) [ ] { } > < / \ | " \' . , : ;'

    return msg

print(validate_password('AAAAAAAAAAA1]'))