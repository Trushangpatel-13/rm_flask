from datetime import datetime, timedelta
import mysql.connector
import json
from flask import make_response, jsonify
import jwt
from configs.config import dbconfig

class user_model():
    def __init__(self):
        self.con = mysql.connector.connect(host=dbconfig['host'],user=dbconfig['username'],password=dbconfig['password'],database=dbconfig['database'])
        self.con.autocommit=True
        self.cur = self.con.cursor(dictionary=True)
        
    def all_user_model(self):
        self.cur.execute("SELECT * FROM users")
        result = self.cur.fetchall()
        if len(result)>0:
            return {"payload":result}
            # return make_response({"payload":result},200)
        else:
            return "No Data Found"
    
    def add_user_model(self,data):
        self.cur.execute(f"INSERT INTO users(name, email, phone, roleid, password) VALUES('{data['name']}', '{data['email']}', '{data['phone']}', '{data['roleid']}', '{data['password']}')")
        return make_response({"message":"CREATED_SUCCESSFULLY"},201)
    
    def add_multiple_users_model(self, data):
        # Generating query for multiple inserts
        qry = "INSERT INTO users(name, email, phone, roleid, password) VALUES "
        for userdata in data:
            qry += f" ('{userdata['name']}', '{userdata['email']}', '{userdata['phone']}', {userdata['roleid']},'{userdata['password']}'),"
        finalqry = qry.rstrip(",")
        self.cur.execute(finalqry)
        return make_response({"message":"CREATED_SUCCESSFULLY"},201)

    def delete_user_model(self,id):
        self.cur.execute(f"DELETE FROM users WHERE id={id}")
        if self.cur.rowcount>0:
            return make_response({"message":"DELETED_SUCCESSFULLY"},202)
        else:
            return make_response({"message":"CONTACT_DEVELOPER"},500)
        
    
    def update_user_model(self,data):
        self.cur.execute(f"UPDATE users SET name='{data['name']}', email='{data['email']}', phone='{data['phone']}' WHERE id={data['id']}")
        if self.cur.rowcount>0:
            return make_response({"message":"UPDATED_SUCCESSFULLY"},201)
        else:
            return make_response({"message":"NOTHING_TO_UPDATE"},204)

    def patch_user_model(self, data):
        qry = "UPDATE users SET "
        for key in data:
            if key!='id':
                qry += f"{key}='{data[key]}',"
        qry = qry[:-1] + f" WHERE id = {data['id']}"
        self.cur.execute(qry)
        if self.cur.rowcount>0:
            return make_response({"message":"UPDATED_SUCCESSFULLY"},201)
        else:
            return make_response({"message":"NOTHING_TO_UPDATE"},204)

    def pagination_model(self, pno, limit):
        pno = int(pno)
        limit = int(limit)
        start = (pno*limit)-limit
        qry = f"SELECT * FROM users LIMIT {start}, {limit}"
        self.cur.execute(qry)
        result = self.cur.fetchall()
        if len(result)>0:
            return make_response({"page":pno, "per_page":limit,"this_page":len(result), "payload":result})
        else:
            return make_response({"message":"No Data Found"}, 204)

    def upload_avatar_model(self, uid, db_path):
        self.cur.execute(f"UPDATE users SET avatar='{db_path}' WHERE id={uid}")
        if self.cur.rowcount>0:
            return make_response({"message":"FILE_UPLOADED_SUCCESSFULLY", "path":db_path},201)
        else:
            return make_response({"message":"NOTHING_TO_UPDATE"},204)

    def get_image_path_model(self, uid):
        self.cur.execute(f"SELECT avatar FROM users WHERE id={uid}")
        result = self.cur.fetchall()
        if len(result)>0:
            print(type(result))
            return {"payload":result}
        else:
            return "No Data Found"  
