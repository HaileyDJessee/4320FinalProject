from flask import current_app as app
from flask import redirect, render_template, url_for, request, flash

from .forms import *


#@app.route("/", methods=['GET', 'POST'])
@app.route("/", methods=['GET', 'POST'])
def user_options():
    
    form = UserOptionForm()
    if request.method == 'POST' and form.validate_on_submit():
        option = request.form['option']

        if option == "1":
            return redirect('/admin')
        else:
            return redirect("/reservations")
    
    return render_template("options.html", form=form, template="form-template")

@app.route("/admin", methods=['GET', 'POST'])
def admin():

    form = AdminLoginForm()

    if request.method == 'POST' and form.validate_on_submit():
        username = request.form['username']
        password = request.form['password']

        with open('passcodes.txt') as f:
            check = f.read()
            if (username + ', ' + password) in check:
                err = 'found user and password'
                return render_template("admin.html", form=form, err = err, template="form-template")
            else:
                err = "ERROR: username and password combination not found please check entries and resubmit."
                return render_template("admin.html", form=form, err = err, template="form-template")


    return render_template("admin.html", form=form, template="form-template")

@app.route("/reservations", methods=['GET', 'POST'])
def reservations():

    form = ReservationForm()

    if request.method == 'POST' and form.validate_on_submit():
        first_name = request.form['first_name']
        row = request.form['row']
        seat = request.form['seat']
        len1 = len(first_name)
        classstring ='INFOTC4320'
        len2 = len(classstring)
        seatingticket = ""
        if len2 > len1:
            for i in range(len1):
                seatingticket += first_name[i]
                seatingticket += classstring[i]
            seatingticket += classstring[-(len2-len1):]
        else:
            for i in range(len1):
                try:
                    if len2 != None:
                        seatingticket += first_name[i]
                        seatingticket += classstring[i]
                except:
                    break
        ticketstring = ('\n' +first_name + ', '+ row +', '+ seat + ', ' + seatingticket)
        with open('reservations.txt', 'a') as res:
            res.writelines(ticketstring)
    return render_template("reservations.html", form=form, template="form-template")

