
# coding: utf-8

# In[77]:

#批量重启TTLlink网络打印服务器

def rebootTTlink(ip):
    # return：0-重启成功，1-连接失败，2-登录失败，3-重启失败
    
    import requests
    
    host = "http://"+ip
    basePath = "/cgi-bin/ttlink"
    data = {"username":"root","password":"admin8"}
    header ={
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Content-Length": '29',
        "Content-Type": "charset=utf-8,application/x-www-form-urlencoded",
        "Upgrade-Insecure-Requests":'1',
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36}"
    }
    session = requests.session()
    url = host + basePath
    try:
        html = session.post(url,data=data)
        html.encoding="utf-8"
        html.raise_for_status()
        if html.status_code == 200:
            print("登录"+ip+"成功")
        else:
            print("登录"+ip+"失败")
            return 2
    except Exception:
        print(ip+"远程连接失败")
        return 1

    #重启
    #Set-Cookie:sysauth=198836f5f27eff66a907265d72bddff5; path=/cgi-bin/ttlink/;stok=f1a2565891b3986c3468a4467f4c8081
    
    cook = html.headers["Set-Cookie"].split("=")
    path = cook[-2] +"="+cook[-1]
    url=host+path+"/admin/reboot?reboot=1" #重启指令
    try:
        html2=session.post(url)
        if(not html2):
            return 
        html2.raise_for_status()

        if html2.status_code == 200:
            print("重启"+ip+"上的服务成功")
        else:
            print("重启"+ip+"上的服务失败")
        
    except:
        print("重启"+ip+"上的服务失败")
        return 3
    
    return 0


def pingip(ip):
    import os
    import platform

    ip.replace(" ","")

    if platform.system() == "Linux":
        cmd = "ping -c 1 %s >> /dev/null" %ip
    else:
        cmd = "ping -n 1 %s >> null" %ip

    result = os.system(cmd)
    return result
        
if __name__ == "__main__":
    
    iplist = ["192.168.1.210",
            "192.168.1.221",
            "192.168.1.222",
            "192.168.1.223",
            "192.168.1.224",
            "192.168.1.225",
            "192.168.1.226",
            "192.168.1.227",
            "192.168.50.33",
            "192.168.4.168",
            "192.168.50.22",
            "192.168.4.198",    
            "192.168.50.23",
            "192.168.4.208", 
            "192.168.50.24",
            "192.168.4.178",   
            "192.168.50.25",
            "192.168.4.188",
            "192.168.50.26",
            "192.168.50.27",
            "192.168.50.28",
            "192.168.50.29",
            "192.168.50.30",
            "192.168.50.31",
            "192.168.1.220",
            "192.168.1.230",
            "192.168.1.229",
            "192.168.1.209",
            "192.168.2.234",
            "192.168.50.32",
            "192.168.50.16",
            "192.168.50.14",
            "192.168.50.15",
            "192.168.1.228",
            "192.168.50.17",
            "192.168.50.11",
            "192.168.50.12",
            "192.168.50.13"]
    iplist.sort()
    # iplist2 = ["192.168.1.222","192.168.1.229","192.168.1.230","192.168.50.12"] #测试
    s0 = e1 = e2 = e3 = 0
    for ip in iplist:
        ip = ip.strip()

        re = pingip(ip)
        if re != 0:
            e1 += 1
            print("ping %s 失败" %ip)
            continue

        status = rebootTTlink(ip)      
        if status == 0:
            s0 += 1
        elif status == 1:
            e1 += 1
        elif status == 2:
            e2 += 1
        elif status ==3:
            e3 += 1
            
    print("成功-%s，连接失败-%s,登录失败-%s，重启失败-%s" %(s0,e1,e2,e3)) 

 

