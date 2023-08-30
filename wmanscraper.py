# Webman info scraper library, written by Bogdikon_ with <3

from bs4 import BeautifulSoup
import requests
import re

headers = {"User-Agent": "Mozilla/5.0"} # Just in case


def test_for_webman(ip):
    url = f'http://{ip}'
    try:  # test if ANY webpage is running on given IP
        response = requests.get(url, headers=headers)
    except ConnectionError:
        return False
    if response is not None:
        soup = BeautifulSoup(response.text, 'html.parser')
        pagetitle = str(soup.find('title'))  # default type is bs4.element.tag, needs to be string
        if 'wMAN' in pagetitle or 'webMAN' in pagetitle:  # test for known value in <title>
            return True
        else:  # a webpage was found, but does not satisfy check to belong to webman
            return False


def get_current_temp_cpu(ip):
    url = f"http://{ip}/cpursx.ps3?/sman.ps3"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    thermaldata = str(soup.find("a", href="/cpursx.ps3?up"))
    cpu = re.search('CPU(.+?)C', thermaldata)
    try:
        cpu = cpu.group(0)
        return cpu
    except AttributeError:
        return False


def get_current_temp_rsx(ip):
    url = f"http://{ip}/cpursx.ps3?/sman.ps3"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    thermaldata = str(soup.find("a", href="/cpursx.ps3?up"))
    rsx = re.search('RSX(.+?)C', thermaldata)
    try:
        rsx = rsx.group(0)
        return rsx
    except AttributeError:
        return False


# def get_current_temp_cpu_fahrenheit(ip):
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

# def get_current_temp_rsx_fahrenheit(ip):
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

def get_fan_speed(ip):
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
    hdd_space_split = hdd_space.split(" ") # Removing additional useless strings to return pure float
    hdd_space_int = hdd_space_split[2]
    try:
        return float(hdd_space_int)
    except AttributeError:
        return False


def get_free_ram(ip):
    url = f"http://{ip}/cpursx.ps3?/sman.ps3"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    try:
        ram = str(soup.find("a", href="/browser.ps3$slaunch").get_text()) # If in XMB
    except AttributeError:
        ram = str(soup.find("a", href="/games.ps3").get_text()) # If in-game
    ram_split = ram.split(" ") # Removing useless info...
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
    firmware_safe = firmware.split("PSID") # You dont need to share your PSID and IDPS, arent you? :D
    try:
        return str(firmware_safe[0])
    except AttributeError:
        return False

def get_current_game(ip, param):
    url = f"http://{ip}/cpursx.ps3?/sman.ps3"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    if soup.find("a", target="_blank"):
        titleid = soup.find("a", target="_blank")
        titlename = soup.find("a", target="_blank").find_next_sibling()
        titlename = str(titlename).replace("\n", "")
        try:
            titleid = re.search('>(.*)<', str(titleid)).group(1)  # remove surrounding HTML
            titlename = re.search('>(.*)<', str(titlename)).group(1)
            if re.search('(.+)[0-9]{2}.[0-9]{2}', titlename) is not None:  # remove game version info if present
                titlename = re.search('(.+)[0-9]{2}.[0-9]{2}', titlename).group(1)
            if param == "id":
                return titleid
            elif param == "name":
                return titlename
            # match param:     UNAVAILABLE IN PYTHON < 3.10
            #    case "id": # If you need titleid
            #        return titleid
            #    case "name": # If you need only game name
            #        return titlename
        except AttributeError:
            return False

    elif test_for_webman(ip): # If cant find the game
        return "XMB" # xmb
    else:
        return None
