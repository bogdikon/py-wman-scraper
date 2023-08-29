import wmanscraper
url = "CHANGE TO YOUR URL!!"
isup = wmanscraper.test_for_webman(url)
cpu = wmanscraper.get_current_temp_cpu(url)
rsx = wmanscraper.get_current_temp_rsx(url)
hdd = wmanscraper.get_free_hdd_space(url)
cooler = wmanscraper.get_cooler_percent(url)
ram = wmanscraper.get_free_ram(url)
firmware = wmanscraper.get_firmware_info(url)

print("is system up: " + str(isup))
print("cpu temp: " + str(cpu))
print("rsx temp: " + str(rsx))
print("free hdd space: " + str(hdd) + " GB")
print("free ram: " + str(ram) + " KB")
print("cooler speed: " + str(cooler) + "%")

print()
print("firmware: " + firmware)
