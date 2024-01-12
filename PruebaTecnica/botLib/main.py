#import types
#import typing
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import botLib.constants as const
import time
import traceback

class Bot(webdriver.Chrome):
    def __init__(self, teardown=False):
        self.teardown = teardown
        super(Bot, self).__init__()
        self.implicitly_wait(15)
        self.maximize_window()
        self.delete_all_cookies()
        
    def __exit__(self, exc_type , exc_val, exc_tb):
        if self.teardown:
            self.quit()

    def land_first_page(self):
        self.get(const.BASE_URL)
        
    def login(self,email,password):
        #insert email
        key = WebDriverWait(self, 5).until(
            EC.element_to_be_clickable((
                By.CSS_SELECTOR, 'input[id="session_key"]')))
        key.click()
        key.send_keys(email)
        

        #insert password
        passwrd = WebDriverWait(self, 5).until(
            EC.element_to_be_clickable((
                By.CSS_SELECTOR, 'input[id="session_password"]')))
        passwrd.click()
        passwrd.send_keys(password)
        

        self.find_element(By.CSS_SELECTOR,'button[data-id="sign-in-form__submit-btn"]').click()
        
    def search(self, search_value):
        search_bar = WebDriverWait(self,15).until(
            EC.element_to_be_clickable((
                By.CSS_SELECTOR, 'div[id="global-nav-typeahead"] > input[aria-label="Search"]'
            ))
        )
        search_bar.click()
        search_bar.send_keys(search_value)
        time.sleep(1)
        search_bar.send_keys(Keys.ENTER)
        time.sleep(2)

    def filter_companies(self):
        
        filter_list = self.find_element(By.XPATH, '//div[@id="search-reusables__filters-bar"]/ul')
        filter_list = filter_list.find_elements(By.CSS_SELECTOR, '*')
        for element in filter_list:
            if element.get_attribute('innerText') == 'Companies':
                element.click()
                break

    def filter_location(self, filter_num=1, custom_filters=['EEUU']):
        """
        Get a number. Default filter(1-5) or custom filter(6). Click the filter on web page. 
        """
        #click the button to display the filter options
        filter_button = WebDriverWait(self,5).until(
            EC.element_to_be_clickable((
                By.CSS_SELECTOR, 'button[id="searchFilter_companyHqGeo"]'
            ))
        )
        filter_button.click()
        time.sleep(1)

        #Click the desired default location
        if 0 < filter_num < 6:
            filter_button = WebDriverWait(self,5).until(
                EC.element_to_be_clickable((
                    By.XPATH, f'//div[@class="authentication-outlet"]/div[2]/section/div/nav/div/ul/li[3]/div/div/div/div[1]/div/form/fieldset/div[1]/ul/li[{int(filter_num)}]/label/p/span[1]'
                ))
            )
            filter_button.click()
        elif filter_num == 6:
            for custom_filter in custom_filters:
                filter_button = WebDriverWait(self,5).until(
                    EC.element_to_be_clickable((
                        By.XPATH, '//div[@class="authentication-outlet"]/div[2]/section/div/nav/div/ul/li[3]/div/div/div/div[1]/div/form/fieldset/div[1]/div/div/input '
                    ))
                )
                filter_button.click()
                filter_button.send_keys(custom_filter)
                drop_down = WebDriverWait(self,5).until(
                    EC.element_to_be_clickable((
                        By.XPATH, '//div[@class="authentication-outlet"]/div[2]/section/div/nav/div/ul/li[3]/div/div/div/div[1]/div/form/fieldset/div[1]/div/div/div[2]/div/div[1]'))
                )
                drop_down.click()
        else:
            print('Wrong input')

        #Send the filter    
        send_filters = WebDriverWait(self, 5).until(
            EC.element_to_be_clickable((
                By.XPATH, '//div[@class="application-outlet"]/div[3]/div[2]/section/div/nav/div/ul/li[3]/div/div/div/div[1]/div/form/fieldset/div[2]/button[2]/span'
            ))
        )
        send_filters.click()

    def filter_industry(self,filter_num=1,custom_filters=['Software']):

        filter_button = WebDriverWait(self,5).until(
            EC.element_to_be_clickable((
                By.CSS_SELECTOR, 'button[id="searchFilter_industryCompanyVertical"]'
            ))
        )
        filter_button.click()

        #Click the desired default location
        if 0 < filter_num < 6:
            filter_button = WebDriverWait(self,5).until(
                EC.element_to_be_clickable((
                    By.XPATH, f'//div[@class="authentication-outlet"]/div[2]/section/div/nav/div/ul/li[4]/div/div/div/div[1]/div/form/fieldset/div[1]/ul/li[{int(filter_num)}]/label/p/span[1]'
                ))
            )
            filter_button.click()
        elif filter_num == 6:
            for custom_filter in custom_filters:
                filter_button = WebDriverWait(self,5).until(
                    EC.element_to_be_clickable((
                        By.CSS_SELECTOR, 'div[data-basic-filter-parameter-name="industryCompanyVertical"]  fieldset input[placeholder="Add an industry"]'
                    ))
                )
                filter_button.click()
                filter_button.send_keys(custom_filter)
                drop_down = WebDriverWait(self,5).until(
                    EC.element_to_be_clickable((
                        By.CSS_SELECTOR, 'div[data-basic-filter-parameter-name="industryCompanyVertical"]  fieldset div[id*="triggered"] > div > div'))
                )
                drop_down.click()
        else:
            print('Wrong input')

        send_filters = WebDriverWait(self,5).until(
            EC.element_to_be_clickable((
                By.XPATH, '//div[@class="application-outlet"]/div[3]/div[2]/section/div/nav/div/ul/li[4]/div/div/div/div[1]/div/form/fieldset/div[2]/button[2]/span'
            ))
        )
        send_filters.click()
        
    def next_button(self,driver):
        time.sleep(2)
        driver.find_element(By.CSS_SELECTOR, 'html body').send_keys(Keys.END)
        next_button = WebDriverWait(self,5).until(
            EC.element_to_be_clickable((
                By.CSS_SELECTOR,'button[aria-label="Next"]'
            ))
        )
        print(f'Next button css selcted')
        
        print(next_button.get_attribute('class'))
        try:
            next_button.click()
        except Exception as e:
            # Catching any exception and printing the error message
            print(f"An error occurred: {e}")


    def cycle_companies(self, keywords=[]):
        try:
            time.sleep(2)
            self.find_element(By.CSS_SELECTOR, 'html body').send_keys(Keys.END)
            number_of_pages = WebDriverWait(self,5).until(
                EC.presence_of_element_located((
                    By.CSS_SELECTOR, ' ul[class*="pages--number"]'
                ))
            )
            print(f'Number of pages \n')
            number_of_pages = number_of_pages.find_elements(By.CSS_SELECTOR, 'li')
            print(f'Number of pages li\n')
            total_number_of_pages = number_of_pages[-1].find_element(By.CSS_SELECTOR, 'button > span')\
                .get_attribute('innerText')
            print(f'\ntotal number of pages\n{total_number_of_pages}')
            dict_data = {'Name':[], 'Company':[],'Company Linkedin Link':[],'Keywords':[],'Linkedin Link':[],'Is Profile Not a Connection':[],'Conect Request Sent':[]}
            #for _ in range(int(total_number_of_pages)):
            for _ in range(2):
                root = WebDriverWait(self,5).until(
                    EC.element_to_be_clickable((
                        By.CSS_SELECTOR, 'ul[class="reusable-search__entity-result-list list-style-none"]'
                    ))
                )

                companies_list = root.find_elements(By.CSS_SELECTOR, 'li')
                for company in companies_list:
                    dict_data_raw = self.open_company_profile(driver=self,company=company,keywords=keywords)
                    print(f'Dict data raw\n{dict_data_raw}')
                    if dict_data_raw:
                        dict_data['Name'].extend(dict_data_raw['Name'])
                        dict_data['Company'].extend(dict_data_raw['Company'])
                        dict_data['Company Linkedin Link'].extend(dict_data_raw['Company Linkedin Link'])
                        dict_data['Keywords'].extend(dict_data_raw['Keywords'])
                        dict_data['Linkedin Link'].extend(dict_data_raw['Linkedin Link'])
                        dict_data['Is Profile Not a Connection'].extend(dict_data_raw['Is Profile Not a Connection'])
                        dict_data['Conect Request Sent'].extend(dict_data_raw['Conect Request Sent'])
                        print('\nagregado al data base\n')
                        print(dict_data)
                

                print(f'pagina numero: {_}')
                print(f'About to click the Next button')
                #Avoid clicking an unclicable button
                #if _ < int(total_number_of_pages)-1:
                if _ < 1:
                    self.next_button(driver=self)

            return dict_data


        except Exception as e:
            print(f'An error ocurred at cycling companies:\n {e}')

    def open_company_profile(self, driver, company,keywords):
        #diccionario con todos los datos a retornar en el run.py
        dict_data = {'Name':[], 'Company':[],'Company Linkedin Link':[],'Keywords':[],'Linkedin Link':[],'Is Profile Not a Connection':[],'Conect Request Sent':[]}
        print(f'creado el dict data frame')
        company = company.find_element(By.TAG_NAME, 'a')
        company_url_raw = company.get_attribute('href')
        print(f'\nCompany url\n {company_url_raw}')
        company_url = f"{company_url_raw}/people/"


        original_window = driver.current_window_handle
        driver.switch_to.new_window('tab')
        driver.get(company_url)

        company_name = driver.find_element(By.XPATH,
                                             '//span[@dir="ltr"]')\
                                              .get_attribute('innerText')
        print(f'Company name: {company_name} \n')
        for keyword in keywords:
        
            keywords_search_bar = WebDriverWait(driver,5).until(
                EC.element_to_be_clickable((
                    By.CSS_SELECTOR, '#people-search-keywords'
                ))
            )

            keywords_search_bar.click()
            keywords_search_bar.send_keys(keyword)
            keywords_search_bar.send_keys(Keys.ENTER)

            people_window = driver.current_window_handle
            print(f'\n This is the people window: {people_window}')
            
            try:
                #Getting the list of profiles to check per keyword per company
                time.sleep(1)
                driver.find_element(By.CSS_SELECTOR, 'html body').send_keys(Keys.END)
                people_list = WebDriverWait(driver,5).until(
                    EC.element_to_be_clickable((
                        By.CSS_SELECTOR, 'div[class*="org-people-profile-card__card-spacing"]'
                    ))
                )
                cards = people_list.find_element(By.CSS_SELECTOR, 'div > div.scaffold-finite-scroll__content > ul')
                cards = cards.find_elements(By.CSS_SELECTOR, 'li')
                print(f'\nNumero de contactos a buscar: {len(cards)} \n')
                print('>----------<')
                counter = 0
                for card in cards:
                    counter = counter + 1
                    print(f'\nEntering a new card ({counter})\n')
                    #Skipping non profile cards
                    #try:
                    dict_profile = self.check_profile(driver=driver, card=card, people_window=people_window, keyword=keyword, company_name=company_name)
                    #except:
                    #    print('Error in cheking profile.. skipping this card')
                    #    continue
                    print(dict_profile)
                    if dict_profile:
                        print(f'\n Beginnig to extract check_profile returned data')
                        dict_data['Company'].append(company_name)
                        print(f'\nfirst dict_data added COmpany name')
                        dict_data['Name'].append(dict_profile['Name'])
                        print(f'\nsecond dict_data added name')
                        dict_data['Company Linkedin Link'].append(company_url_raw)
                        print(f'\nthird dict_data added name')
                        dict_data['Keywords'].append(keyword)
                        print(f'\n fourth dict_data added name')
                        dict_data['Linkedin Link'].append(dict_profile['Linkedin Link'])
                        print(f'\n fifth dict_data added name')
                        dict_data['Is Profile Not a Connection'].append(dict_profile['Is Profile Not a Connection'])
                        print(f'\n sixth dict_data added name')
                        dict_data['Conect Request Sent'].append(dict_profile['Conect Request Sent'])
                        print(f'\n Ended to extract check_profile returned data')
                        print(dict_data)
                    
                driver.close()
                #Close 2nd tab
                print(f'\nAbout to close 2nd window (tryStatement)')
                try:
                    driver.switch_to.window(people_window)
                    driver.close()
                except:
                    print(f'No peoples window found. (exceptExceptStatement)')
                print(f'\nAbout to switch to original window(tryStatement')
                driver.switch_to.window(original_window)
                    
                
                #driver.get(company_url)
            except:
                print('No profiles found for the keyword')
                driver.close()
                #Close 2nd tab
                print(f'\nAbout to close 2nd window (exceptStament)')
                try:
                    driver.switch_to.window(people_window)
                    driver.close()
                except:
                    print(f'No peoples window found. (exceptExceptStatement)')
                print(f'\nAbout to switch to original window exceptStament)')
                driver.switch_to.window(original_window)

        
        return dict_data
            

    def check_profile(self, driver, card, people_window, keyword, company_name):
        card_link = card.find_element(By.TAG_NAME, 'a')
        #Getting the profile linkedin link
        card_link = card_link.get_attribute('href')
        #print(f'card liks: {card_link}')
        driver.switch_to.new_window('tab')
        driver.get(card_link)
        print(f'Entering a new profile')
        time.sleep(1)
        card_link = str(driver.current_url)
        correct_profile = self.verify_keyword_in_profile(driver=driver,keyword=keyword,company_name=company_name)
        print(f'has the key words? --> {correct_profile}\n')
        profile_is_not_a_connection = not self.is_profile_a_connection(driver=driver)
        #is_connection_pending = self.is_connection_pending(driver=driver)
        if correct_profile :
            dict_connect = self.send_connect_req(driver=driver)
            contact_name = self.find_element(By.CSS_SELECTOR, 'h1[class*="text-heading"]')\
                .get_attribute("innerText")
            print(f'\n name of the contact: {contact_name}')

            #Close 3rd window
            time.sleep(2)
            print(f'about to close the 3rd window\n')
            driver.close()
            print(f'about to swich to the 2nd window\n')
            driver.switch_to.window(people_window)
            print(f'ending checing function\n')
            return_data = {'Linkedin Link': str(card_link),'Name':contact_name, 'Is Profile Not a Connection': profile_is_not_a_connection}
            return_data.update(dict_connect)
            return return_data
            
        elif not correct_profile:
            print(f'about to close the 3rd window\n')
            driver.close()
            print(f'about to swich to the 2nd window\n')
            driver.switch_to.window(people_window)
            print(f' checing function returning FALSE\n')
            return False


    def is_profile_a_connection(self, driver):
        #Get the div of the "connection" buttons innerHTML
        text = str( WebDriverWait(driver,5).until(
            EC.element_to_be_clickable((
                By.CSS_SELECTOR, 'main div.ph5.pb5 > div[class*="pv-top-card"] > div'
            ))
        ).get_attribute('innerHTML') )
        value = 'Remove Connection'
        if value in text:
            return True
        else:
            return False
        
    def is_connection_pending(self, driver):
        #Get the div of the "connection" buttons innerHTML
        text = str( WebDriverWait(driver,5).until(
            EC.element_to_be_clickable((
                By.CSS_SELECTOR, 'main div.ph5.pb5 > div[class*="pv-top-card"] > div'
            ))
        ).get_attribute('innerHTML') )
        value = 'Pending'
        if value in text:
            return True
        else:
            return False

    
    def verify_keyword_in_profile(self, driver, company_name=None, keyword=None):
            experience_list = WebDriverWait(driver,5).until(
                EC.element_to_be_clickable((
                    By.CSS_SELECTOR, 'main > section div[id="experience"] ~ div > ul'))
            )
            experience_list = experience_list.find_elements(By.CSS_SELECTOR, 'li')
            correct_profile = False
            text = ''
            for element in experience_list:
                #Name of the company in the current experience card of the profile
                time.sleep(2)
                searched_company_name = str(element.find_element(By.CSS_SELECTOR, 'div[class*="display-flex flex-column full-width"] > div > div > span > span').get_attribute("innerText"))
                print(f'\n searched company name: {searched_company_name}')
                searched_company_name = searched_company_name.lower()
                company_name = company_name.lower()
                if company_name in searched_company_name:
                    text = text + str(element.get_attribute('innerText')).lower()
                    break
            keyword = keyword.lower()
            if company_name and keyword in text:
                correct_profile = True
            return correct_profile
    
    def send_connect_req(self, driver ):
        try:
            connect_button = WebDriverWait(driver,5).until(
                        EC.element_to_be_clickable((
                            By.CSS_SELECTOR, 'div.pv-top-card-v2-ctas button[aria-label*="to connect"] > span'
                        ))
                    )
        except:
            try:
                more_button = connect_button = WebDriverWait(driver,5).until(
                        EC.element_to_be_clickable((
                            By.CSS_SELECTOR, 'div[class*="pv-top-card-v2"] button[aria-label*="More"] span'
                        ))
                    )
                more_button.click()
                connect_button = WebDriverWait(driver,5).until(
                        EC.element_to_be_clickable((
                            By.CSS_SELECTOR, 'div[class*="pv-top-card-v2-ctas"] div[class*="artdeco-dropdown"] ul div[aria-label*="connect"] span'
                        ))
                    )
            except:
                pass
        connect_button.click()

        #Send connect request without a note
        connect_button = WebDriverWait(driver,5).until(
            EC.element_to_be_clickable((
                By.CSS_SELECTOR, 'button[aria-label="Send now"]'
            ))
        )
        #connect_button.click()
        return {'Conect Request Sent' : False}

    def check_contact_list(self,df,email,password):
        self.land_first_page()
        self.login(email=email,password=password)
        for i in range(len(df)):
            link = df.loc[i,'Linkedin Link']
            self.get(link)
            is_connection = self.is_profile_a_connection(driver=self)
            is_connection_pending = self.is_connection_pending(driver=self)

            if not is_connection and not is_connection_pending:
                send_req = self.send_connect_req(driver=self)
                df.loc[i,'Conect Request Sent'] = send_req['Conect Request Sent']
                pass
            elif not is_connection and is_connection_pending:
                df.loc[i,'Conect Request Sent'] = True
                df.loc[i,'Is Profile Not a Connection'] = True
            else:
                df.loc[i,'Conect Request Sent'] = True
                df.loc[i,'Is Profile Not a Connection'] = False
        return df