#!/usr/bin/env python3
import os
import hashlib
import configparser

# Set the zone directory
config_file = '/etc/bunny-dns-sync.conf'
config = configparser.ConfigParser()
config.read(config_file)

zone_dir = config.get('DEFAULT', 'zone_dir')
dns_zone_hashes_file = "/tmp/dns_zone_hashes.txt"

# Commands for add, update, and remove
command_for_updated_zone = "/usr/local/bin/bunn-dns.py %s"
command_for_added_zone = "/usr/local/bin/bunn-dns.py %s"
command_for_removed_zone = "/usr/local/bin/bunn-dns.py %s"

# read dns_zone_hashes_file and get the zone name and hash
# the format is zone_name:zone_hash
# if the dns_zone_hashes_file does not exist, create it
if not os.path.isfile(dns_zone_hashes_file):
    open(dns_zone_hashes_file, 'a').close()

# Read existing hashes into a dictionary
existing_hashes = {}
with open(dns_zone_hashes_file, 'r') as f:
    for line in f:
        zone_name, zone_hash = line.strip().split(':')
        existing_hashes[zone_name] = zone_hash

# generated hashes of all zone files located in zone_dir/*.db remove the ending .db
# and compare the hashes with the ones in dns_zone_hashes_file
for zone_file in os.listdir(zone_dir):
    if zone_file.endswith('.db'):
        zone_name = os.path.splitext(zone_file)[0]
        with open(os.path.join(zone_dir, zone_file), 'rb') as f:
            zone_hash = hashlib.md5(f.read()).hexdigest()

        if zone_name in existing_hashes:
            if existing_hashes[zone_name] != zone_hash:
                os.system(command_for_updated_zone % zone_name)
                existing_hashes[zone_name] = zone_hash
        else:
            os.system(command_for_added_zone % zone_name)
            existing_hashes[zone_name] = zone_hash

# Write updated hashes back to the file
with open(dns_zone_hashes_file, 'w') as f:
    for zone_name, zone_hash in existing_hashes.items():
        if os.path.isfile(os.path.join(zone_dir, f"{zone_name}.db")):
            f.write(f"{zone_name}:{zone_hash}\n")
        else:
            os.system(command_for_removed_zone % zone_name)