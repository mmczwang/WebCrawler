import requests
from bs4 import BeautifulSoup
from lxml import etree
import pandas as pd
import csv
import time


mylist = open(r'Galveston_num.csv', 'r')
datastring = mylist.read()
parcelid = datastring.split('\n')

ParNum, MailAddr, LegalDesc, CurLevy, CurAMD, PYearAMD, TtlAMD, LawSuit = [], [], [], [], [], [], [], []
MktVal, LandVal, ImpVal, CapVal, AgrVal = [], [], [], [], []

for parID in parcelid:
    url = 'https://actweb.acttax.com/act_webdev/galveston/showdetail2.jsp?can='+parID
    request_headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        # 'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
    }

    try:
        r = requests.get(url, headers=request_headers)
        soup = BeautifulSoup(r.content, 'html.parser')

        rl = soup.find(string='Improvement Value:').find_previous('td')
        ll = soup.find(string='Legal Description:').find_previous('td')

        rlh3 = rl.find_all('h3')
        try:
            Market_val = rlh3[2].get_text().strip()
            # print(Market_val)
        except:
            Market_val = 0

        try:
            Land_val = rlh3[3].get_text().strip()
            # print(Land_val)
        except:
            Land_val = 0

        try:
            Impro_val = rlh3[4].get_text().strip()
            # print(Impro_val)
        except:
            Impro_val = 0

        try:
            Cap_val = rlh3[5].get_text().strip()
            # print(Cap_val)
        except:
            Cap_val = 0

        try:
            Agr_val = rlh3[6].get_text().strip()
            # print(Agr_val)
        except:
            Agr_val = 0


        llh3 = ll.find_all('h3')
        try:
            Par_num = llh3[0].get_text().strip()
            print(Par_num)
        except:
            Par_num = 'n/a'

        try:
            mail_addr = llh3[2].get_text().strip().replace('\r\n', '').replace('Address:', '')
            mail_addr = mail_addr.strip()
            # print(mail_addr)
        except:
            mail_addr = 'n/a'

        try:
            legal_desc = llh3[4].get_text().strip().replace('\r\n', '').replace('Legal Description:', '')
            legal_desc = legal_desc.strip()
            # print(legal_desc)
        except:
            legal_desc = 'n/a'

        try:
            current_levy = llh3[5].get_text().strip().replace('\r\n', '')
            # print(current_levy)
        except:
            current_levy = 0

        try:
            current_amd = llh3[6].get_text().strip().replace('\r\n', '')
            # print(current_amd)
        except:
            current_amd = 0

        try:
            pyad = llh3[7].get_text().strip().replace('\r\n', '')
            # print(pyad)
        except:
            pyad = 0

        try:
            tad = llh3[8].get_text().strip().replace('\r\n', '')
            # print(tad)
        except:
            tad = 0

        try:
            lawsuit = llh3[12].get_text().strip().replace('\r\n', '')
            # print(lawsuit)
        except:
            lawsuit = 'n/a'

        ParNum.append(Par_num)
        MailAddr.append(mail_addr)
        LegalDesc.append(legal_desc)
        CurLevy.append(current_levy)
        CurAMD.append(current_amd)
        PYearAMD.append(pyad)
        TtlAMD.append(tad)
        LawSuit.append(lawsuit)
        MktVal.append(Market_val)
        LandVal.append(Land_val)
        ImpVal.append(Impro_val)
        CapVal.append(Cap_val)
        AgrVal.append(Agr_val)
        # Exempt.append(Exemp)


        time.sleep(1)



    except:
        continue

data_base = pd.DataFrame()

data_base['ParNum'] = pd.Series(ParNum)
data_base['MailAddr'] = pd.Series(MailAddr)
data_base['LegalDesc'] = pd.Series(LegalDesc)
data_base['CurLevy'] = pd.Series(CurLevy)
data_base['CurAMD'] = pd.Series(CurAMD)
data_base['PYearAMD'] = pd.Series(PYearAMD)
data_base['TtlAMD'] = pd.Series(TtlAMD)
data_base['LawSuit'] = pd.Series(LawSuit)
data_base['MktVal'] = pd.Series(MktVal)
data_base['LandVal'] = pd.Series(LandVal)
data_base['ImpVal'] = pd.Series(ImpVal)
data_base['CapVal'] = pd.Series(CapVal)
data_base['AgrVal'] = pd.Series(AgrVal)


data_base.to_csv('RealEstate_data.csv', index=False, sep='|', encoding='utf-8')
