#!/bin/bash
apt purge zabbix-agent -y
ubuntu() 
{
which apt >/dev/null 2>&1
if [ $? -eq 0 ]
then
installation_with_config
else
yumpkg
fi
}
configuration()
 {
sed -i 's/^Server=.*/Server=172.31.11.146/g' /etc/zabbix/zabbix_agentd.conf
sed -i 's/^ServerActive=.*/ServerActive=172.31.11.146/g' /etc/zabbix/zabbix_agentd.conf
sed -i '/^Hostname=.*/s/^/#/' /etc/zabbix/zabbix_agentd.conf
sed -i 's/.*ListenPort=.*/ListenPort=10050/g' /etc/zabbix/zabbix_agentd.conf
sed -i '/.*HostMetadata=.*/s/^/#/' /etc/zabbix/zabbix_agentd.conf
sed -i '167i HostMetadata=linux' /etc/zabbix/zabbix_agentd.conf
}
installation_with_config() 
{
zabbix_agentd --version >/dev/null 2>&1
if [ $? -eq 0 ];
then
$(configuration)
else
apt update -y
apt install zabbix-agent -y
$(configuration)
fi
}
yumpkg()
{
echo "Agent Imstall"
}
ubuntu
systemctl restart zabbix-agent;sleep 10;systemctl restart zabbix-agent
systemctl status zabbix-agent
