#!/usr/bin/env python3

# DNS TOOL TO SYNC DNS RECORDS TO BUNNYCDN
# Github repo: https://github.com/remarkablecloud/sync-dns-to-bunnycdn
# Description: Sync zones and dns recors from local DNS server to BunnyCDN DNS Service
# Version:     1.0
# Author:      RemarkableCloud
# Author URI:  https://remarkablecloud.com/
# License:      GPLv3
# License URI:  https://www.gnu.org/licenses/gpl-3.0.html
# Requires:    Python 3.6 or higher
# Requires:    dig (dnsutils)
# Requires:    AXFR zone transfer enabled on source DNS server
# Usage: 
#  Add Zone:             python3 bunny-dns.py -add-zone example.com
#  Get Zone id:          python3 bunny-dns.py -get-zone-id example.com
#  Delete Zone:          python3 bunny-dns.py -delete-zone example.com
#  Sync Zone Records:    python3 bunny-dns.py -sync-zone example.com

# Import modules
import sys
import os
import requests
import json
import argparse
import dns.resolver
import dns.query
import dns.zone
import dns.rdatatype
import subprocess

# Global variables
config_file = '/etc/bunny-dns-sync.conf'
config = {}

# Mapping from BunnyCDN types to DNS record types
dns_to_bunny = {
    'A': 0,
    'AAAA': 1,
    'CNAME': 2,
    'TXT': 3,
    'MX': 4,
    'Redirect': 5,
    'Flatten': 6,
    'PullZone': 7,
    'SRV': 8,
    'CAA': 9,
    'PTR': 10,
    'Script': 11,
    'NS': 12,
    'SOA': 99, # BunnyCDN does not support SOA records this is a dummy value
}
# Functions

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
#print(config)

# Function to add a zone
def add_zone(zone_name):
    """Add a zone to BunnyCDN DNS Service"""
    api_key = config['api_key']
    api_url = config['api_url']
    headers = {
        'accept': 'application/json',
        'content-type': 'application/json',
        'AccessKey': api_key
    }
    data = {
        'Domain': zone_name
    }
    response = requests.post(api_url + '/dnszone', headers=headers, json=data)
    if response.status_code == 201:
        print('Zone {} added'.format(zone_name))
    else:
        print('Error adding zone {}'.format(zone_name))
        print('Status code: {}'.format(response.status_code))
        print('Response: {}'.format(response.text))

# Function to get zone_id from zone_name 

def get_zone_id(zone_name):
    """Get the zone_id from BunnyCDN DNS Service for the given zone_name"""
    api_key = config['api_key']
    api_url = config['api_url']
    headers = {
        'accept': 'application/json',
        'AccessKey': api_key
    }
    params = {
        'page': 1,
        'perPage': 10,
        'search': zone_name
    }
    response = requests.get(api_url + '/dnszone', headers=headers, params=params)
    if response.status_code == 200:
        zones = response.json()
        for zone in zones['Items']:  # Change this line
            if zone['Domain'] == zone_name:
                print('Zone ID for {} is {}'.format(zone_name, zone['Id']))
                return zone['Id']
        print('Zone {} not found'.format(zone_name))
    else:
        print('Error getting zone ID for {}'.format(zone_name))
        print('Status code: {}'.format(response.status_code))
        print('Response: {}'.format(response.text))

# Function to delete a zone
def delete_zone(zone_name):
    """Delete a zone from BunnyCDN DNS Service"""
    #zone_id = get_zone_id(zone_name)
    if zone_id:
        api_key = config['api_key']
        api_url = config['api_url']
        headers = {
            'accept': 'application/json',
            'AccessKey': api_key
        }
        url = api_url + '/dnszone/' + str(zone_id)  # Change this line
        response = requests.delete(url, headers=headers)
        if response.status_code == 204:
            print('Zone {} deleted'.format(zone_id))
        else:
            print('Error deleting zone {}'.format(zone_id))
            print('Status code: {}'.format(response.status_code))
            print('Response: {}'.format(response.text))
    else:
        print('Zone {} not found'.format(zone_name))

# Function to get local DNS records


def get_local_dns_records(zone_name):
    local_nameserver = config['local_nameserver']
    command = ['dig', 'AXFR', '@' + local_nameserver, zone_name]
    process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    output = process.stdout.split('\n')
    records = []
    for line in output:
        if line and not line.startswith(';'):
            fields = line.split()
            if len(fields) >= 5:
                record_type = fields[3]
                record_data = fields[4:]
                record = {
                    'Name': fields[0],
                    'Ttl': int(fields[1]),  # Convert Ttl to integer
                    'Type': dns_to_bunny[record_type] if record_type in dns_to_bunny else record_type,
                }
                # If the Name is ending in zone_name, remove zone_name from Name
                if record['Name'].endswith(zone_name + '.'):
                    record['Name'] = record['Name'][:-len(zone_name)-1]
                # If the Name value is ending in period, remove the period
                if record['Name'].endswith('.'):
                    record['Name'] = record['Name'][:-1]
                if record_type in ['MX', 'SRV']:
                    record['Priority'] = int(record_data[0])  # Convert Priority to integer
                if record_type == 'SRV':
                    record['Weight'] = int(record_data[1])  # Convert Weight to integer
                    record['Port'] = int(record_data[2])  # Convert Port to integer
                record['Value'] = ' '.join(record_data[1:]) if record_type == 'MX' else ' '.join(record_data[3:]) if record_type == 'SRV' else ' '.join(record_data)
                # If the Value is ending in period, remove the period
                if record['Value'].endswith('.'):
                    record['Value'] = record['Value'][:-1]
                # If the record type is TXT (3), ensure the Value is enclosed in single quotes
                if record['Type'] == 3:
                    if record['Value'].startswith('"') and record['Value'].endswith('"'):
                        record['Value'] = record['Value'].strip('"')
                    elif record['Value'].startswith("'") and record['Value'].endswith("'"):
                        record['Value'] = record['Value'].strip("'")
                records.append(record)
    return records


