def tutorialModule(id,a,b) :
    import requests
    import os
    import pandas as pd
    import gspread
    from oauth2client.service_account import ServiceAccountCredentials
 
    if not os.path.exists("dragonball"):
        os.makedirs("dragonball")

    check_list = []

    scope = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive',
    ]

    json_file_name = 'dragonballproject-9f19a8b84433.json'

    credentials = ServiceAccountCredentials.from_json_keyfile_name(json_file_name, scope)
    gc = gspread.authorize(credentials)

    spreadsheet_url = 'https://docs.google.com/spreadsheets/d/1abPr5zsOSQ0aYsoBFk9XDgWQgdCPlqUqgbB9EZNpst4/edit#gid=0'

    doc = gc.open_by_url(spreadsheet_url)
    worksheet = doc.worksheet('시트1')

    if a == "pandas":
        check_list.append("O")
        print("단서1 정답")
    if b == "merge":
        check_list.append("O")
        print("단서2 정답")
    if check_list.count("O") == 2 :
        image_url = "https://github.com/hodragon5237/aivleexample/blob/main/dragonBall_Start.jpg?raw=true"
        save_path = "./dragonball/시작.png"

        download_file = requests.get(image_url)

        with open(save_path, 'wb') as photo:
            photo.write(download_file.content)

        id_list = worksheet.col_values(1)
        raw_list = pd.DataFrame(worksheet.get_all_records())

        if id not in id_list: 
            raw_list.loc[len(raw_list)] = [id,1,0,0,0,0,0,0,0,0]
            raw_list['합계']=raw_list.loc[:,'Start':'7성구'].sum(axis=1)
        else :
            raw_list.loc[raw_list[raw_list.ID == id].index, 'Start'] = 1
        
        raw_list = raw_list.sort_values('합계', ascending=False)

        worksheet.update([raw_list.columns.values.tolist()] + raw_list.values.tolist())
                
        print("드래곤볼을 획득했습니다.")
    else :
        print("드래곤볼 획득에 실패했습니다.")

def firstModule(id,a,b,c,d,e,f,g,h) :
    import requests
    import os
    import pandas as pd
    import gspread
    from oauth2client.service_account import ServiceAccountCredentials
 
    if not os.path.exists("dragonball"):
        os.makedirs("dragonball")

    check_list = []

    scope = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive',
    ]

    json_file_name = 'dragonballproject-9f19a8b84433.json'

    credentials = ServiceAccountCredentials.from_json_keyfile_name(json_file_name, scope)
    gc = gspread.authorize(credentials)

    spreadsheet_url = 'https://docs.google.com/spreadsheets/d/1abPr5zsOSQ0aYsoBFk9XDgWQgdCPlqUqgbB9EZNpst4/edit#gid=0'

    doc = gc.open_by_url(spreadsheet_url)
    worksheet = doc.worksheet('시트1')

    if a == "7":
        check_list.append("O")
        print("단서1 정답")
    if b == "109642" or "109,642":
        check_list.append("O")
        print("단서2 정답")
    if c == "RID":
        check_list.append("O")
        print("단서3 정답")
    if d == "countplot":
        check_list.append("O")
        print("단서4 정답")
    if e == "Density":
        check_list.append("O")
        print("단서5 정답")
    if f == "0":
        check_list.append("O")
        print("단서6 정답")
    if g == "5":
        check_list.append("O")
        print("단서7 정답")
    if h == "0.84":
        check_list.append("O")
        print("단서8 정답")
    if check_list.count("O") == 8 :
        image_url = "https://github.com/hodragon5237/aivleexample/blob/main/1%EC%84%B1%EA%B5%AC.png?raw=true"
        save_path = "./dragonball/1성구.png"

        download_file = requests.get(image_url)

        with open(save_path, 'wb') as photo:
            photo.write(download_file.content)

        id_list = worksheet.col_values(1)
        raw_list = pd.DataFrame(worksheet.get_all_records())

        if id not in id_list: 
            raw_list.loc[len(raw_list)] = [id,0,1,0,0,0,0,0,0,0]
            raw_list['합계']=raw_list.loc[:,'Start':'7성구'].sum(axis=1)
        else :
            raw_list.loc[raw_list[raw_list.ID == id].index, '1성구'] = 1

        raw_list.sort_values('합계', ascending=False)

        worksheet.update([raw_list.columns.values.tolist()] + raw_list.values.tolist())
        
        print("드래곤볼을 획득했습니다.")
    else :
        print("드래곤볼 획득에 실패했습니다.")

