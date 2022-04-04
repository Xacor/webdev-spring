from flask import Flask, render_template, request, make_response
import operator as op

app = Flask(__name__)
application = app

OPERATIONS = {'+': op.add, '-': op.sub, '*': op.mul, '/': op.truediv}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/args')
def args():
    return render_template('args.html')


@app.route('/headers')
def headers():
    return render_template('headers.html')


@app.route('/cookies')
def cookies():
    response = make_response(render_template('cookies.html'))
    if request.cookies.get('cookie') is None:
        response.set_cookie('cookie', 'value')
    else:
        response.delete_cookie('cookie', 'value')
    return response


@app.route('/form', methods=['GET', 'POST'])
def form():
    return render_template('form.html')


@app.route('/calc', methods=['GET', 'POST'])
def calc():
    result = None
    if request.method == 'POST':
        error_msg = ''
        try:
            operand1 = float(request.form.get('operand1'))
            operand2 = float(request.form.get('operand2'))
            operation = request.form.get('operation')
            result = OPERATIONS[operation](operand1, operand2)
        except ValueError:
            error_msg = 'Нужно вводить только цифры'
        except ZeroDivisionError:
            error_msg = 'Деление на ноль'
    return render_template('calc.html', operations=OPERATIONS, result=result, error_msg=error_msg)


@app.route('/phone', methods=['GET', 'POST'])
def phone():
    error_msg = ''
    input_class = ''
    phone = request.form.get('phone')
    if request.method == 'POST':
        error_msg = ''
        input_class = ''

        digits = sum(c.isdigit() for c in phone)

        if (phone.startswith('+7') or phone.startswith('8')) and digits == 11 or not (phone.startswith('+7') or phone.startswith('8')) and digits == 10:
            input_class = 'is-valid'
            if phone.startswith('+7'):
                phone = phone.replace('+7', '8')
            elif not phone.startswith('8'):
                phone = '8.' + phone

            phone = phone.replace(' ', '').replace(
                '.', '').replace('(', '').replace(')', '').replace('-', '')
            phone = phone[0:1] + '-' + phone[1:4] + '-' + \
                phone[4:7] + '-' + phone[7:9] + '-' + phone[9:]

        elif any([c for c in phone if not c.isdigit() and c not in [' ', '(', ')', '-', '.', '+']]):
            error_msg = 'Недопустимый ввод. В номере телефона встречаются недопустимые символы.'
            input_class = 'is-invalid'
            phone = ''
        else:
            error_msg = 'Недопустимый ввод. Неверное количество цифр.'
            input_class = 'is-invalid'
            phone = ''

        print(phone)
    return render_template('phone.html', input_class=input_class, error_msg=error_msg, phone=phone)
