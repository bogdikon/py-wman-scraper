import wmanscraper
url = "192.168.0.106"
isup = wmanscraper.test_for_webman(url)
cpu = wmanscraper.get_current_temp_cpu(url)
rsx = wmanscraper.get_current_temp_rsx(url)
hdd = wmanscraper.get_free_hdd_space(url)
cooler = wmanscraper.get_fan_speed(url)
ram = wmanscraper.get_free_ram(url)
firmware = wmanscraper.get_firmware_info(url)
titlename = wmanscraper.get_current_game(url, "name")
titleid = wmanscraper.get_current_game(url, "id")


print("is system up: " + str(isup))
print("cpu temp: " + str(cpu))
print("rsx temp: " + str(rsx))
print("free hdd space: " + str(hdd) + " GB")
print("free ram: " + str(ram) + " KB")
print("fan speed: " + str(cooler) + "%")

print()
print("firmware: " + firmware)

print()
print("title name: " + titlename)
print("title id: " + titleid)
