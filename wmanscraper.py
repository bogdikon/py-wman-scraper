# Webman info scraper library, written by Bogdikon_ with <3

from bs4 import BeautifulSoup
import requests
import re


headers = {"User-Agent": "Mozilla/5.0"}

def test_for_webman(ip):
        response = None
        url = f'http://{ip}'
        try:    # test if ANY webpage is running on given IP
            response = requests.get(url, headers=headers)
        except ConnectionError as e:
            print(f'No webpage found on "{ip}"')
            return False
        if response is not None:
            soup = BeautifulSoup(response.text, 'html.parser')
            pageTitle = str(soup.find('title'))     # default type is bs4.element.tag, needs to be string
            if 'wMAN' in pageTitle or 'webMAN' in pageTitle:    # test for known value in <title>
                return True
            else:   # a webpage was found, but does not satisfy check to belong to webman
                return False

def get_current_temp_cpu(ip):
    url = f"http://{ip}/cpursx.ps3?/sman.ps3"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    thermalData = str(soup.find("a", href="/cpursx.ps3?up"))
    cpu = re.search('CPU(.+?)C', thermalData)
    try:
        cpu = cpu.group(0)
        return cpu
    except AttributeError:
        return False

def get_current_temp_rsx(ip):
    url = f"http://{ip}/cpursx.ps3?/sman.ps3"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    thermalData = str(soup.find("a", href="/cpursx.ps3?up"))
    rsx = re.search('RSX(.+?)C', thermalData)
    try:
        rsx = rsx.group(0)
        return rsx
    except AttributeError:
        return False

#def get_current_temp_cpu_fahrenheit(ip):
#    url = f"http://{ip}/cpursx.ps3?/sman.ps3"
#    response = requests.get(url, headers=headers)
#    soup = BeautifulSoup(response.text, 'html.parser')
#    thermalData = str(soup.find("a", href="/cpursx.ps3?up"))
#    cpu = re.search('CPU(.+?)F', thermalData)
#    try:
#        cpu = cpu.group(0)
#        return cpu
#    except AttributeError:
#        return False

#def get_current_temp_rsx_fahrenheit(ip):
#    url = f"http://{ip}/cpursx.ps3?/sman.ps3"
#    response = requests.get(url, headers=headers)
#    soup = BeautifulSoup(response.text, 'html.parser')
#    thermalData = str(self.soup.find("a", href="/cpursx.ps3?up"))
#    rsx = re.search('RSX(.+?)F', thermalData)
#    try:
#        rsx = rsx.group(0)
#        return rsx
#    except AttributeError:
#        return False # TODO: Make these fahrenheit funcs work

def get_cooler_percent(ip):
    url = f"http://{ip}/cpursx.ps3?/sman.ps3"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    percent = str(soup.find("a", href="/cpursx.ps3?mode").get_text())
    percent_split = percent.split(" ")
    try:
        return int(percent_split[3].replace("%", ""))
    except AttributeError:
        return False

def get_free_hdd_space(ip):
    url = f"http://{ip}/cpursx.ps3?/sman.ps3"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    hdd_space = str(soup.find("a", href="/dev_hdd0").get_text())
    hdd_space_split = hdd_space.split(" ")
    hdd_space_int = hdd_space_split[2]
    try:
        return float(hdd_space_int)
    except AttributeError:
        return False

def get_free_ram(ip):
    url = f"http://{ip}/cpursx.ps3?/sman.ps3"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    ram = str(soup.find("a", href="/browser.ps3$slaunch").get_text())
    ram_split = ram.split(" ")
    ram_int = ram_split[1]
    try:
        return float(ram_int.replace(",", "."))
    except AttributeError:
        return False

def get_firmware_info(ip):
    url = f"http://{ip}/cpursx.ps3?/sman.ps3"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    firmware = str(soup.find("a", href="/setup.ps3").get_text())
    firmware_safe = firmware.split("PSID")
    try:
        return str(firmware_safe[0])
    except AttributeError:
        return False
