#!/usr/bin/env python3
import os
import hashlib

# Set the lock file
lock_file = '/tmp/zone-change-detector.lock'

# Check if lock file exists
if os.path.isfile(lock_file):
    print("Another instance of the script is running. Exiting.")
    exit()

# Create lock file
open(lock_file, 'a').close()
# Global variables
config_file = '/etc/bunny-dns-sync.conf'
config = {}

# Function to read config file
def read_config(config_file):
    """Read config file and return a dictionary with the config parameters"""
    config = {}
    with open(config_file) as f:
        for line in f:
            if line.startswith('Config'):
                continue
            if line.startswith('#'):
                continue
            if line.strip() == '':
                continue
            (key, val) = line.split('=')
            config[key.strip()] = val.strip().strip("'")
    return config

config = read_config(config_file)
zone_dir = config['zone_dir']
dns_zone_hashes_file = "/tmp/dns_zone_hashes.txt"

# Commands for add, update, and remove
command_for_updated_zone = "/usr/local/bin/bunny-dns.py -sync-zone %s"
command_for_added_zone = "/usr/local/bin/bunny-dns.py -add-zone %s"
command_for_removed_zone = "/usr/local/bin/bunny-dns.py -delete-zone %s"

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
# Remove lock file
os.remove(lock_file)            