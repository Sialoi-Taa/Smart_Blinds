import os


file_path = 'network_info.txt'

if os.path.exists(file_path):
    os.remove(file_path)

ssid = 'Smart_Blinds'
password = 'prototype123'
with open(file_path, 'w') as file:
    file.write(f'{ssid}\n')
    file.write(f'{password}')

with open(file_path, 'r') as file:
    ssid_read = file.readline()
    ssid_read = ssid_read.rstrip('\n')
    password_read = file.readline()

print("SSID read as:", ssid_read)
print("Password read as:", password_read)