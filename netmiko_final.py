from netmiko import ConnectHandler
from pprint import pprint


device_ip = "10.0.15.63"
username = "admin"
password = "cisco"

device_params = {
    "device_type": "cisco_ios",
    "ip": device_ip,
    "username": username,
    "password": password,
}


def gigabit_status():
    ans = ""
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