from random import randrange
import requests
from threading import Thread
from time import sleep
from tqdm import tqdm

ipbad = False
goodips = []

def checkIp1(ipstr, region="Europe"):
    global ipbad
    global goodips
    # 0 in region
    # 1 outside
    # 2 prob ip throttled
    if ipbad:
        return 2

    r = requests.get("https://ipinfo.io/" + ipstr.split(":")[0])
    if r.status_code != 200:
        ipbad = True
        return 2
    if r.json()["timezone"].split("/")[0] == region:
        goodips.append(ipstr)
        return 0
    return 1

def checkIp2(ipstr, maxtime=2):
    # import os
    # if os.getuid() != 0:
    #     print("[-] Requires root")
    #     os._exit(1)

    from ping3 import ping
    if ping(ipstr.split(":")[0], timeout=maxtime):
        goodips.append(ipstr)
        return True
    return False


def getIps():
    url = "https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks4&timeout=200&country=all"
    return requests.get(url).text.split("\r\n")


def main():
    filename = "GoodIps.txt"
    print("[*] Downloading proxies...")
    Ips = getIps()
    jobs = []
    t = False

    print(f"[*] Checking {len(Ips)} ips")

    if t:
        for ip in tqdm(Ips, desc="Starting Thread"):
            t = Thread(target=checkIp1, args=(ip,))
            t.start()
            jobs.append(t)
        sleep(1)

        o = True
        for job in tqdm(jobs, desc="Finishing"):
            if ipbad:
                if o:
                    print("[-] IP Throttled, killing remaining threads...")
                    o = False
            else:
                job.join()
    else:
        for ip in tqdm(Ips, desc="Checking ip"):
            checkIp2(ip, 0.05)
    
    print("[+] Done!")
    print(f"[*] Writing {len(goodips)} ips to file: {filename}")
    with open(filename, "w") as f:
        f.write("\n".join(goodips))
    import random
    print(f"[+] Random ip: {random.choice(goodips)}")

main()