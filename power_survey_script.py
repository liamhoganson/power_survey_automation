# Imports
import os
import pynipap
from pynipap import AuthOptions, VRF, Pool, Prefix
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import get_form_responses

# Defining Variables
get_dicitonary = get_form_responses.get_form_responses()
load_dotenv("env_vars.env")
username = os.getenv('USERNAME')
passwd = os.getenv('PASSWD')
PDU_PASSWORD = os.getenv("PDU_PASS")
NIPAP_SERVER = os.getenv("NIPAP_SERVER")
options = Options()
driver = webdriver.Firefox(options=options)

# Nipap Auth
def establish_nipap_connection(user, password, server):
    pynipap.xmlrpc_uri = (f"http://{user}:{password}@"+server+":1337/XMLRPC")
    return pynipap.AuthOptions({'authoritative_source': user+'_client'})
a = establish_nipap_connection(username, passwd, NIPAP_SERVER)


# Get PDU IP Address(es) from NIPAP
def get_pdus(site):
    search_query_options = {
        'val1': 'inherited_tags',
        'operator': 'equals_any',
        'val2': 's-'+site
    }
    pdu_search_query = Prefix.smart_search('172.16.0.0/12', extra_query=search_query_options, search_options={'max_result': 1000, 'include_all_children': True, 'include_all_parents': True})
    pdu_query_results = pdu_search_query['result']
    pdu_results = {pdu.node: pdu.prefix for pdu in pdu_query_results if pdu.node is not None and ('pdu' in pdu.node)}
    pdu_names = list(pdu_results.keys())
    pdu_results = list(pdu_results.values())
    pdu_results = [value[:-3] for value in pdu_results]
    return pdu_results


# ICT Function
def ICT(element):

    # ICT port-to-xpath dictionary
    port_to_xpath_mapping = {
        'Port 1 or PFLUX (Slot 1/ Port 1)': "/html/body/div/div/div/div/div/div[3]/form/div[2]/table/tbody/tr[1]/td[1]/input",
        'Port 2': "/html/body/div/div/div/div/div/div[3]/form/div[2]/table/tbody/tr[2]/td[1]/input",
        'Port 3': "/html/body/div/div/div/div/div/div[3]/form/div[2]/table/tbody/tr[3]/td[1]/input",
        'Port 4': "/html/body/div/div/div/div/div/div[3]/form/div[2]/table/tbody/tr[4]/td[1]/input",
        'Port 5  or PFLUX (Slot 2/ Port 1)': "/html/body/div/div/div/div/div/div[3]/form/div[2]/table/tbody/tr[5]/td[1]/input",
        'Port 6': "/html/body/div/div/div/div/div/div[3]/form/div[2]/table/tbody/tr[6]/td[1]/input",
        'Port 7': "/html/body/div/div/div/div/div/div[3]/form/div[2]/table/tbody/tr[1]/td[3]/input",
        'Port 8': "/html/body/div/div/div/div/div/div[3]/form/div[2]/table/tbody/tr[2]/td[3]/input",
        'Port 9   or PFLUX (Slot 3/ Port 1)': "/html/body/div/div/div/div/div/div[3]/form/div[2]/table/tbody/tr[3]/td[3]/input",
        'Port 10': "/html/body/div/div/div/div/div/div[3]/form/div[2]/table/tbody/tr[4]/td[3]/input",
        'Port 11': "/html/body/div/div/div/div/div/div[3]/form/div[2]/table/tbody/tr[5]/td[3]/input",
        'Port 12': "/html/body/div/div/div/div/div/div[3]/form/div[2]/table/tbody/tr[6]/td[3]/input"
    }
    
    try:
        driver.get(f'http://admin:{PDU_PASSWORD}@' + pdu)
    except:
        driver.get('http://' + pdu)
        driver.switch_to.alert.send_keys("admin")
        driver.switch_to.alert.send_keys(Keys.TAB)
        driver.switch_to.alert.send_keys(PDU_PASSWORD)
        driver.switch_to.alert.accept()

    only_ports = [e for e in element if 'Port' in e and 'RTR' not in e]
    for port in only_ports:
        if port in port_to_xpath_mapping:
            driver.implicitly_wait(5)
            xpath = port_to_xpath_mapping[port]
            driver.find_element(By.XPATH, '/html/body/div/div/div/div/div/div[2]/div/a[2]').click()
            driver.find_element(By.XPATH, xpath).click()
            label_button = driver.find_element(By.XPATH, '//*[@id="nx"]')
            label_button.click()
            label_button.send_keys(element[port])
            print(f"Successfully filled {element[port]} for {port}")
        elif port not in port_to_xpath_mapping:
            print(f"{port} not in list. Skipping")

