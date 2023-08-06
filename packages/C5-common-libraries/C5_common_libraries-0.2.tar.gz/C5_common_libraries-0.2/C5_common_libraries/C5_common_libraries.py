#!/usr/bin/env python
# coding: utf-8

# In[1]:



CPU_list = ['Core i9','Core i7','Core i5','Core 2','Celeron','Pentium','AMD Ryzen 7','AMD Ryzen 5','AMD Ryzen 3','AMD Ryzen','AMD Athlon','Intel Xeon']
Memory_list = ['4GB','8GB','16GB','32GB','64GB']
Storage_list = ['128GB','256GB','500GB','512GB','1TB','2TB']
        
Notebooks = ['ThinkPad','ThinkBook','IdeaPad', 'Legion']
Desktops = ['ThinkCentre','IdeaCentre','Yoga']
CatchPhrase = {'NB no office':'ノートパソコン Windows11 公式レノボ直販','NB with office':'ノートパソコン Windows11 公式レノボ直販 Office付き','DT no office':'デスクトップパソコン Windows11 公式レノボ直販','DT with office':'デスクトップパソコン Windows11 公式レノボ直販 Office付き','Gaming NB no office':'ゲーミングノートPC Windows11 公式レノボ直販','Gaming DT no office':'ゲーミングノートPC Windows11 公式レノボ直販 Office付き','Gaming DT no office':'デスクトップゲーミングPC Windows11 公式レノボ直販','Gaming DT with office':'デスクトップゲーミングPC Windows11 公式レノボ直販 Office付き','Tablet':'タブレット Android 公式レノボ直販'}
    

class EA:      
    def Element_action(driver,action,xpath):
        if action == 'click':
            driver.find_element_by_xpath(xpath).click()    
        if action == 'clear':
            driver.find_element_by_xpath(xpath).clear() 
        if action == 'read':
            text = driver.find_element_by_xpath(xpath).text
            return text
    
def Xlsx_to_CSV(excel_name,csv_name):
    """
    Use this library to convert xlsx to csv
    """
    import pandas as pd
    import sys
    #read_file = pd.read_excel(excel_name,encoding="utf8")
    read_file = pd.read_excel(excel_name)
    read_file.to_csv (csv_name, index = None, header=True,encoding ='utf-8-sig')
    
    
def FTP_File_Upload(FTP_HOST,FTP_USER,FTP_PASS,FTP_path,file):
    """
    Use this library to upload a file to FTP location
    """
    from ftplib import FTP
    from pathlib import Path

    with FTP(FTP_HOST, FTP_USER, FTP_PASS) as ftp, open(FTP_path, 'rb') as file:
        ftp.encoding = "utf-8"
        ftp.port = 21
        ftp.storbinary(f'STOR {FTP_path.name}', file)
        

