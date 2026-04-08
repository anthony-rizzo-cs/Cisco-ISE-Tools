# Cisco ISE Node Monitor

A lightweight, enterprise-ready Python utility designed to query Cisco Identity Services Engine (ISE) Primary Admin Nodes (PANs) and validate the deployment status of all connected nodes. 

This tool is built for Network Security Engineers requiring quick, automated health checks of distributed NAC environments without relying on the GUI.

## Features
* **REST API Integration:** Utilizes the Cisco ISE `/api/v1/deployment/node` endpoint for real-time telemetry.
* **Native OS Truststore Integration:** Employs the `truststore` library to natively inject the host operating system's certificate store into the SSL context. This allows the script to run seamlessly in enterprise environments utilizing custom internal PKI or SSL inspection without resorting to insecure `verify=False` practices.
* **Secure Credential Handling:** Uses `getpass` to ensure admin credentials are never hardcoded or echoed to the terminal during execution.
* **Robust Error Handling:** Safely catches timeouts, HTTP errors, and JSON parsing failures to prevent application crashes during network degradation.
* **Operational Logging:** Replaces standard standard output with the Python `logging` module, allowing for easy integration into SIEM forwarders (like Splunk) or file-based audit trails.

## Installation & Usage

1. Clone the repository:
   ```bash
   git clone [https://github.com/yourusername/ise-node-monitor.git](https://github.com/yourusername/ise-node-monitor.git)

3. Install the required dependencies (requirements.txt)
   pip install -r requirements.txt
   
4. Update the ise_pans list in the main() function with your fully qualified domain names:
     ise_pans = ["ise-pan-primary.domain.local", "ise-pan-secondary.domain.local"]

5.Run the script and follow the prompts
