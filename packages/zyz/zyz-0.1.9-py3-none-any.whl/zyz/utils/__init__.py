
def get_public_ip():
    import urllib.request
    ip = urllib.request.urlopen("https://ifconfig.me/ip").read().decode()
    return ip
