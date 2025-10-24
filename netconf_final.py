from ncclient import manager
import xmltodict

m = manager.connect(
    host="10.0.15.63",
    port=830,
    username="admin",
    password="cisco",
    hostkey_verify=False
    )

def create():
    netconf_config = """
    <config>
        <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
            <interface>
                <name>Loopback66070138</name>
                <description>Loopback 66070138 created by NETCONF</description>
                <type xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type">
                    ianaift:softwareLoopback
                </type>
                <enabled>true</enabled>
                <ipv4 xmlns="urn:ietf:params:xml:ns:yang:ietf-ip">
                    <address>
                        <ip>172.1.38.1</ip>
                        <netmask>255.255.255.0</netmask>
                    </address>
                </ipv4>
            </interface>
        </interfaces>
    </config>
    """

    try:
        netconf_reply = netconf_edit_config(netconf_config)
        xml_data = netconf_reply.xml
        print(xml_data)
        if '<ok/>' in xml_data:
            return "Interface loopback 66070138 is created successfully using Netconf"
    except Exception as e:
        print("Error:", e)
        return "Cannot create: Interface loopback 66070138"


def delete():
    netconf_config = """ 
    <config>
        <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
            <interface operation="delete">
                <name>Loopback66070138</name>
            </interface>
        </interfaces>
    </config>
    """

    try:
        netconf_reply = netconf_edit_config(netconf_config)
        xml_data = netconf_reply.xml
        print(xml_data)
        if '<ok/>' in xml_data:
            return "Interface loopback 66070138 is deleted successfully using Netconf"
    except Exception as e:
        print("Error:", e)
        return "Cannot delete: Interface loopback 66070138"


def enable():
    netconf_config = """
    <config>
        <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
            <interface>
                <name>Loopback66070138</name>
                <enabled>true</enabled>
            </interface>
        </interfaces>
    </config>
    """

    try:
        netconf_reply = netconf_edit_config(netconf_config)
        xml_data = netconf_reply.xml
        print(xml_data)
        if '<ok/>' in xml_data:
            return "Interface loopback 66070138 is enabled successfully using Netconf"
    except Exception as e:
        print("Error:", e)
        return "Cannot enable: Interface loopback 66070138"

def disable():
    netconf_config = """
    <config>
        <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
            <interface>
                <name>Loopback66070138</name>
                <enabled>false</enabled>
            </interface>
        </interfaces>
    </config>
    """

    try:
        netconf_reply = netconf_edit_config(netconf_config)
        xml_data = netconf_reply.xml
        print(xml_data)
        if '<ok/>' in xml_data:
            return "Interface loopback 66070138 is shutdowned successfully using Netconf"
    except Exception as e:
        print("Error:", e)
        return "Cannot shutdown: Interface loopback 66070138 (checked by Netconf)"

def netconf_edit_config(netconf_config):
    return  m.edit_config(target="running", config=netconf_config)


def status():
    netconf_filter = """
    <filter>
        <interfaces-state xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
            <interface>
                <name>Loopback66070138</name>
            </interface>
        </interfaces-state>
    </filter>
    """

    try:
        # Use Netconf operational operation to get interfaces-state information
        netconf_reply = m.get(filter=netconf_filter)
        netconf_reply_dict = xmltodict.parse(netconf_reply.xml)
        interface_data = netconf_reply_dict.get('rpc-reply', {}).get('data', {}).get('interfaces-state', {}).get('interface')
        # if there data return from netconf_reply_dict is not null, the operation-state of interface loopback is returned
        if interface_data:
            # extract admin_status and oper_status from netconf_reply_dict
            admin_status = interface_data.get('admin-status')
            oper_status = interface_data.get('oper-status')
            if admin_status == 'up' and oper_status == 'up':
                return "Interface loopback 66070138 is enable (checked by Netconf)"
            elif admin_status == 'down' and oper_status == 'down':
                return "Interface loopback 66070138 is disabled (checked by Netconf)"
        else: # no operation-state data
            return "No Interface loopback 66070138 (checked by Netconf)"
    except Exception as e:
        print("Error:", e)


# if __name__ == "__main__":
#     print("------------Create-----------------------")
#     print(create())
#     print("------------Status-----------------------")
#     print(status())
#     print("------------Diasble-----------------------")
#     print(disable())
#     print("------------Status-----------------------")
#     print(status())
#     print("------------Enable-----------------------")
#     print(enable())
#     print("------------Status-----------------------")
#     print(status())
#     print("------------Delete-----------------------")
#     print(delete())