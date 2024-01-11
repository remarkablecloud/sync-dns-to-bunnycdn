# BunnyCDN DNS Sync Tool

## Description
This script is a DNS tool that synchronizes zones and DNS records from a local DNS server to BunnyCDN DNS Service. It lets you easily manage and update your DNS records on BunnyCDN by leveraging AXFR zone transfer from your source DNS server.

## Version
1.0

## Author
[RemarkableCloud](https://remarkablecloud.com/)

## License
This project is licensed under the [GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.html).

## Requirements
- Python 3.6 or higher
- `dig` (dnsutils)
- AXFR zone transfer enabled on the source DNS server

## To-Do
- [X] Whitelist Domain (zones that must be ignored in add/sync/delete)
- [X] Support for BunnyCDN Custom Nameservers and contact email (BunnyCDN doesn't support SOA records)

# How to Install

## Clone the repository
```bash
git clone https://github.com/remarkablecloud/sync-dns-to-bunnycdn.git
```

## Navigate to the repository directory
```bash
cd sync-dns-to-bunnycdn
```
## Copy the configuration file to /etc (using sudo for permissions)
```bash
sudo cp config/bunny-dns-sync.conf /etc/bunny-dns-sync.conf
sudo cp config/bunny-dns-sync-exclude.txt /etc/bunny-dns-sync-exclude.txt
```

## Copy scripts to /usr/local/bin

```bash
sudo cp scripts/bunny-dns.py /usr/local/bin/bunny-dns.py
sudo cp scripts/zone-change-detector.py /usr/local/bin/zone-change-detector.py
```

## Set executable permissions

```bash
sudo chmod +x /usr/local/bin/bunny-dns.py
sudo chmod +x /usr/local/bin/zone-change-detector.py
```
## Edit the configuration file to add your BunnyCDN Key and the source of your dns zones
 ```bash
sudo nano etc/bunny-dns-sync.conf
```
## Optional: Add domains to the exclude list
 ```bash
sudo nano /etc/bunny-dns-sync
```
## Create a log file
 ```bash
sudo touch /var/log/bunny-dns.log
```
## Create a cron job like
 ```bash
* * * * * /usr/local/bin/zone-change-detector.py >> /var/log/bunny-dns.log
```

/usr/local/bin/zone-change-detector.py will monitor all your zones .db located in $zone_dir, if any zones are added, changed, or deleted, it will call /usr/local/bin/zone-change-detector.py to sync the changes


# Manual Usage:

#### Add Zone
python3 bunny-dns.py -add-zone example.com

#### Get Zone ID
 bunny-dns.py -get-zone-id example.com

#### Delete Zone
bunny-dns.py -delete-zone example.com

#### Sync Zone Records
bunny-dns.py -sync-zone example.com

## How to Contribute

Feel free to contribute to this project by opening issues or submitting pull requests.
### Support
If you encounter any issues or have questions, please open an issue.

Happy syncing!
