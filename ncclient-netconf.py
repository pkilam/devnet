from ncclient import manager
import xml.dom.minidom

#Create Netconf connection to the device using the login information
m = manager.connect(
    host="172.16.1.6",
    port=830,
    username="cisco",
    password="cisco",
    hostkey_verify=False
)

#Retrieve the capabilities from the device
print("#Supported Capabilities (Yang models):")
for capability in m.server_capabilities:
    print(capability)

#Retrieve the current running configuration from the device
print("#Current Running Configuration")
netconf_reply = m.get_config(source="running")
print(netconf_reply)

#Print the running configuraiton by prettyfing the XML
print("#Prettified Current Running Configuration")
print(xml.dom.minidom.parseString(netconf_reply.xml).toprettyxml())

#Create a filter to get a particular part of the running configuration

netconf_filter = """
<filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
    <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native" >
        <hostname />
    </native>
</filter>
"""
netconf_reply = m.get_config(source="running", filter=netconf_filter)
print(netconf_reply)
print(xml.dom.minidom.parseString(netconf_reply.xml).toprettyxml())


#Modify the hostname of the device to CSR1000v-1
netconf_hostname = """
<config  xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
    <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native" >
        <hostname>CSR100v-1</hostname>
    </native>
</config>
"""
#send the configuration changes to the device and pirnt the status
netconf_reply = m.edit_config(target="running", config=netconf_hostname)
print(xml.dom.minidom.parseString(netconf_reply.xml).toprettyxml())


#Modify the loopback 1 interface of the device
netconf_loopback = """
<config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
    <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native" >   
        <interface>
                <Loopback>
                    <name>1</name>
                    <description>Paul\'s Loopback</description>
                    <ip>
                        <address>
                            <primary>
                                <address>10.1.1.1</address>
                                <mask>255.255.255.0</mask>
                            </primary>
                        </address>
                    </ip>
                </Loopback>
        </interface>
    </native>
</config>
"""

#send the configuration changes to the device and pirnt the status
netconf_reply = m.edit_config(target="running", config=netconf_loopback)
print(xml.dom.minidom.parseString(netconf_reply.xml).toprettyxml())

