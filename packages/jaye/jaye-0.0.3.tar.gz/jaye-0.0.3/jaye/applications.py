# output : pd.DataFrame
# index : datetime
# dtype : float64
from .settings import *
# from .subclass import acct, comm, company
from .Jaye import *

from datetime import datetime, date, time, timedelta
from dateutil.parser import parse
from pytz import timezone, utc

import numpy as np
import pandas as pd
import requests
import json
import os

class cash:
    def __init__(self):
        self.tx = pd.DataFrame()
        self.token = ""

    def balance(self):
        url = BASE_URL_ACCOUNT + "/cash/balance/"
        headers = {'Authorization': self.token}
        response = requests.get(url, headers=headers)
        return response.json()


    def transaction(self):
        return self.tx


class account:
    def __init__(self,jaye):
        self.cash = cash()
        self.is_login = False
        self.myinfo = {}
        self.jaye = jaye

    def login(self, jaye_account,password):
        # 로그인 중이라면 중복 로그인 방지
        if self.is_login == True:
            print('접속 중인 기존 계정을 로그아웃하십시오')
            return None

        # 로그 아웃 상태라면 로그인 실행
        url = BASE_URL_ACCOUNT + '/accounts/login/'
        data = {"jaye_account":jaye_account,"password":password}
        # 로그인 실패 시 return으로 함수 실행 중단

        headers = {"accept" : 'application/json', 'content-type' : 'application/json;charset=UTF-8'}
        response= requests.post(url,data = json.dumps(data),headers = headers)
        self.myinfo = response.json()

        user_token = 'token ' + self.myinfo["token"]


        self.cash.token = user_token
        self.jaye.analysis.token = user_token
        self.is_login = True

    def logout(self):
        url = BASE_URL_ACCOUNT + '/accounts/logout/'
        response = requests.post(url)
        self.cash = cash()
        self.is_login = False
        self.myinfo = {}
        # parents instance jaye
        self.jaye.analysis = analysis()
        # self.jaye.trade = trade()
        # self.jaye.simulation = simulation()

class analysis:
    def __init__(self):
        self.token = ''
        pass

    @property
    def assets(self):
        url = BASE_URL_PUBLIC + "/analysis/assets/"
        headers = {'Authorization': self.token}
        response = requests.get(url, headers=headers)
        try:
            df_assets = pd.DataFrame(response.json())
        except json.JSONDecodeError:
            print('JSONDecodeError occured')
            return None
        except:
            print(response.json())
            return None

        return df_assets

    def factor_history(self,symbol,start,end):

        url = BASE_URL_PUBLIC + f"/analysis/factor-history/?company={symbol}&from={start}&to={end}"
        headers = {'Authorization': self.token}
        response = requests.get(url, headers=headers)
        try:
            df_factor_history = pd.DataFrame(response.json())
        except json.JSONDecodeError:
            print('JSONDecodeError occured')
            return None
        except:
            print(response.json())
            return None

        return df_factor_history

    def factors(self, symbol_list):
        url = BASE_URL_PUBLIC + f"/analysis/factors/?code_list={'%2C'.join(symbol_list)}"
        headers = {'Authorization': self.token}
        response = requests.get(url, headers=headers)
        try:
            df_factors = pd.DataFrame(response.json())
        except json.JSONDecodeError:
            print('JSONDecodeError occured')
            return None
        except:
            print(response.json())
            return None

        return df_factors

    def fundamental(self,symbol,start,end):
        url = BASE_URL_PUBLIC + f"/analysis/fundamental/?company={symbol}&from={start}&to={end}"
        headers = {'Authorization': self.token}
        response = requests.get(url, headers=headers)
        try:
            df_fundamental = pd.DataFrame(response.json())
        except json.JSONDecodeError:
            print('JSONDecodeError occured')
            return None
        except:
            print(response.json())
            return None

        return df_fundamental

    def market(self,symbol,start,end):
        url = BASE_URL_PUBLIC + f"/analysis/market/?company={symbol}&from={start}&to={end}"
        headers = {'Authorization': self.token}
        response = requests.get(url, headers=headers)
        try:
            df_market = pd.DataFrame(response.json())
        except json.JSONDecodeError:
            print('JSONDecodeError occured')
            return None
        except:
            print(response.json())
            return None

        return df_market

class trade:
    def __init__(self):
        pass


class simulation:
    def __init__(self):
        pass

