
import requests
import os

from common.lib.newReport import new_report
from common.lib.public import *
from time import sleep


# cxx增加   2022.1.22修改
from common.lib.sendmail import send_mail

#2021.1.22cxx1.24修改
def parsley(cf,file_pa,codeBaseu,num=['0000275324']):
#def parsley(num,cf):

    try:
        productName = cf.get("product_name", "product_name")
        timeu = get_shijianchuo_p()  # 运行时间
        contactName = cf.get("parsle", "contactName")  # 维护人
        num_result = int(cf.get("parsle", "num_result"))  # result在第几列
        totalCount = int(gain_excel_nrows(0, file_pa) - 1)
        passedCount = int(num_pa(file_pa, num_result))
        if totalCount == passedCount:
            result = 'PASS'
        else:
            result = 'FAIL'


        url = 'http://test.chinasoftinc.com:8423/parsley/api/gateway/send'
        par = {
            "Content-Type": "application/json",
            "module": "parsley",
            "method": "parsley/api/gateway/send",
            "rpcType": "http",
            "httpMethod": "post",
            "mannjuToken": "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiLmnY7nkZ7pvpksd2VsaW5rLCs4Ni0xNTM5OTQxNDg2NCxFMTAwMDQ3MTE2IiwicGFzc3dvcmQiOiJ6cmdqXzAwMSIsImlkIjoiNjAwNTIzNCIsImlhdCI6MTY0MjEyMDA5OSwianRpIjoiNWYzOWNlZmUtMGVjOC00ZTY3LWE5ZGItNDU3MzMxNWFkODYwIiwidXNlcm5hbWUiOiLmnY7nkZ7pvpksd2VsaW5rLCs4Ni0xNTM5OTQxNDg2NCxFMTAwMDQ3MTE2In0.nLzQOjHOvxk2cOHoVfh91fEXy8cGHJNZlXCGmh0b6T0"
        }

        data = {
            "version": "1.0",
            "f_header": {
                "access_token": "wxfd9f5f0f4fa9fafd",
                "corp_uuid": "corp_1",
                "agent_uuid": "2f287992ea4d4b5384ca",
               # "scene_uuid": "24341dcf451e42789a75",
                "scene_uuid":"f384e3ff76cf45f5882b",
                "receiver_type": 1,
                "send_type": 2
            },
            "v_header": {
                "lob_numbers":num
                    #["0000275324"]
            },
            "payload": [
                # {
                #     "title": "API自动化测试结果提醒(点击查看百度网页）",
                #     "name": name,
                #     "urlType": "html",
                #     #"urlPath": 'http://localhost:63342/API/report/file_service/20220117134755.html?_ijt=okocmp0p5r4vnpogpu8pbjf4sb'
                #     "urlPath":"http://www.baidu.com"
                # }
                {

                    "title": "API自动化测试结果提醒",
                    "productName":productName,  #产品名称
                    "result":result,  #运行结果
                    "name":"",
                    "statistics":"【统计】",
                    "totalCount":totalCount ,  #合计数量
                    "passedCount":passedCount,  #passed数量
                    #"failedCoutn":int(num_fa(file_pa)),   #failed数量
                    "failedCoutn": totalCount-passedCount,
                    "coverage":'{:.2f}%'.format(passedCount/totalCount*100),  #百分比
                    "codeBase":"【代码仓库】",
                    "codeBaseu":codeBaseu,
                    "time":"【运行时间】",
                    "timeu":timeu,
                    "explain":"若结果有失败请尽快修复，确保在上线前无问题",
                    "contactName":contactName,
                    "report":"【点击查看报告详情】",
                    # "urlType": "html",
                    # "urlPath": urlPath
                    #"urlPath": "http://192.168.1.7/api/20211130164559.html"
                }
            ]
        }
        rec = requests.post(url, params=par, json=data)
        print(rec.text)
        sleep(1)
    except:
        pass

