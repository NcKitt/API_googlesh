## google sheet
import geopy.distance as ps
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('mytakecarebot-3826cd5b85bc.json', scope)
client = gspread.authorize(creds)
sheet = client.open("แบบฟอร์มกรอกข้อมูลเพื่อทำการนัดหมายและ Request assistant (Responses)").sheet1

# https://bot-takecare.herokuapp.com/getEmployee?name=น้ำแดง หวานหวาน

### web service
from flask import Flask, jsonify, request

app = Flask(__name__)

data1 = sheet.get_all_records()
listdata_column = pd.DataFrame(data1)
columns_name_th = listdata_column.columns.tolist()
columns_name_en = ['Timestamp', 'User_Name', 'User_Surname', 'User_Sex', 'User_Age', 'User_HouseNo', 'User_Village', \
                   'User_Alley', 'User_Road', 'User_Sub_District', 'User_District', 'User_Province', 'User_Postal_code',
                   'User_Phonenumber', \
                   'User_Congenital_disease', 'Emergencer_Name', 'Emergencer_Phone', 'Emergencer_Relation',
                   'User_Reason', 'User_Photo_link', \
                   'User_Current_Location', 'User_Location_name', 'User_Location_HouseNo', 'User_Location_Village',
                   'User_Location_Alley', \
                   'User_Location_Road', 'User_Location_Sub_District', 'User_Location_District',
                   'User_Location_Province', 'User_Location_Postal_code', \
                   'Hospital_Name', 'Hospital_tower', 'Hospital_floor', 'User_Day', 'User_time', 'User_timerange',
                   'Assistant_requirement', \
                   'Assistant_Sex', 'Assistant_Age', 'Permision']


def loadCustomer():
    data = sheet.get_all_records()
    listdata = pd.DataFrame(data)
    listdata.columns = columns_name_en
    return listdata


def searchCustomer(name, surname):
    data = sheet.get_all_records()
    listdata = pd.DataFrame(data)
    listdata.columns = columns_name_en

    if len(name.split(' ')) == 2:
        realname = name.split(' ')[0]
        surname = name.split(' ')[1]
    elif len(name.split('+')) == 2:
        realname = name.split('+')[0]
        surname = name.split('+')[1]

    customer = listdata[(listdata['User_Name'] == realname) & (listdata['User_Surname'] == surname)]
    return customer


@app.route('/getCustomer', methods=['GET'])
def getCustomer():
    try:
        name = request.args.get('name')
        surname = request.args.get('surname')
        res = searchCustomer(name, surname)
        show = res.iloc[0]
        show_dict = show.transpose().to_dict()
        
        return jsonify({'Timestamp':str(show['Timestamp']), 'User_Fullname':str((show['User_Name'] + ' ' +  show['User_Surname'])), 'User_Name':str(show['User_Name']), 'User_Surname':str(show['User_Surname']),
                        'User_Sex':str(show['User_Sex']), 'User_Age': int(show['User_Age']), 'User_HouseNo': str(show['User_HouseNo']),
                          'User_Village': str(show['User_Village']), 'User_Alley': str(show['User_Alley']), 'User_Road': str(show['User_Road']),
                          'User_Sub_District': str(show['User_Sub_District']), 'User_District':str(show['User_District']),
                          'User_Province': str(show['User_Province']), 'User_Postal_code': str(show['User_Postal_code']),
                          'User_Phonenumber': str(show['User_Phonenumber']), 'User_Congenital_disease':str(show['User_Congenital_disease']),
                          'Emergencer_Name': str(show['Emergencer_Name']), 'Emergencer_Phone': str(show['Emergencer_Phone']),
                          'Emergencer_Relation': str(show['Emergencer_Relation']), 'User_Reason':str(show['User_Reason']),
                          'User_Photo_link': str(show['User_Photo_link']), 'User_Current_Location':str(show['User_Current_Location']),
                          'User_Location_name': str(show['User_Location_name']), 'User_Location_HouseNo': str(show['User_Location_HouseNo']),
                          'User_Location_Village': str(show['User_Location_Village']), 'User_Location_Alley':str(show['User_Location_Alley']),
                          'User_Location_Road': str(show['User_Location_Road']),'User_Location_Sub_District':str(show['User_Location_Sub_District']),
                          'User_Location_District': str(show['User_Location_District']), 'User_Location_Province':str(show['User_Location_Province']),
                          'User_Location_Postal_code': str(show['User_Location_Postal_code']), 'Hospital_Name':str(show['Hospital_Name']),
                          'Hospital_tower':str(show['Hospital_tower']), 'Hospital_floor': str(show['Hospital_floor']),
                          'User_Day': str(show['User_Day']),'User_time': str(show['User_time']), 'User_timerange': str(show['User_timerange']),
                          'Assistant_requirement':str(show['Assistant_requirement']), 'Assistant_Sex':str(show['Assistant_Sex']),
                          'Assistant_Age': str(show['Assistant_Age']), 'Permision':str(show['Permision'])})

    except Exception as e:
        return jsonify({'message': 'ไม่พบข้อมูลค่ะ'})


if __name__ == '__main__':
    app.run(debug=True)