# SynAccess Function   
def Syn_Access(element):
    driver.get('http://' + pdu)
    driver.switch_to.alert.send_keys("admin")
    driver.switch_to.alert.send_keys(Keys.TAB)
    driver.switch_to.alert.send_keys(PDU_PASSWORD)
    driver.switch_to.alert.accept()


# PacketFlux Function
def Packet_Flux():

    # Packet Flux Button Variables
    list_of_buttons = [
        "/html/body/div/div[2]/div[1]/div[1]/header/span",
        "/html/body/div/div[2]/div[1]/div[2]/header/span",
        "/html/body/div/div[2]/div[1]/div[3]/header/span",
        "/html/body/div/div[2]/div[1]/div[4]/header/span",
        "/html/body/div/div[2]/div[2]/div[1]/header/span",
        "/html/body/div/div[2]/div[2]/div[2]/header/span",
        "/html/body/div/div[2]/div[2]/div[3]/header/span",
        "/html/body/div/div[2]/div[2]/div[4]/header/span",
        "/html/body/div/div[2]/div[3]/div[1]/header/span",
        "/html/body/div/div[2]/div[3]/div[2]/header/span",
        "/html/body/div/div[2]/div[3]/div[3]/header/span",
        "/html/body/div/div[2]/div[3]/div[4]/header/span",
        "/html/body/div/div[2]/div[4]/div[1]/header/span",
        "/html/body/div/div[2]/div[4]/div[2]/header/span",
        "/html/body/div/div[2]/div[4]/div[3]/header/span",
        "/html/body/div/div[2]/div[4]/div[4]/header/span"
    ]

    try:
        driver.get('http://' + pdu)
        WebDriverWait(driver, 3).until(EC.alert_is_present())
        driver.switch_to.alert.accept()
        driver.switch_to.alert.send_keys("admin"+ Keys.TAB + PDU_PASSWORD)
        driver.switch_to.alert.accept(expected_text=None, text_to_write=None)
    except:
        print ("")

    only_ports = [e for e in element if 'Port' in e and 'RTR' not in e]
    for keys, button in (zip(only_ports, list_of_buttons)):
        driver.find_element(By.XPATH, button).click()
        input_button = driver.find_element(By.XPATH, '/html/body/div/div[2]/div[5]/div/form/div/input[1]')
        input_button.click()
        input_button.send_keys(element[keys])
        cancel_button = driver.find_element(By.XPATH, '/html/body/div/div[2]/div[5]/div/form/button[2]')
        cancel_button.click()

# Digital Logger Function
def Digital_Logger():
    driver.get('http://' + pdu)
    driver.switch_to.alert.send_keys("admin")
    driver.switch_to.alert.send_keys(Keys.TAB)
    driver.switch_to.alert.send_keys(PDU_PASSWORD)
    driver.switch_to.alert.accept()
    driver.switch_to.active_element

# CyberPower Function
def Cyber_Power():
    driver.get('http://' + pdu)
    driver.switch_to.alert.send_keys("admin")
    driver.switch_to.alert.send_keys(Keys.TAB)
    driver.switch_to.alert.send_keys(PDU_PASSWORD)
    driver.switch_to.alert.accept()



# Main function to 'probe' the PDU to determine it's type.
for element, pdu in (zip(get_dicitonary, get_pdus(get_dicitonary[0]['Site Slug (Example: brtn)']))):
    print(pdu, element)
    driver.get(f'http://admin:{PDU_PASSWORD}@' + pdu)
    driver.implicitly_wait(10)
    title_element = driver.find_element(By.TAG_NAME, 'title')
    title_text = title_element.get_attribute('text')
    
    # Run ICT Function
    if "ICT" in title_text:
        ICT(element)

    # Run Synaccess Function
    elif "Synaccess" in title_text:
        Syn_Access(element)

    # Run CyberPower Function    
    elif "PDU Remote Management" in title_text:
        Cyber_Power(element)

    # Run PacketFlux Function    
    elif "PacketFlux" in title_text:
        Packet_Flux()
#driver.quit()