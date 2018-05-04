ss=$1
total_mem=`free -k|grep '^Mem'|awk '{print $2;}'`
while true
do
        current_date=$(date '+%d/%m/%Y %H:%M:%S')
        current_percent_mem=$(ps -ux|awk '{print $2 " " $4;}'|grep "$process " |grep -v 'grep' |awk '{print $2;}')
        if [[ "$current_percent_mem" = "" ]];
        then
                used_mem_GiB="0"
        else
#                used_mem_GiB=$(echo "$current_percent_mem/100*$total_mem/1024/1024"|bc -l)
		used_mem_GiB=$current_percent_mem
        fi
        echo "$current_date $used_mem_GiB" 2>&1
        if [[ "$used_mem_GiB" == "0" ]];
        then
                exit 0
        fi
        sleep 1
done