def secondModule(a,b,c,d,e,f,g) :
    import requests
    import os
    import pandas as pd
    import gspread
    from oauth2client.service_account import ServiceAccountCredentials
 
    if not os.path.exists("dragonball"):
        os.makedirs("dragonball")

    check_list = []

    if a == "0":
        check_list.append("O")
        print("단서1 정답")
    if b == "pad" or "ffill":
        check_list.append("O")
        print("단서2 정답")
    if c == "2":
        check_list.append("O")
        print("단서3 정답")
    if d == "3574.445236":
        check_list.append("O")
        print("단서4 정답")
    if e == "109175" or "109,175":
        check_list.append("O")
        print("단서5 정답")
    if f == "115":
        check_list.append("O")
        print("단서6 정답")
    if g == "108":
        check_list.append("O")
        print("단서7 정답")
    if check_list.count("O") == 7 :
        image_url = "https://github.com/hodragon5237/aivleexample/blob/main/2%EC%84%B1%EA%B5%AC.png?raw=true"
        save_path = "./dragonball/2성구.png"

        download_file = requests.get(image_url)

        with open(save_path, 'wb') as photo:
            photo.write(download_file.content)
        
        print("드래곤볼을 획득했습니다.")
    else :
        print("드래곤볼 획득에 실패했습니다.")

def thirdModule(a,b,c,d,e,f,g,h,i) :
    import requests
    import os
 
    if not os.path.exists("dragonball"):
        os.makedirs("dragonball")

    check_list = []

    check_list = []

    if a == "44346" or "44,346":
        check_list.append("O")
        print("단서1 정답")
    if b == "fit":
        check_list.append("O")
        print("단서2 정답")
    if c == "0.69942":
        check_list.append("O")
        print("단서3 정답")
    if d == "signaltype":
        check_list.append("O")
        print("단서4 정답")
    if e == "276.47308":
        check_list.append("O")
        print("단서5 정답")
    if f == "A_DISTANCE":
        check_list.append("O")
        print("단서6 정답")
    if g == "0.71666":
        check_list.append("O")
        print("단서7 정답")
    if h == "HOUR_7":
        check_list.append("O")
        print("단서8 정답")
    if i == "joblib":
        check_list.append("O")
        print("단서9 정답")
    if check_list.count("O") == 9 :
        image_url = "https://github.com/hodragon5237/aivleexample/blob/main/3%EC%84%B1%EA%B5%AC.png?raw=true"
        save_path = "./dragonball/3성구.png"

        download_file = requests.get(image_url)

        with open(save_path, 'wb') as photo:
            photo.write(download_file.content)
        
        print("드래곤볼을 획득했습니다.")
    else :
        print("드래곤볼 획득에 실패했습니다.")

def fourthModule(a,b) :
    import requests
    import os
 
    if not os.path.exists("dragonball"):
        os.makedirs("dragonball")

    check_list = []

    if a == "11201" or "11,201":
        check_list.append("O")
        print("단서1 정답")
    if b == "load_weights":
        check_list.append("O")
        print("단서2 정답")
    if check_list.count("O") == 2 :
        image_url = "https://github.com/hodragon5237/aivleexample/blob/main/4%EC%84%B1%EA%B5%AC.png?raw=true"
        save_path = "./dragonball/4성구.png"

        download_file = requests.get(image_url)

        with open(save_path, 'wb') as photo:
            photo.write(download_file.content)
        
        print("드래곤볼을 획득했습니다.")
    else :
        print("드래곤볼 획득에 실패했습니다.")

def fifthModule(a,b) :
    import requests
    import os
 
    if not os.path.exists("dragonball"):
        os.makedirs("dragonball")

    check_list = []

    if a == "load":
        check_list.append("O")
        print("단서1 정답")
    if b == "16.4" or "016.4":
        check_list.append("O")
        print("단서2 정답")
    if check_list.count("O") == 2 :
        image_url = "https://github.com/hodragon5237/aivleexample/blob/main/5%EC%84%B1%EA%B5%AC.png?raw=true"
        save_path = "./dragonball/5성구.png"

        download_file = requests.get(image_url)

        with open(save_path, 'wb') as photo:
            photo.write(download_file.content)
        
        print("드래곤볼을 획득했습니다.")
    else :
        print("드래곤볼 획득에 실패했습니다.")