###############################################################################################################
    def user_login_model(self,password,emp_id):
        self.cur.execute(f"SELECT First_Name, Last_Name, Employee_ID,RMC,RMO,RMP,RMS,RMQ from users WHERE Password='{password}' and Employee_ID='{emp_id}'")
        result = self.cur.fetchall()
        print(len(result))
        if len(result)==1:
            exptime = datetime.now() + timedelta(minutes=1)
            exp_epoc_time = exptime.timestamp()
            data = {
                "payload":result[0],
                "exp":int(exp_epoc_time)
            }
            print(int(exp_epoc_time))
            jwt_token = jwt.encode(data, "Saurer_RM", algorithm="HS256")
            return make_response({"token":jwt_token}, 200)
        else:
            print("No")
            return make_response({"message":"NO SUCH USER"}, 204)


    def post_data_all(self,ibo,data):
        k = data.keys()
        v = data.values()
        qry = "UPDATE rotor_motor_data SET "
        for (key,value) in zip(k,v):
            #print(key)
            a = ''
            #print(type(a))
            if(type(value)==str):
               #print(value)
                qry += f"{key}=\'{value}\', "
            elif(value== None):
                qry += f"{key}= null, "
            elif(type(value)=='str'):
                if(len(value)==0):
                    qry += f"{key}= null, "
            else:
                qry += f"{key}={value}, "
        qry = qry.rstrip(", ")
        finalqry = qry + f" WHERE IBO_no=\'{ibo}\'"
        print(finalqry)
        self.cur.execute(finalqry)
        if self.cur.rowcount>0:
            print("Completed")
            return 1
        else:
            return 0



    """
    #def get_data_form_model(self, process,sub_process):
        self.cur.execute(f"SELECT Key_Name, Value_Name FROM form_details WHERE Process=\"{process}\" and Sub_Process=\"{sub_process}\"")
        result = self.cur.fetchall()
        form_field = []
        form_object = {}
        k=[]
        v=[]
        if len(result)>0:
            for i in range(0,len(result)):
                k.append(result[i]["Key_Name"])
                v.append(result[i]["Value_Name"])
            for i in range(0,len(k)):
                form_object = {}
                form_object['key'] = k[i]
                form_object['value'] = v[i]
                form_field.append(form_object)
            obj = {}
            for i in range(0,len(k)):
                obj[k[i]] = v[i]
            print(obj)
            return {"payload":form_field,"param":obj}
        else:
            return "No Data Found"

    def get_data_default_model(self, form_field_key,form_field_value, ibo):

        qry = "SELECT "
        for field in form_field_key:
            qry += f"{field},"

        qry = qry.rstrip(",")
        finalqry = qry + f" FROM rotor_motor_data WHERE IBO_no=\'{ibo}\'"
        self.cur.execute(finalqry)
        result = self.cur.fetchone()
        if len(result) > 0:
            default_val = []
            default_key = []
            for i in range(0,len(form_field_key)):
                if(result[form_field_key[i]]):
                    #print(form_field_key[i])
                    #print(i)
                    default_val.append(form_field_value[i])
                    default_key.append(form_field_key[i])
            return {"default_val":default_val,"default_key":default_key}
        else:
            return "No Data Found"

    def get_data_model(self, field, ibo):

        qry = "SELECT "
        for i in field:
            qry += f"{i},"

        qry = qry.rstrip(",")
        finalqry = qry + f" FROM rotor_motor_data WHERE IBO_no=\'{ibo}\'"
        #print(finalqry)

        self.cur.execute(finalqry)
        result = self.cur.fetchone()
        if len(result) > 0:

            return {"payload_other":result}
        else:
            return "No Data Found"

    def post_data_model(self, field, value, ibo):

        qry = "UPDATE rotor_motor_data SET "
        for i in range(0,len(field)):
            #print(i)
            qry += f"{field[i]}={value[i]}, "

        qry = qry.rstrip(", ")
        finalqry = qry + f" WHERE IBO_no=\'{ibo}\'"
        #print(finalqry)
        #self.cur.execute(finalqry)


    """
    def all_data_model(self,ibo):

        qry = f"SELECT * FROM rotor_motor_data WHERE IBO_no=\'{ibo}\'"
        self.cur.execute(qry)
        result = self.cur.fetchone()
        if(result!=None):
            if len(result) > 0:
                print(result)
                return result
        else:
            return None


