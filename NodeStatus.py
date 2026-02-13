import getpass
import requests
import truststore
import gc

truststore.inject_into_ssl()  #adds local certificates for authentication and trust

def check_pan(pan, auth):
    url = f"https://{pan}/api/v1/deployment/node"
    headers = {"Accept": "application/json", "Content-Type": "application/json"}

    try:
        response = requests.get(url, auth=auth, headers=headers, timeout=5)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")
    except requests.exceptions.RequestException as e:
        print(f"An error has occured: {e}")
    data = response.json()
    nodes = data.get("response", [])
    nodeStatus = [
        {
            "hostname": node.get("hostname"), # add hostnames here, if more than one separate with comma
            "nodeStatus": node.get("nodeStatus"),
        }
        for node in nodes
    ]
    print(f"Checking {pan}...")
    print(f"Return Code: {response.status_code}")
    t=0
    for node in nodeStatus:
        if node.get("nodeStatus") != "Connected":
            print(node)
            t=t+1
    if t == 0:
        print("All nodes online")

if __name__ == "__main__":
    fqdn = ["enter.fqdn.here"]  # Separate fqdn's by comma if more than one i.e ["my.fqdn.one", "my.fqdn.two"]
    username = getpass.getpass('Username: ')  # Grab username to log into your Cisco ISE Admin node
    password = getpass.getpass()
    auth = (username, password)
    for f in fqdn:
        check_pan(f, auth)
    
    del username   # Clear username from memory
    del password   # Clear password from memory
    gc.collect()   # Garbage cleanup to ensure no information lingering in memory