from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/')
def index():
    if 'agreement_accepted' not in session:
        return redirect(url_for('agreement'))
    return render_template('index.html')

@app.route('/model_description')
def model_description():
    return render_template('model_description.html')

@app.route('/terms')
def terms():
    return render_template('terms.html')

@app.route('/agreement', methods=['GET', 'POST'])
def agreement():
    if request.method == 'POST':
        session['agreement_accepted'] = True  # Запоминаем согласие пользователя
        return redirect(url_for('index'))
    return render_template('agreement.html')

@app.route('/basic', methods=['GET', 'POST'])
def basic():
    if request.method == 'POST':
        x =int(request.form.get('type', 0))
        size = float(request.form.get('size',1))
        mas =[[2.4,1.05,2.5,0.38],[3.0,1.12,2.5,0.35],[3.6,1.2,2.5,0.32]]
        pm = round(mas[x][0]*size**mas[x][1],2)
        tm = round(mas[x][2]*pm**mas[x][3],2)
        n =round(pm/tm,2)
        return render_template('result.html', level="Basic COCOMO", pm=pm, tm=tm, n =n)
    return render_template('basic.html')

@app.route('/intermediate', methods=['GET', 'POST'])
def intermediate():
    if request.method == 'POST':
        size = float(request.form.get('size',1))
        type = int(request.form.get('type', 0))
        mas = [[3.2, 1.05, 2.5, 0.38], [3.0, 1.12, 2.5, 0.35], [2.8, 1.2, 2.5, 0.32]]
        eaf =float(request.form.get('rebiabiliry',1))*float(request.form.get('db',1))*float(request.form.get('complexity',1))\
             *float(request.form.get('speed',1))*float(request.form.get('memory',1))*float(request.form.get('vm',1))\
             *float(request.form.get('time',1))*float(request.form.get('askills',1))*float(request.form.get('experience',1))\
             *float(request.form.get('poskills',1))*float(request.form.get('vmexperience',1))*float(request.form.get('clexperience',1))\
             *float(request.form.get('method',1))*float(request.form.get('tool',1))*float(request.form.get('timetable',1))
        pm = round(eaf*mas[type][0] * size ** mas[type][1], 2)
        tm = round(mas[type][2] * pm ** mas[type][3],2)
        n = round(pm / tm, 2)
        return render_template('result.html', level="Intermediate COCOMO", pm=pm, tm=tm, n =n)
    return render_template('intermediate.html')



@app.route('/detailed', methods=['GET', 'POST'])
def detailed():
    if request.method == 'POST':
        a =2.45
        size = float(request.form.get('size', 1))
        e = 0.91 + 0.01 * (float(request.form.get('prec', 3.72)) + float(request.form.get('flex', 3.04)) + float( request.form.get('resl', 4.24))\
            + float(request.form.get('team', 3.29)) + float(request.form.get('pmat', 4.68)))

        eafns =float(request.form.get('acap', 1.0))*float(request.form.get('aexp', 1.0))*float(request.form.get('pcap', 1.0))\
            *float(request.form.get('pcon', 1.0))*float(request.form.get('pexp', 1.0))*float(request.form.get('ltex', 1.0))\
            *float(request.form.get('rely', 1.0))*float(request.form.get('data', 1.0))*float(request.form.get('cplx', 1.0))\
            *float(request.form.get('ruse', 1.0))*float(request.form.get('docu', 1.0))*float(request.form.get('time', 1.0))\
            *float(request.form.get('stor', 1.0))*float(request.form.get('pvol', 1.0))*float(request.form.get('tool', 1.0))\
            *float(request.form.get('site', 1.0))
        sced = float(request.form.get('sced', 1.0))
        eaf = eafns * sced
        pm = round(eaf * a*size**e,2)
        pmns = eafns * a*size**e
        tm = round(sced * 3.67  * pmns ** (0.28 + 0.2 * (e - 0.91)),2)
        n = round(pm / tm, 2)
        return render_template('result.html', level="Детальный COCOMO II", pm=pm, tm=tm, n =n)
    return render_template('detailed.html')

@app.route('/preliminary', methods=['GET', 'POST'])
def preliminary():
    if request.method == 'POST':
        a =2.94
        size = float(request.form.get('size', 1))
        e = 0.91 + 0.01 * (float(request.form.get('prec', 3.72)) + float(request.form.get('flex', 3.04)) + float(request.form.get('resl', 4.24)) \
            + float(request.form.get('team', 3.29)) + float(request.form.get('pmat', 4.68)))
        eafns = float(request.form.get('pers', 1.0))*float(request.form.get('prex', 1.0))*float(request.form.get('pcpx', 1.0))\
            *float(request.form.get('ruse', 1.0))*float(request.form.get('pdif', 1.0))*float(request.form.get('fcil', 1.0))
        sced = float(request.form.get('sced', 1.0))
        eaf = eafns * sced
        pm = round(eaf * a * size ** e, 2)
        pmns = eafns * a * size ** e
        tm = round(sced * 3.67  * pmns ** (0.28 + 0.2 * (e - 0.91)),2)
        n = round(pm / tm, 2)
        return render_template('result.html', level="Предварительный COCOMO II", pm=pm, tm=tm, n =n)
    return render_template('preliminary.html')

if __name__ == '__main__':
    app.run(debug=True)
