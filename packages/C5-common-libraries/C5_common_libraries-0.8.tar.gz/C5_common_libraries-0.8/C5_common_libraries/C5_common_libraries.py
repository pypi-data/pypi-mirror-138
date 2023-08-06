#!/usr/bin/env python
# coding: utf-8

# In[1]:

class EA:
    """
    Use this method to convert perform click, clear or read operation on web elements.
    input parameters :
    1) driver : selenium webdriver instance
    2) action : action on the webelement in string form ('read','click','clear')
    3) Dict : Input in the form of a dictionary where keys are name of the element and values are their respective xpaths
    """
    def Element_action(driver,action,Dict):

        element_names = list(Dict.keys())
        List_of_values = []
        for e in element_names:
            xpath = Dict[e]
            #print(e ," : ", Dict[e])
            if action == 'click':
                driver.find_element_by_xpath(xpath).click()
            if action == 'clear':
                driver.find_element_by_xpath(xpath).clear()
            if action == 'read':
                try:
                    Value = driver.find_element_by_xpath(xpath).text
                    print(Value)
                except:
                    Value = 'Element not found : ' + str(e)
            #
            #Dict_2 creation key:e, value: Value
        
            List_of_values.append(Value)
        return List_of_values

class Xlsx_to_CSV:
    def Xlsx2CSV(excel_name,csv_name):
        """
        Use this method to convert xlsx to csv
        input parameters:
        1) excel_name : file path of the excel to be converted.
        2) csv_name : file path of the new csv file.
        """
        import pandas as pd
        import sys
        #read_file = pd.read_excel(excel_name,encoding="utf8")
        read_file = pd.read_excel(excel_name)
        read_file.to_csv (csv_name, index = None, header=True,encoding ='utf-8-sig')
    

class FTP_File_Upload:
    def File_Upload(FTP_HOST,FTP_USER,FTP_PASS,FTP_path,file):
        """
        Use this method to upload a file to FTP location.
        
        """
        from ftplib import FTP
        from pathlib import Path

        with FTP(FTP_HOST, FTP_USER, FTP_PASS) as ftp, open(FTP_path, 'rb') as file:
            ftp.encoding = "utf-8"
            ftp.port = 21
            ftp.storbinary(f'STOR {FTP_path.name}', file)
        

