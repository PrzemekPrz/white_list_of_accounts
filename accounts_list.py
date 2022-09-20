import json
import requests
import pandas as pd
import datetime

def white_list_of_accounts():
    """
    List of VAT taxpayers, i.e. a list of registered
    and unregistered entities as well as entities removed
    and returned to the VAT register.
    Shared by the Ministry of Finance in PL
    """
    file = pd.read_excel(r'C:') # give the path to the file xlsx, with name of column "Accounts"
    accounts_list = file['Accounts'].values.tolist()
    today = datetime.date.today()
    time = today.strftime('%Y-%m-%d')
    container = []
    for account in accounts_list:
        url = f'https://wl-api.mf.gov.pl/api/search/bank-accounts/{account}?date={time}'
        response = requests.get(url)
        dbase = json.loads(response.text)
        if len(dbase['result']['entries'][0]['subjects']) != 0:
            array = []
            array.append(account)
            var_1 = dbase['result']['entries'][0]['subjects'][0]['name']
            array.append(var_1)
            np = dbase['result']['entries'][0]['subjects'][0]['nip']
            array.append(np)
            container.append(array)
        else:
            array_1 = []
            array_1.append(account)
            var_2 = 'empty'
            array_1.append(var_2)
            container.append(array_1)

    df = pd.DataFrame(container)
    df.columns = ['Accounts', 'Name', 'Nip_number']
    df.to_excel('./accounts.xlsx')
    print('Save to excel')
white_list_of_accounts()