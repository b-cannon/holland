from flask import Flask, flash, redirect, render_template, request, \
    session, url_for
from functools import wraps

app = Flask(__name__)
app.config.from_object('config')


def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to enter your name')
            return redirect(url_for('home'))
    return wrap

#removed method=get, post
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    #flash('Bye!')
    return redirect(url_for('home'))

@app.route('/', methods=['GET', 'POST'])
@app.route('/home/', methods=['GET', 'POST'])
def home():
    error = None
    if request.method == 'POST':
        if request.form['username']:
            session['logged_in'] = True
            session['username'] = request.form['username']
            return redirect(url_for('social'))
        else:
            error = 'You must enter your name'
    return render_template('home.html', error=error)

#*****************PAGES***************************
#@app.route('/home/', methods=['GET', 'POST'])
#@app.route('/home/<name>')
#@login_required
#def home():
#    name = session['username']
#    return render_template('home.html', name=name)

#Social page 1st
@app.route('/social/', methods=['GET', 'POST'])
@login_required
def social():
    return render_template('social.html')

#Enterprise page 2nd
@app.route('/enterprising/')
@login_required
def enterprising():
    return render_template('enterprising.html')

#Conventional page 3rd
@app.route('/conventional/')
@login_required
def conventional():
    return render_template('conventional.html')

#Realistic page 4th
@app.route('/realistic/')
@login_required
def realistic():
    return render_template('realistic.html')

#Investigative 5th
@app.route('/investigative/')
@login_required
def investigative():
    return render_template('investigative.html')

#Artistic 6th page
@app.route('/artistic/')
@login_required
def artistic():
    return render_template('artistic.html')

#*********************************************************

#*********************** ADD ATTRIBUTES TO SESSION*****************
#Social page 1st
@app.route('/add_social/', methods=['GET', 'POST'])
@login_required
def add_social():
    social_list = request.form.getlist('social_attr')
    i = 0
    for s in social_list:
        i += 1
    session['social'] = i
    return redirect(url_for('enterprising'))

#Enterprise page 2nd
@app.route('/add_enterprise/', methods=['GET', 'POST'])
@login_required
def add_enterprise():
    enterprise_list = request.form.getlist('enterprise_attr')
    i = 0
    for e in enterprise_list:
        i += 1
    session['enterprise'] = i
    return redirect(url_for('conventional'))

#Conventional page 3rd
@app.route('/add_conventional/', methods=['GET', 'POST'])
@login_required
def add_conventional():
    conventional_list = request.form.getlist('conventional_attr')
    i = 0
    for c in conventional_list:
        i += 1
    session['conventional'] = i
    return redirect(url_for('realistic'))

#4th page
@app.route('/add_realistic/', methods=['GET', 'POST'])
@login_required
def add_realistic():
    realistic_list = request.form.getlist('realistic_attr')
    i = 0
    for r in realistic_list:
        i += 1
    session['realistic'] = i
    return redirect(url_for('investigative'))

#5th page
@app.route('/add_investigative/', methods=['GET', 'POST'])
@login_required
def add_investigative():
    investigative_list = request.form.getlist('investigative_attr')
    i = 0
    for v in investigative_list:
        i += 1
    session['investigative'] = i
    return redirect(url_for('artistic'))

#artistic 6th page
@app.route('/add_artistic/', methods=['GET', 'POST'])
@login_required
def add_artistic():
    artistic_list = request.form.getlist('artistic_attr')
    i = 0
    for a in artistic_list:
        i += 1
    session['artistic'] = i
    return redirect(url_for('results'))

#****************************************************************


##RESULTS returns the totals from each page, and gets
#the 3 highest
@app.route('/results/', methods=['GET', 'POST'])
@login_required
def results():
    name = session['username']
    soc = session['social']
    enter = session['enterprise']
    con = session['conventional']
    real = session['realistic']
    inv = session['investigative']
    art = session['artistic']

    attr_tuples = [
        ('Social', soc),
        ('Enterprising', enter),
        ('Conventional', con),
        ('Realistic', real),
        ('Investigative', inv),
        ('Artistic', art)
    ]
    attr_tuples = sorted(attr_tuples, key=lambda attr: attr[1], reverse=True)
    first = attr_tuples[0][0]
    second = attr_tuples[1][0]
    third = attr_tuples[2][0]

    if attr_tuples[2][1] == attr_tuples[3][1]:
        third = "(tie) " + attr_tuples[2][0] + "/" + attr_tuples[3][0]

    return render_template('results.html', name=name, soc=soc, enter=enter, \
                           con=con, real=real, inv=inv, art=art, first=first, second=second, \
                           third=third)


