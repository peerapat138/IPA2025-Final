from netmiko import ConnectHandler
import re

def get_motd(ip):
    device = {
        "device_type": "cisco_ios",
        "host": ip,
        "username": "admin",
        "password": "cisco"
    }
    try:
        net_connect = ConnectHandler(**device)
        output = net_connect.send_command("show running-config")
        net_connect.disconnect()

        # print("=== DEBUG: raw output ===")
        # print(output)
        # print("=========================")

        if "banner motd" in output:
            match = re.search(r"\^C\s*([\s\S]*?)\s*\^C", output)
            if match:
                message = match.group(1)
                return message if message else "Error: Empty MOTD"
            else:
                return "Error: Cannot parse MOTD"
        else:
            return "Error: No MOTD Configured"

    except Exception as e:
        print(f"Error: {str(e)}")
        return "Error: No MOTD Configured"
