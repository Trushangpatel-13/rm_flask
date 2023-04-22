from flask import Flask, make_response, jsonify
from flask_cors import CORS
from models.user_model import user_model
from models.auth_model import auth_model
import os
from datetime import datetime
from flask_cors import CORS, cross_origin
from flask import request, send_file
from datetime import datetime
import json

#HOST="http://10.0.2.2:5000/static/uploads"
#HOST="http://127.0.0.1:5000/static/uploads"

#HOST="http://192.168.1.100:5000/static/uploads"
HOST="http://192.168.0.101:5000/static/uploads"
UPLOAD_FOLDER = "C:/Users/Administrator/PycharmProjects/Saurer_RM_Flask/static/uploads"

obj = user_model()
auth = auth_model()

app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['CORS_HEADERS'] = 'Content-Type'



@app.route("/user/login",methods=["POST"])
@cross_origin()
def user_login():
    auth_data = request.form
    return obj.user_login_model(auth_data['password'], auth_data['employee_id'])

@app.route("/post/data/all",methods=["POST"])
def ibo_post_data_all():
    ibo = request.form.get('IBO')
    res = request.form.get('data')
    data = json.loads(res)
    response = obj.post_data_all(ibo, data)
    if(response):
        return make_response({'payload':1}, 200)
    else:
        return make_response({'payload':0}, 200)

@app.route("/ping")
def user_ping():
    auth_data = request.form
    return "Response Ok"

@app.route('/image/upload', methods = ['POST'])
def upload_file():
    if request.method == 'POST':
      f = request.files['file']
      type = (f.filename).split(".")[1]
      ibo = request.form.get('ibo')
      process = request.form.get('Process')
      emp = request.form.get('Emp')
      date = str(datetime.now().strftime("%d-%m-%y_%H-%M-%S"))
      file = ibo+"_"+date+"_"+process+"_"+emp+"."+type
      subdir = UPLOAD_FOLDER + "/"+ibo+"/"+process
      present = os.path.exists(subdir)
      if(not present):
         os.makedirs(subdir)
      f.save(os.path.join(UPLOAD_FOLDER,ibo,process,file))
      return make_response({"payload": 1}, 200)

@app.route("/image/get", methods=["GET"])
def get_file():
    ibo = request.args.get('IBO')
    process = request.args.get('Process')
    getdir = UPLOAD_FOLDER+"/" + ibo + "/" + process
    #print(getdir)
    if(os.path.exists(getdir)):
        img_list = os.listdir(getdir)
        images = []
        appendDir = HOST+"/" + ibo + "/" + process + "/"
        for s in img_list:
            images.append(appendDir + s)
        print(images)
        return make_response({"images": images}, 200)
    else:
        return make_response("No Image Found", 204)

@app.route("/image/delete", methods=["GET"])
def delete_file():
    deldir = request.args.get('path')
    #print(deldir)
    index = deldir.index("uploads") + 7

    path = UPLOAD_FOLDER + deldir[index:]
    #print(path)

    if(os.path.exists(path)):
        os.remove(path)
        #print("Deleted")
        return make_response("Deleted Successfully", 200)
    else:
        return make_response("No Image Found", 204)

@app.route("/data/get/form", methods=["GET"])
def get_form_data():
    process = request.args.get('process')
    sub_process = request.args.get('sub_process')

    data = obj.get_data_form_model(process,sub_process)
    #default = obj.get_data_default_model(data["param_key"],data["param_value"],ibo)
    #data.update(default)

    return make_response(data, 200)

@app.route("/data/get/form/other", methods=["GET"])
def get_form_other_data():
    form_field = request.args.get('field').rstrip("]").lstrip("[").split(",")
    ibo = request.args.get('IBO')

    #print(form_field)
    field = []
    for i in form_field:
        field.append(i.rstrip("\"").lstrip("\""))

    data = obj.get_data_model(field, ibo)
    #print(data)
    return make_response(data, 200)

@app.route("/data/post/form", methods=["POST"])
def post_form_data():
    form_field = request.form.get('field').rstrip("]").lstrip("[").split(",")
    form_value = request.form.get('value').rstrip("]").lstrip("[").split(",")
    field = []
    value = []

    for i in form_field:
        field.append(i.rstrip("\"").lstrip("\""))
    for i in form_value:
        value.append(i.replace("\"","\'"))
    ibo = request.form.get('IBO')
    data = obj.post_data_model(field, value, ibo)

    return make_response("Done", 200)

@app.route("/data/get/all", methods=["GET"])
def all_data_model():

    ibo = request.args.get('IBO')
    data = obj.all_data_model(ibo)

    if (data != None):
        return make_response({'payload': data}, 200)
    else:
        return make_response({'payload': "Invalid"}, 500)



if __name__ == '__main__':
    #app.run(host='192.168.0.101', debug=True)
    app.run(debug=False)