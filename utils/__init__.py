import os
# set proxy
def set_proxy():
    os.environ['HTTP_PROXY'] = "http://10.30.69.253:7890"
    os.environ['HTTPS_PROXY'] = "http://10.30.69.253:7890"
    print("Proxy set.")