def sixthModule() :
    import requests
    import joblib
    from sklearn.metrics import r2_score
    from sklearn.model_selection import train_test_split

    import os
    import pandas as pd

    if not os.path.exists("dragonball"):
        os.makedirs("dragonball")

    check_list = []

    # 학습/평가 데이터 로딩
    df_feature = pd.read_csv("add_data/onenavi_train_feature.csv",sep="|")
    df_target = pd.read_csv("add_data/onenavi_train_target.csv",sep="|")

    df_evaluation_target = pd.read_csv("add_data/onenavi_evaluation_et.csv",sep="|")
    df_evaluation_feature = pd.read_csv("add_data/onenavi_evaluation_feature.csv",sep="|")

    # train_test_split
    train_x, test_x, train_y, test_y = train_test_split(df_feature, df_target, test_size=0.20, random_state=42)

    firstCheckModel = joblib.load("./model/4_model.pkl")
    secondCheckModel = joblib.load("./model/5_model.pkl")

    panda_pred_y = firstCheckModel.predict(test_x)
    caviar_pred_y = secondCheckModel.predict(test_x)

    def calculation_etaa(et, eta):
        etaa = (1-(abs(et-eta)/et))*100.0
        etaa[(etaa < 0)] = 0
        return etaa
    
    df_evaluation_target["pandaETA"] = firstCheckModel.predict(df_evaluation_feature)
    df_evaluation_target["pandaETAA"] = calculation_etaa(df_evaluation_target['ET'], df_evaluation_target["pandaETA"])
    df_evaluation_target["caviarETA"] = firstCheckModel.predict(df_evaluation_feature)
    df_evaluation_target["caviarETAA"] = calculation_etaa(df_evaluation_target['ET'], df_evaluation_target["caviarETA"])

    if r2_score(test_y,panda_pred_y) >= 0.718:
        check_list.append("O")
        print("단서1 정답")
    if r2_score(test_y,caviar_pred_y) >= 0.716:
        check_list.append("O")
        print("단서2 정답")
    if (df_evaluation_target["pandaETAA"].mean() >= 82.5) or (df_evaluation_target["caviarETAA"].mean() >= 82.5):
        check_list.append("O")
        print("단서3 정답")
    if check_list.count("O") == 3 :
        image_url = "https://github.com/hodragon5237/aivleexample/blob/main/6%EC%84%B1%EA%B5%AC.png?raw=true"
        save_path = "./dragonball/6성구.png"

        download_file = requests.get(image_url)

        with open(save_path, 'wb') as photo:
            photo.write(download_file.content)
        
        print("드래곤볼을 획득했습니다.")
    else :
        print("드래곤볼 획득에 실패했습니다.")

def seventhModule() :
    import requests
    import joblib
    from sklearn.metrics import r2_score
    from sklearn.model_selection import train_test_split
    import tensorflow as tf

    import os
    import pandas as pd

    if not os.path.exists("dragonball"):
        os.makedirs("dragonball")

    check_list = []

    # 학습/평가 데이터 로딩
    df_feature = pd.read_csv("add_data/onenavi_train_feature.csv",sep="|")
    df_target = pd.read_csv("add_data/onenavi_train_target.csv",sep="|")

    df_evaluation_target = pd.read_csv("add_data/onenavi_evaluation_et.csv",sep="|")
    df_evaluation_feature = pd.read_csv("add_data/onenavi_evaluation_feature.csv",sep="|")

    # train_test_split
    train_x, test_x, train_y, test_y = train_test_split(df_feature, df_target, test_size=0.20, random_state=42)

    firstCheckModel = joblib.load("./model/6_model.pkl")
    secondCheckModel = tf.keras.models.load_model("model/DeeplearningModel_2.h5")

    def calculation_etaa(et, eta):
        etaa = (1-(abs(et-eta)/et))*100.0
        etaa[(etaa < 0)] = 0
        return etaa 

    temp_dataframe = pd.DataFrame()

    first_checkList = []
    second_checkList = []

    for i in range(10):

        temp_test_index = df_evaluation_feature.sample(n=10).index

        first_pred_y = firstCheckModel.predict(df_evaluation_feature.loc[temp_test_index])
        second_pred_y = secondCheckModel.predict(df_evaluation_feature.loc[temp_test_index])
        et = df_evaluation_target.loc[temp_test_index]['ET'].reset_index(drop=True)
        etaa = df_evaluation_target.loc[temp_test_index]['ETAA'].reset_index(drop=True)

        temp_dataframe["firstETA_{}".format(i)] = first_pred_y
        temp_dataframe["firstETAA_{}".format(i)] = calculation_etaa(et, temp_dataframe["firstETA_{}".format(i)])
        temp_dataframe["raw_firstETAA_{}".format(i)] = etaa
        temp_dataframe["secondETA_{}".format(i)] = second_pred_y
        temp_dataframe["secondETAA_{}".format(i)] = calculation_etaa(et, temp_dataframe["secondETA_{}".format(i)])
        temp_dataframe["raw_secondETAA_{}".format(i)] = etaa
        
        if temp_dataframe["firstETAA_{}".format(i)].mean() >= temp_dataframe["raw_firstETAA_{}".format(i)].mean():
            first_checkList.append("O")
        if temp_dataframe["secondETAA_{}".format(i)].mean() >= temp_dataframe["raw_secondETAA_{}".format(i)].mean():
            second_checkList.append("O")

    if  first_checkList.count("O") >= 7:
        check_list.append("O")
        print("단서1 정답")
    if  second_checkList.count("O") >= 8:
        check_list.append("O")
        print("단서2 정답")
    if check_list.count("O") == 2 :
        image_url = "https://raw.githubusercontent.com/hodragon5237/aivleexample/main/7%EC%84%B1%EA%B5%AC.png"
        save_path = "./dragonball/7성구.png"

        download_file = requests.get(image_url)

        with open(save_path, 'wb') as photo:
            photo.write(download_file.content)
        
        print("드래곤볼을 획득했습니다.")
    else :
        print("드래곤볼 획득에 실패했습니다.")