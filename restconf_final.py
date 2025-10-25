import json
import requests
requests.packages.urllib3.disable_warnings()



# the RESTCONF HTTP headers, including the Accept and Content-Type
# Two YANG data formats (JSON and XML) work with RESTCONF 
headers = {
    "Accept": "application/yang-data+json",
    "Content-Type": "application/yang-data+json"
}
basicauth = ("admin", "cisco")


def create(ip):
    # Router IP Address is 10.0.15.181-184
    api_url = f"https://{ip}/restconf/data/ietf-interfaces:interfaces"

    yangConfig = {
    "ietf-interfaces:interface": {
        "name": "Loopback66070138",
        "description": "loopback 66070138 create by RESTCONF",
        "type": "iana-if-type:softwareLoopback",
        "enabled": True,
        "ietf-ip:ipv4": {
            "address": [
                {
                    "ip": "172.1.38.1",
                    "netmask": "255.255.255.0"
                }
            ]
        },
        "ietf-ip:ipv6": {}
    }
}
    resp = requests.post(
        api_url, 
        data=json.dumps(yangConfig), 
        auth=basicauth,
        headers=headers,
        verify=False
        )

    if(resp.status_code >= 200 and resp.status_code <= 299):
        print("STATUS OK: {}".format(resp.status_code))
        return "Interface loopback 66070138 is created successfully using Restconf"
    else:
        print('Error. Status Code: {}'.format(resp.status_code))
        return "Cannot create: Interface loopback 66070138"


def delete(ip):
    # Router IP Address is 10.0.15.181-184
    api_url = f"https://{ip}/restconf/data/ietf-interfaces:interfaces/interface=Loopback66070138"

    resp = requests.delete(
        api_url, 
        auth=basicauth, 
        headers=headers, 
        verify=False
        )

    if(resp.status_code >= 200 and resp.status_code <= 299):
        print("STATUS OK: {}".format(resp.status_code))
        return "Interface loopback 66070138 is deleted successfully using Restconf"
    else:
        print('Error. Status Code: {}'.format(resp.status_code))
        return "Cannot delete: Interface loopback 66070138"


def enable(ip):
    # Router IP Address is 10.0.15.181-184
    api_url = f"https://{ip}/restconf/data/ietf-interfaces:interfaces/interface=Loopback66070138"
    yangConfig = {
    "ietf-interfaces:interface": {
        "name": "Loopback66070138",
        "type": "iana-if-type:softwareLoopback",
        "enabled": True,
    }
}

    resp = requests.patch(
        api_url, 
        data=json.dumps(yangConfig), 
        auth=basicauth, 
        headers=headers, 
        verify=False
        )

    if(resp.status_code >= 200 and resp.status_code <= 299):
        print("STATUS OK: {}".format(resp.status_code))
        return "Interface loopback 66070138 is enabled successfully using Restconf"
    else:
        print('Error. Status Code: {}'.format(resp.status_code))
        return "Cannot enable: Interface loopback 66070138"


def disable(ip):
    # Router IP Address is 10.0.15.181-184
    api_url = f"https://{ip}/restconf/data/ietf-interfaces:interfaces/interface=Loopback66070138"

    yangConfig = {
    "ietf-interfaces:interface": {
        "name": "Loopback66070138",
        "type": "iana-if-type:softwareLoopback",
        "enabled": False,
    }
}

    resp = requests.patch(
        api_url, 
        data=json.dumps(yangConfig), 
        auth=basicauth, 
        headers=headers, 
        verify=False
        )

    if(resp.status_code >= 200 and resp.status_code <= 299):
        print("STATUS OK: {}".format(resp.status_code))
        return "Interface loopback 66070138 is shutdowned successfully using Restconf"
    else:
        print('Error. Status Code: {}'.format(resp.status_code))
        return "Cannot shutdown: Interface loopback 66070138 (checked by Restconf)"


def status(ip):
    api_url_status = f"https://{ip}/restconf/data/ietf-interfaces:interfaces-state/interface=Loopback66070138"

    resp = requests.get(
        api_url_status, 
        auth=basicauth, 
        headers=headers, 
        verify=False
        )

    if(resp.status_code >= 200 and resp.status_code <= 299):
        print("STATUS OK: {}".format(resp.status_code))
        response_json = resp.json()
        admin_status = response_json['ietf-interfaces:interface']['admin-status']
        oper_status = response_json['ietf-interfaces:interface']['oper-status']
        if admin_status == 'up' and oper_status == 'up':
            return "Interface loopback 66070138 is enabled (checked by Restconf)"
        elif admin_status == 'down' and oper_status == 'down':
            return "Interface loopback 66070138 is disable (checked by Restconf)"
    elif(resp.status_code == 404):
        print("STATUS NOT FOUND: {}".format(resp.status_code))
        return "No Interface loopback 66070138 (checked by Restconf)"
    else:
        print('Error. Status Code: {}'.format(resp.status_code))

# if __name__ == "__main__":
#      enable()
