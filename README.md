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
base_url = https://api.bunny.net/dns

