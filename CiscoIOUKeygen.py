#! /usr/bin/python3
# Cisco IOU License Generator - Python 3 version

import os
import socket
import hashlib
import struct

# Get the host ID and hostname to calculate the host key
hostid = os.popen("hostid").read().strip()
hostname = socket.gethostname()
ioukey = int(hostid, 16)

for x in hostname:
    ioukey = ioukey + ord(x)

print("hostid=" + hostid + ", hostname=" + hostname + ", ioukey=" + hex(ioukey)[2:])

# Create the license using md5sum
iouPad1 = b'\x4B\x58\x21\x81\x56\x7B\x0D\xF3\x21\x43\x9B\x7E\xAC\x1D\xE6\x8A'
iouPad2 = b'\x80' + b'\0' * 39
md5input = iouPad1 + iouPad2 + struct.pack('!i', ioukey) + iouPad1
iouLicense = hashlib.md5(md5input).hexdigest()[:16]

print("\nAdd the following text to /opt/unetlab/addons/iol/bin")
print(f"[license]\n{hostname} = {iouLicense};\n")
print("You can disable the phone home feature with something like:")
print("echo '127.0.0.127 xml.cisco.com' >> /etc/hosts")
