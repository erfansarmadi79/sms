#!/bin/bash

set -e






####   ./ipt.sh eth0 "192.168.1.221 192.168.1.210 192.168.1.213" "255.0.0.0 255.255.0.0 255.255.255.0" 10.42.0.240 "8.8.8.8 4.2.2.3"













# Input validation function for IP addresses
function valid_ip() {
  local  ip=$1
  local  stat=1

  if [[ $ip =~ ^([0-9]{1,3}\.){3}[0-9]{1,3}$ ]]; then
    OIFS=$IFS
    IFS='.'
    ip=($ip)
    IFS=$OIFS
    [[ ${ip[0]} -le 255 && ${ip[1]} -le 255 && ${ip[2]} -le 255 && ${ip[3]} -le 255 ]]
    stat=$?
  fi
  
  return $stat
}



function valid_netmask() {

  input=$1
  
  local  stat=1

# Check if the input is a valid netmask or CIDR notation 
  
  
if [[ "$input" =~ ^\/([0-9]|[1-2][0-9]|3[0-2])$ ]]; then
  # Input is a CIDR notation
  cidr="${input:1}"
  if [[ ! "$cidr" =~ ^[0-9]+$ ]]; then
    echo "Invalid CIDR notation: $input"
    stat=$?
    exit 1
  fi
  if (( cidr < 0 || cidr > 32 )); then
    echo "CIDR notation out of range: $input"
    stat=$?
    exit 1
  fi
  
elif [[ "$input" =~ ^([0-9]|[1-2][0-9]|3[0-2])$ ]]; then
  # Input is a CIDR notation
  cidr="${input}"
  if [[ ! "$cidr" =~ ^[0-9]+$ ]]; then
    echo "Invalid CIDR notation: $input"
    stat=$?
    exit 1
  fi
  if (( cidr < 0 || cidr > 32 )); then
    echo "CIDR notation out of range: $input"
    stat=$?
    
    exit 1
  fi

else
  # Input is a netmask
  # Split the netmask into four octets
  IFS='.' read -r -a octets <<< "$input"
  
  # Check that there are exactly four octets
  if [[ ${#octets[@]} -ne 4 ]]; then
    stat=$?
    
    echo "Invalid netmask: $input"
    exit 1
  fi
  
  # Check that each octet is a valid number between 0 and 255
  for octet in "${octets[@]}"; do
    if ! [[ $octet =~ ^[0-9]+$ ]] || (( octet > 255 )); then
      echo "Invalid netmask: $input"
      stat=$?
     
      exit 1
    fi
  done
  
  # Check that the netmask is contiguous
  binary=$(echo "obase=2; ${octets[0]}" | bc)
  binary+="$(echo "obase=2; ${octets[1]}" | bc)"
  binary+="$(echo "obase=2; ${octets[2]}" | bc)"
  binary+="$(echo "obase=2; ${octets[3]}" | bc)"
  if [[ $(echo "$binary" | grep -o '01' | wc -l) -gt 1 ]]; then
    echo "Invalid netmask: $input"
    stat=$?
    
    exit 1
  fi
  
  
fi

}






# Input converter function for Netmask
function converter_netmask() {

  input=$1

# Check if the input is a valid netmask or CIDR notation
if [[ "$input" =~ ^\/([0-9]|[1-2][0-9]|3[0-2])$ ]]; then
  # Input is a CIDR notation
  cidr="${input:1}"
  if [[ ! "$cidr" =~ ^[0-9]+$ ]]; then
    echo "Invalid CIDR notation: $input"
    exit 1
  fi
  if (( cidr < 0 || cidr > 32 )); then
    echo "CIDR notation out of range: $input"
    exit 1
  fi
elif [[ "$input" =~ ^([0-9]|[1-2][0-9]|3[0-2])$ ]]; then
  # Input is a CIDR notation
  cidr="${input}"
  if [[ ! "$cidr" =~ ^[0-9]+$ ]]; then
    echo "Invalid CIDR notation: $input"
    stat=$?
    exit 1
  fi
  if (( cidr < 0 || cidr > 32 )); then
    echo "CIDR notation out of range: $input"
    stat=$?
    
    exit 1
  fi
else
  # Input is a netmask
  # Split the netmask into four octets
  IFS='.' read -r -a octets <<< "$input"
  
  # Check that there are exactly four octets
  if [[ ${#octets[@]} -ne 4 ]]; then
    echo 
    echo "Invalid netmask: $input"
    exit 1
  fi
  
  # Check that each octet is a valid number between 0 and 255
  for octet in "${octets[@]}"; do
    if ! [[ $octet =~ ^[0-9]+$ ]] || (( octet > 255 )); then
      echo "Invalid netmask: $input"
      exit 1
    fi
  done
  
  # Check that the netmask is contiguous
  binary=$(echo "obase=2; ${octets[0]}" | bc)
  binary+="$(echo "obase=2; ${octets[1]}" | bc)"
  binary+="$(echo "obase=2; ${octets[2]}" | bc)"
  binary+="$(echo "obase=2; ${octets[3]}" | bc)"
  if [[ $(echo "$binary" | grep -o '01' | wc -l) -gt 1 ]]; then
    echo "Invalid netmask: $input"
    exit 1
  fi
  
  
  
  
  IFS='.' read -r -a octets <<< "$input"
  binary=""
  for octet in "${octets[@]}"; do
  binary+=$(printf '%08d' $(bc <<< "ibase=10; obase=2; $octet"))
  done

# Count the number of consecutive 1's in the binary netmask
 cidr=$(echo "$binary" | awk -F '0' '{print length($1)}')

fi

  echo "/$cidr"

}


function validdns() {

local  stat=1

read domain_name <<< $1

# Use nslookup command to check if DNS record exists
if nslookup "$domain_name" > /dev/null; then
  stat=$?
else
  stat=$?
fi

return $stat


}





#ii=$(validate_netmask "$1")



#echo "klklklk : $ii"





#interface="eth0"
#ips=(192.168.1.103 192.168.1.210 192.168.1.213)
#netmasks=(255.0.0.0 255.255.0.0 255.255.255.0)
#gateway=10.42.0.145
#ldns=(8.8.8.8 4.2.2.3)

read -ra interface <<< $1
read -ra ips <<< $2
read -ra netmasks <<< $3
read -ra gateway <<< $4
read -ra ldns <<< $5


sudo sed -i '/config_'$interface'=/d' /etc/conf.d/net
sudo sed -i '/routes_'$interface'=/d' /etc/conf.d/net
sudo sed -i '/dns_servers_'$interface'=/d' /etc/conf.d/net

# Loop through the lists of IPs and netmasks and write to file


ip_netmask="config_$interface=\""

for i in "${!ips[@]}"
do

  ip=${ips[i]}
  netmask=${netmasks[i]}
  
  if valid_ip $ip && valid_netmask $netmask; then
  	cnvnetmask=$(converter_netmask "$netmask")
  	ip_netmask="${ip_netmask}"" "
        ip_netmask="${ip_netmask}""${ip}""$cnvnetmask"
  else
    echo "Invalid IP or netmask: ${ip}/${netmask}"
  fi
done


echo "$ip_netmask\"" >> /etc/conf.d/net


# Write gateway and DNS settings to file
if valid_ip $gateway; then
  echo "routes_$interface=\"default via ${gateway}\"" >> /etc/conf.d/net
else
  echo "Invalid gateway IP: ${gateway}"
fi

dns_net="dns_servers_$interface=\""
for d in "${!ldns[@]}"
do

  dns=${ldns[d]}
  
  if validdns $dns; then
      dns_net="${dns_net}"" "
      dns_net="${dns_net}""${dns}"
  else
  	echo "Invalid Dns : $dns"
done

echo "$dns_net\"" >> /etc/conf.d/net