# Function to get remote DNS records

def get_remote_dns_records(zone_name):
    """Get the DNS records for the given zone_name from BunnyCDN DNS Service"""
    #zone_id = get_zone_id(zone_name)
    if zone_id:
        api_key = config['api_key']
        api_url = config['api_url']
        headers = {
            'accept': 'application/json',
            'AccessKey': api_key
        }
        url = api_url + '/dnszone/' + str(zone_id)
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            dns_records = response.json()['Records']
            remote_records = []
            for record in dns_records:
                # Only include the fields that are present in the local records, plus the record_id
                remote_record = {
                    'Id': record['Id'],
                    'Name': record['Name'],
                    'Ttl': record.get('Ttl', 0),  # Provide a default value if 'TTL' does not exist
                    'Type': record['Type'],
                }
                # Include additional fields for MX and SRV records
                if record['Type'] == 4:  # 4 is the type for MX records
                    remote_record['Priority'] = record['Priority']
                    remote_record['Value'] = record['Value']
                elif record['Type'] == 8:  # 8 is the type for SRV records
                    remote_record.update({
                        'Priority': record['Priority'],
                        'Weight': record['Weight'],
                        'Port': record['Port'],
                        'Value': record['Value'],
                    })
                else:
                    remote_record['Value'] = record['Value']
                remote_records.append(remote_record)
            return remote_records
        else:
            print('Error retrieving DNS records for zone {}'.format(zone_id))
            print('Status code: {}'.format(response.status_code))
            print('Response: {}'.format(response.text))
    else:
        print('Zone {} not found'.format(zone_name))

# Function to compare local and remote DNS records

def compare_records(local_records, remote_records):
    records_to_delete = []
    records_to_add = []

    # Convert records to a comparable form
    local_records_comparable = [{k: v for k, v in record.items() if k != 'Id'} for record in local_records]
    remote_records_comparable = [{k: v for k, v in record.items() if k != 'Id'} for record in remote_records]

    # Find records to delete
    for record in remote_records:
        if {k: v for k, v in record.items() if k != 'Id'} not in local_records_comparable:
            records_to_add.append(record)

    # Find records to add
    for record in local_records:
        if {k: v for k, v in record.items() if k != 'Id'} not in remote_records_comparable:
            # Apply the rules
            if not ((record['Name'] == '' and record['Type'] == 12) or record['Type'] == 99):
                records_to_delete.append(record)

    return records_to_delete, records_to_add


# Function to sync DNS records
def sync_dns_records(zone_id, records_to_add, records_to_delete):
    """Sync DNS records by deleting and adding records"""
    api_key = config['api_key']
    api_url = config['api_url']
    headers = {
        'accept': 'application/json',
        'AccessKey': api_key,
        'content-type': 'application/json'
    }

    # Delete records
    for record in records_to_delete:
        url = api_url + '/dnszone/' + str(int(zone_id)) + '/records/' + str(int(record['Id']))
        response = requests.delete(url, headers=headers)
        if response.status_code == 204:
            print('Record deleted successfully: {}'.format(record))
        else:
            print('Error deleting record: {}'.format(record))
            print('Status code: {}'.format(response.status_code))
            print('Response: {}'.format(response.text))

    # Add records
    for record in records_to_add:
        url = api_url + '/dnszone/' + str(zone_id) + '/records'
        response = requests.put(url, headers=headers, json=record)
        if response.status_code == 201:
            print('Record added successfully: {}'.format(record))
        else:
            print('Error adding record: {}'.format(record))
            print('Status code: {}'.format(response.status_code))
            print('Response: {}'.format(response.text))


# MAIN CODE
    
# Parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('-add-zone', help='Add a zone to BunnyCDN DNS Service')
parser.add_argument('-get-zone-id', help='Get the zone_id for a zone_name')
parser.add_argument('-delete-zone', help='Delete a zone from BunnyCDN DNS Service')
parser.add_argument('-sync-zone', help='Sync a zone', type=str)
args = parser.parse_args()

# Check if -add-zone argument is provided
if args.add_zone:
    add_zone(args.add_zone)
    zone_id = get_zone_id(args.add_zone)
    local_records = get_local_dns_records(args.add_zone)
    remote_records = get_remote_dns_records(args.add_zone)
    records_to_add, records_to_delete = compare_records(local_records, remote_records)
    sync_dns_records(zone_id, records_to_add, records_to_delete)

# Check if -get-zone-id argument is provided
if args.get_zone_id:
    get_zone_id(args.get_zone_id)

# Check if -delete-zone argument is provided
if args.delete_zone:
    zone_id = get_zone_id(args.delete_zone)
    delete_zone(args.delete_zone)

# Check if -sync-zone argument is provided
if args.sync_zone:
     zone_name = args.sync_zone
     zone_id = get_zone_id(args.sync_zone)
     local_records = get_local_dns_records(zone_name)
     remote_records = get_remote_dns_records(zone_name)
     records_to_add, records_to_delete = compare_records(local_records, remote_records)
     sync_dns_records(zone_id, records_to_add, records_to_delete)
