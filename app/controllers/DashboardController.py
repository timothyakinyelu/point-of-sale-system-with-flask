from flask import render_template, json


def dashboard():
    
    
    legend = json.dumps('Monthly Data')
    labels = json.dumps(["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"])
    values = json.dumps([10, 9, 8, 7, 6, 4, 7, 8, 5, 8, 3, 7])
    return render_template('dashboard.html', labels = labels, legend = legend, values = values)

# def chart():
#     legend = 'Monthly Data'
#     labels = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
#     values = [10, 9, 8, 7, 6, 4, 7, 8, 5, 8, 3, 7]
#     return jsonify(labels = labels, legend = legend, values = values)