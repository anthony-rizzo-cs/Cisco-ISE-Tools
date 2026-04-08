"""
Cisco ISE Node Status Checker
Retrieves and validates the deployment status of Cisco ISE nodes via REST API.
"""
import getpass
import logging
import requests
import truststore
from typing import Tuple

# Inject local system certificate store for enterprise SSL inspection compatibility
truststore.inject_into_ssl()

# Configure logging for enterprise-grade execution
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

def check_ise_nodes(fqdn: str, auth: Tuple[str, str]) -> None:
    """
    Queries the Cisco ISE API for node deployment status.
    
    Args:
        fqdn (str): The Fully Qualified Domain Name of the ISE PAN.
        auth (Tuple[str, str]): A tuple containing (username, password).
    """
    url = f"https://{fqdn}/api/v1/deployment/node"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    logging.info(f"Querying Primary Admin Node (PAN): {fqdn}...")

    # 1. Secure API Request
    try:
        response = requests.get(url, auth=auth, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.exceptions.Timeout:
        logging.error(f"Connection to {fqdn} timed out.")
        return  # Exit function early to prevent crash
    except requests.exceptions.HTTPError as e:
        logging.error(f"HTTP Error querying {fqdn}: {e}")
        return
    except requests.exceptions.RequestException as e:
        logging.error(f"Network error querying {fqdn}: {e}")
        return

    # 2. Parse Data Securely
    try:
        data = response.json()
        nodes = data.get("response", [])
    except ValueError:
        logging.error(f"Failed to parse JSON response from {fqdn}.")
        return

    offline_nodes = []
    
    # 3. Evaluate Node Status
    for node in nodes:
        hostname = node.get("hostname", "Unknown")
        status = node.get("nodeStatus", "Unknown")
        
        if status.lower() != "connected":
            offline_nodes.append({"hostname": hostname, "status": status})

    # 4. Report Findings
    if not offline_nodes:
        logging.info(f"SUCCESS: All nodes managed by {fqdn} are Connected.")
    else:
        logging.warning(f"ALERT: Found {len(offline_nodes)} node(s) with abnormal status on {fqdn}:")
        for node in offline_nodes:
            logging.warning(f"  - {node['hostname']}: {node['status']}")

def main():
    print("--- Cisco ISE Deployment Status Monitor ---\n")
    
    # Configuration
    ise_pans = ["enter.fqdn.here"]  # e.g., ["ise-pan-01.local", "ise-pan-02.local"]
    
    # Secure Credential Intake
    username = input("ISE Admin Username: ")
    password = getpass.getpass("ISE Admin Password: ")
    auth_credentials = (username, password)

    print("\nStarting execution...")
    for pan in ise_pans:
        check_ise_nodes(pan, auth_credentials)
        
    # Note on Python Memory: Unlike C, Python's GC does not guarantee memory zeroing for strings.
    # The primary security control here is using getpass to prevent terminal echoing.

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logging.info("Execution cancelled by user.")