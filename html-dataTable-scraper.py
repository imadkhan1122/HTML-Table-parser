import time
import time
import csv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import urllib
from urllib import request
import os
import re


class GET_PDF_FILES:
    def __init__(self):
        self.Dir = input('Enter input directory path where files will download!')
        if not os.path.exists(self.Dir): 
            os.mkdir(self.Dir)
        self.options = Options()
        self.options.headless = True
        self.main()
    
    def download_files(self, Pth, lnk):
        request.urlretrieve(lnk, Pth)
        return
    
    def get_com_urls(self,URL, pth):   
        # open chrome browser
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=self.options)
        # Go to given URL
        driver.get(URL)
        # wait for 10 seconds
        delay = 10 # seconds
        try:
            # wait untill page loads
            WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'DataTables_Table_0_length')))
            # locate and extract name of the firm
            firm_name = driver.find_element_by_css_selector("h1.content-title.text-center").text
            firm_pth = re.sub('\W+',' ', firm_name)
            firm_pth = pth +'/' + firm_pth
            # if firm name not exists in the base folder, create it.
            if not os.path.exists(firm_pth):
                os.mkdir(firm_pth)
            # Scroll page down to starting point of the table
            Strt = driver.find_element_by_id("DataTables_Table_0_length")
            actions = ActionChains(driver)
            actions.move_to_element(Strt).perform()
            time.sleep(2)
            # go to options
            select = Select(driver.find_element_by_css_selector("select.form-control.input-sm"))
            # select All 
            select.select_by_value("-1")
            time.sleep(2)
            # locate all the table
            table = driver.find_element_by_css_selector('table#DataTables_Table_0')
            # locate all rows of the table
            rows = table.find_elements_by_css_selector('tr')
            # loop over the rows of the table
            for row in rows:
                # skip first row which is table attributes
                if row != rows[0]:
                    try:
                        # locate first column of all rows one by one and expands all rows
                        col = row.find_elements_by_css_selector('td')[0].click()
                    except:
                        pass
            p_rows = table.find_elements_by_css_selector('tr.parent')
            c_rows = table.find_elements_by_css_selector('tr.child')
            for p_row, c_row in zip(p_rows, c_rows):
                try:
                    # subdirectory by name of entity
                    entity_col = p_row.find_elements_by_css_selector('td')[1].text
                    inc_name = firm_pth +'/' + entity_col
                    if not os.path.exists(inc_name):
                        os.mkdir(inc_name)
                    # subdirectory1 of entity by type of document
                    loc1 = inc_name +'/' + "Diagnostic Most Recent Letter of Authorization and Date EUA Original Issue"
                    if not os.path.exists(loc1):
                        os.mkdir(loc1)
                    file1_N = p_row.find_elements_by_css_selector('td')[2].text
                    file_link1 = p_row.find_elements_by_css_selector('td>a')[2].get_attribute('href')
                    file1_N = re.sub('\W+',' ', file1_N)
                    pth1 = loc1+ "/" + file1_N + '.pdf'
                    self.download_files(pth1, file_link1)
                    # subdirectory2 of entity by type of document
                    loc2 = inc_name +'/' + "Authorization Documents"
                    if not os.path.exists(loc2):
                        os.mkdir(loc2)
                    file_link2 = p_row.find_elements_by_css_selector('td')[5]
                    link2 = [[name.text,link.get_attribute('href')] for name, link in zip(file_link2.find_elements_by_tag_name('a'),
                                file_link2.find_elements_by_css_selector('a'))]
                    for ele in link2:
                        if link2 != []:
                            name = ele[0]
                            link = ele[1]
                            Name = re.sub('\W+',' ', name)
                            F_Name = loc2+'/'+Name+'.pdf'
                            self.download_files(F_Name, link)
                    # subdirectory3 of entity by type of document
                    loc3 = inc_name +'/' + "Other Documents"
                    if not os.path.exists(loc3):
                        os.mkdir(loc3)
                    Other_file = c_row.find_element_by_css_selector('td.child>ul.dtr-details>li>span.dtr-data>ul')
                    Other_files = [[name.text,link.get_attribute('href')] for name, link in zip(Other_file.find_elements_by_tag_name('a'), 
                                Other_file.find_elements_by_css_selector('li>a'))]
                    for ele in Other_files:
                        if Other_files != []:
                            name = ele[0]
                            link = ele[1]
                            Name = re.sub('\W+',' ', name)
                            F_Name = loc3+'/'+Name+'.pdf'
                            self.download_files(F_Name, link)
                except:
                    pass    
            End = driver.find_element_by_id("DataTables_Table_0_info")
            actions.move_to_element(End).perform()
            time.sleep(2)
            
        except TimeoutException:
            print ("Loading took too much time!")

        driver.quit()
    def main(self):
        url1 = 'https://www.fda.gov/medical-devices/coronavirus-disease-2019-covid-19-emergency-use-authorizations-medical-devices/in-vitro-diagnostics-euas-molecular-diagnostic-tests-sars-cov-2'
        url2 = 'https://www.fda.gov/medical-devices/coronavirus-disease-2019-covid-19-emergency-use-authorizations-medical-devices/in-vitro-diagnostics-euas-antigen-diagnostic-tests-sars-cov-2'
        url3 = 'https://www.fda.gov/medical-devices/coronavirus-disease-2019-covid-19-emergency-use-authorizations-medical-devices/in-vitro-diagnostics-euas-serology-and-other-adaptive-immune-response-tests-sars-cov-2'
        lst = [url1, url2, url3]
        for url in lst:
            self.get_com_urls(url, self.Dir)
        return



GET_PDF_FILES()