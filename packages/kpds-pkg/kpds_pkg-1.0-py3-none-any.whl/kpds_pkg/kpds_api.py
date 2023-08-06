import requests
import pandas as pd
from pandas import Series
from pandas import DataFrame
import json
from kpds_pkg import config
import datetime

now = datetime.datetime.now()
nowDatetime = now.strftime('%Y-%m-%d_%H-%M-%S')

def ticker_auth(auth_key):
    if auth_key != "":
        url = "https://www.koreapds.com/api/kpds_ticker_auth.php?auth_key="+auth_key
        output = requests.get(url)

        json_data  = json.loads(output.text)

        nl = '\n'
        if json_data["AUTH"][0]["MESSAGE"] == "정상적으로 인증되었습니다." :
            print(f'{json_data["AUTH"][0]["MESSAGE"]} {nl}ID : {json_data["AUTH"][0]["ID"]} 만료일 : {json_data["AUTH"][0]["END_DATE"]}')

        elif json_data["AUTH"][0]["MESSAGE"] != "정상적으로 인증되었습니다.":
            print(f'ERROR : {json_data["AUTH"][0]["MESSAGE"]}')

        config.auth=1
        config.api_key = auth_key

    else:
        print("입력 값이 잘못되었습니다.")

        config.auth=0
        config.api_key=""

def ticker_find(find_data):
    # 변수 확인
    if config.auth == 0:
        print("Error : 사용자 인증이 필요합니다.")
        exit()
    elif config.auth == 1:
        auth_key="?auth_key=" + config.api_key
        
    if find_data == "":
        print("Error : 키워드를 입력해주세요.")
        exit()
    else:
        find_data_param = "&find_data=" + find_data

    url_param = auth_key + find_data_param
    url = "https://www.koreapds.com/api/kpds_ticker_find.php" + url_param
    output = requests.get(url)

    # json
    json_data  = json.loads(output.text)
    print(f'찾은 데이터 개수 : {json_data["Search Ticker Count"]}')

    df = pd.json_normalize(json_data['Search Ticker data'])

    return df

def ticker_info(ticker):
    if config.auth == 0:
        print("Error : 사용자 인증이 필요합니다.")
        exit()
    elif config.auth == 1:
        auth_key="?auth_key=" + config.api_key

    if ticker == "":
        print("ERROR : TICKER를 입력해주세요.")
        exit()
    else:
        ticker_param = "&ticker=" + ticker

    url_param = auth_key + ticker_param

    url =  "https://www.koreapds.com/api/kpds_ticker_info.php" + url_param
    output = requests.get(url)
    
    json_data  = json.loads(output.text)

    df = pd.json_normalize(json_data)
    df = df.transpose()
    df.rename(columns={0:"INFO"}, inplace=True)

    return df

def kpds_ticker_raw_data(ticker,**param):
    if config.auth == 0:
        print("Error : 사용자 인증이 필요합니다.")
        exit()
    elif config.auth == 1:
        auth_key="?auth_key=" + config.api_key

    if ticker == "":
        print("Error : TICKER를 입력해주세요.")
        exit()
    else:
        ticker_param = "&ticker=" + ticker

    if param.get("row") == None:
        param["row"] = ""
    if param.get("start_date") == None:
        param["start_date"] = ""       
    if param.get("end_date") == None:
        param["end_date"] = ""       
    if param.get("avg") == None:
        param["avg"] = ""       
    if param.get("sort") == None:
        param["sort"] = ""       
    if param.get("fx") == None:
        param["fx"] = ""       

    row = "&row="+param.get("row")     
    start_date = "&start_date="+param.get("start_date") 
    end_date = "&end_date="+param.get("end_date") 
    avg = "&avg="+param.get("avg") 
    sort = "&sort="+param.get("sort") 
    fx = "&fx="+param.get("fx") 

    url_param = auth_key + ticker_param + row + start_date + end_date + avg + sort + sort + fx
    
    url =  "https://www.koreapds.com/api/kpds_ticker_raw_data.php" + url_param
    output = requests.get(url)
  
    data = json.loads(output.text)
    df = pd.json_normalize(data['DATA'])
    print(f"{ticker} 데이터 추출 완료")

    if param.get("excel") == "o":
        # 출력한 데이터 엑셀 저장
        info_data = ticker_info(ticker)
        writer = pd.ExcelWriter('raw_data' + '_' + nowDatetime + '.xlsx', engine='openpyxl')

        info_data = info_data.head(6) 
        info_data.to_excel(writer)
        df.to_excel(writer, startrow=len(info_data)+2, index=False)
        writer.save()

        print(f"{ticker} 데이터 저장 완료")

    return df

