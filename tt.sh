#1/bin/bash


# Use the df command to get information about mounted partitions
df -Th | awk '{print $1,$2,$3,$4,$5,$6,$7}' | sed '1d' | while read line
do
    # Get the fields from the line
    filesystem=$(echo $line | awk '{print $1}')
    type=$(echo $line | awk '{print $2}')
    size=$(echo $line | awk '{print $3}')
    used=$(echo $line | awk '{print $4}')
    avail=$(echo $line | awk '{print $5}')
    mounton=$(echo $line | awk '{print $7}')

    # Print the partition information
    echo "Filesystem: $filesystem"
    echo "Type: $type"
    echo "Used: $used"
    echo "Size: $size"
    echo "Avail: $avail"
    echo "Mounted on: $mounton"
    echo "-------------------------------------"

    sleep 10
done
