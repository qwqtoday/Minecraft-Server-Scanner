import ipaddress
from concurrent.futures import ThreadPoolExecutor
import mcstatus
import json
import time
def save_server(information: str, ip):
    file = open(r'servers.json')
    data = json.load(file)
    data[ip] = information
    json.dump(data, open('servers.json', 'w'))

def check_mc(ip):
    try:
        server_status = mcstatus.JavaServer.lookup(ip).status()
        print(f"The ip {ip} has a Minecraft server with {server_status.latency}ms ping")
        save_server(server_status.raw, ip)
    except Exception as e:
        print(ip, e)


def main():
    cidr = input('Enter the cidr that you want to scan!  ')
    ips = [str(ip) for ip in ipaddress.IPv4Network(cidr)]
    with ThreadPoolExecutor(max_workers=400) as executor:
        for ip in ips:
            executor.submit(check_mc, ip)

if __name__ == '__main__':
    main()
