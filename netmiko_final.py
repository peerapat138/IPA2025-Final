from netmiko import ConnectHandler
from pprint import pprint

username = "admin"
password = "cisco"


def gigabit_status(ip):
    ans = ""
    device_params = {
    "device_type": "cisco_ios",
    "ip": ip,
    "username": username,
    "password": password,
    }
    with ConnectHandler(**device_params) as ssh:
        up = 0
        down = 0
        admin_down = 0
        status = []
        result = ssh.send_command("sh ip int br", use_textfsm=True)
        for interfaces in result:
            if "GigabitEthernet" in interfaces["interface"]:
                status_int = interfaces.get("status", " ")
                interface_name = interfaces['interface']
                if status_int == "up":
                    up += 1
                elif status_int == "down":
                    down += 1
                elif status_int == "administratively down":
                    admin_down += 1
            status.append(f"{interface_name} {status_int}")
        interface_summary = ", ".join(status)
        summary_count = f"-> {up} up, {down} down, {admin_down} administratively down"
        ans = f"{interface_summary} {summary_count}"
        pprint(ans)
        return ans

# if __name__ == "__main__":
#     gigabit_status()