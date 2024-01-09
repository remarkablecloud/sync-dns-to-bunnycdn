# BunnyCDN DNS Sync Tool

## Description
This script is a DNS tool designed to synchronize zones and DNS records from a local DNS server to BunnyCDN DNS Service. It allows you to easily manage and update your DNS records on BunnyCDN by leveraging AXFR zone transfer from your source DNS server.

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

## Configuration
To customize the tool for your environment, create a configuration file named `bunny-dns-sync.conf` in the `/etc/` directory. You can use the provided [sample configuration file](/etc/bunny-dns-sync.conf) as a template.

```ini
# /etc/bunny-dns-sync.conf

 # Config
api_key = YOUR_BUNNYCDN_API_KEY
api_url = https://api.bunny.net

Make sure to replace YOUR_BUNNYCDN_API_KEY with your actual BunnyCDN API key.

Usage:
# Add Zone
python3 bunny-dns.py -add-zone example.com

# Get Zone ID
python3 bunny-dns.py -get-zone-id example.com

# Delete Zone
python3 bunny-dns.py -delete-zone example.com

# Sync Zone Records
python3 bunny-dns.py -sync-zone example.com


Certainly! Here's the entire README content within a single markdown code block:

markdown
Copy code
# BunnyCDN DNS Sync Tool

## Description
This script is a DNS tool designed to synchronize zones and DNS records from a local DNS server to BunnyCDN DNS Service. It allows you to easily manage and update your DNS records on BunnyCDN by leveraging AXFR zone transfer from your source DNS server.

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

## Configuration
To customize the tool for your environment, create a configuration file named `bunny-dns-sync.conf` in the `/etc/` directory. You can use the provided [sample configuration file](/etc/bunny-dns-sync.conf) as a template.

```ini
# /etc/bunny-dns-sync.conf

[BunnyCDN]
api_key = YOUR_BUNNYCDN_API_KEY
base_url = https://api.bunny.net/dns
Make sure to replace YOUR_BUNNYCDN_API_KEY with your actual BunnyCDN API key.

Usage
bash
Copy code
# Add Zone
python3 bunny-dns.py -add-zone example.com

# Get Zone ID
python3 bunny-dns.py -get-zone-id example.com

# Delete Zone
python3 bunny-dns.py -delete-zone example.com

# Sync Zone Records
python3 bunny-dns.py -sync-zone example.com
GitHub Repository
GitHub - Sync DNS to BunnyCDN

How to Contribute
Feel free to contribute to this project by opening issues or submitting pull requests.

Support
If you encounter any issues or have questions, please open an issue.

Happy syncing!