def kpds_ticker_raw_data_merge(ticker, **param):
    if config.auth == 0:
        print("Error : 사용자 인증이 필요합니다.")
        exit()
    elif config.auth == 1:
        auth_key="?auth_key=" + config.api_key

    if ticker == "":
        print("Error : TICKER를 입력해주세요.")
        exit()
    else:
        ticker_param = "&ticker=" + ticker


    if param.get("row") == None:
        param["row"] = ""
    if param.get("start_date") == None:
        param["start_date"] = ""       
    if param.get("end_date") == None:
        param["end_date"] = ""       
    if param.get("avg") == None:
        param["avg"] = ""       
    if param.get("sort") == None:
        param["sort"] = ""       
    if param.get("merge_type ") == None:
        param["merge_type "] = ""       

  
    row = "&row="+param.get("row")     
    start_date = "&start_date="+param.get("start_date") 
    end_date = "&end_date="+param.get("end_date") 
    avg = "&avg="+param.get("avg") 
    sort = "&sort="+param.get("sort") 
    merge_type = "&merge_type="+param.get("merge_type") 

    url_param = auth_key + ticker_param + row + start_date + end_date + avg + sort + sort + merge_type

    url =  "https://www.koreapds.com/api/kpds_ticker_raw_data_merge.php" + url_param
    output = requests.get(url)

    if( (param.get("merge_type")).lower() == "none"):
        # df_list = []
        df_dic = {}
        replace_data = output.text.replace('}{','}  {')
        split_data = replace_data.split('  ')
        
        writer = pd.ExcelWriter('raw_data_merge_'+(param.get("merge_type")).lower() +'_'+ nowDatetime +'.xlsx', engine='openpyxl')

        for i in range(len(split_data)):
            data = json.loads(split_data[i])
            df = pd.json_normalize(data['DATA'])
            info_data = ticker_info(data['TICKER'])
            
            df_dic[info_data.iloc[2]['INFO']] = df
            
            if (param.get("excel")).lower() == "o":
                # info_data = ticker_info(data['TICKER'])
                info_data = info_data.head(6)
                info_data.to_excel(writer, sheet_name = 'Sheet' + str(i))
                df.to_excel(writer, sheet_name = 'Sheet' + str(i), startrow=len(info_data)+2, index=False)
                writer.save()
        print(f"{ticker} 데이터 저장 완료")   
        return df_dic   

    else:
        data = json.loads(output.text)
        df = pd.json_normalize(data['DATA'])

        ticker = ticker.split(",")
        ticker_count = len(ticker)

        if param.get("excel") == "o":
            writer = pd.ExcelWriter('raw_data_merge_' + (param.get("merge_type")).lower() + '_' + nowDatetime +'.xlsx', engine='openpyxl')
            
            for i in range(ticker_count):
                info_data = ticker_info(ticker[i])
                info_data = info_data.head(6)
                if i == 0:
                    info_data.to_excel(writer, startcol=(i+1)*i)
                else:
                    info_data.to_excel(writer, startcol=(i+1)*i, index=False)
                
            df.to_excel(writer, startrow=len(info_data)+2, index=False)
            writer.save()

            print(f"{ticker} 데이터 저장 완료")
		return df

    
    