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
    seating_matrix = [['O','O','O','O']  for row in range(12)]
    matrix = seating_matrix
    if request.method == 'POST' and form.validate_on_submit():
        username = request.form['username']
        password = request.form['password']

        
        with open('passcodes.txt') as f:
            check = f.read()
            if (username + ', ' + password) in check:
                cost_matrix = [[100, 75, 50, 100] for row in range(12)]
                sales = 0
                with open("reservations.txt", "r+") as file:
                    print(file.tell())
                    for line in file:
                        lineholder= line
                        seatinglocation = lineholder.split(', ')
                        salessub=  cost_matrix[int(seatinglocation[1])][int(seatinglocation[2])]
                        sales += salessub
                with open("reservations.txt", "r+") as file:
                        print(file.tell())
                        for line in file:
                            lineholder= line
                            seatinglocation = lineholder.split(', ')
                            matrix[int(seatinglocation[1])][int(seatinglocation[2])] = 'X'
                return render_template("admin.html", form=form, sales = sales, matrix = '\n'.join(map(str, seating_matrix)), template="form-template")
            else:
                err = "Bad username/password combination. Try Again"
                return render_template("admin.html", form=form, err = err, template="form-template")
    return render_template("admin.html", form=form, template="form-template")
@app.route("/reservations", methods=['GET', 'POST'])
def reservations():

    form = ReservationForm()
    seating_matrix = [['O','O','O','O']  for row in range(12)]
    matrix = seating_matrix
    with open("reservations.txt", "r+") as file:
            print(file.tell())
            for line in file:
                lineholder= line
                seatinglocation = lineholder.split(', ')
                matrix[int(seatinglocation[1])][int(seatinglocation[2])] = 'X'
    if request.method == 'POST' and form.validate_on_submit():
        first_name = request.form['first_name']
        row = request.form['row']
        seat = request.form['seat']
        len1 = len(first_name)
        classstring ='INFOTC1040'
        len2 = len(classstring)
        seatingticket = ''
        ticketcheck = (str(int(row)-1) + ', ' + str(int(seat)-1))
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
        ticketstring = ('\n' +first_name + ', '+ str(int(row)-1) +', '+ str(int(seat)-1) + ', ' + seatingticket)
        ticket = seatingticket
        err = None
        reservationfound = False
        ticketcheck = (str(int(row)-1) + ', ' + str(int(seat)-1))
        with open('reservations.txt', 'r') as file:
            for line in file:
                lineholder = line
                if ticketcheck in lineholder:
                    ticket = None
                    reservationfound = True
                    break
        if reservationfound == True:
            err = "ERROR!"
        else:
            with open('reservations.txt', 'a') as res:
                res.writelines(ticketstring)
        with open("reservations.txt", "r+") as file:
            for line in file:
                lineholder= line
                seatinglocation = lineholder.split(', ')
                matrix[int(seatinglocation[1])][int(seatinglocation[2])] = 'X'
        return render_template("reservations.html", form=form, ticket = ticket, row = row, seat = seat, first_name = first_name, matrix = '\n'.join(map(str, seating_matrix)), err = err, template="form-template")
                        
    return render_template("reservations.html", form=form, matrix = '\n'.join(map(str, seating_matrix)), template="form-template")

