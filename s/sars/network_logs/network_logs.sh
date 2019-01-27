#!/bin/bash
declare -a namesArr
declare -a dataArr
declare -a server
declare -a DBservers
exist="0"
dirName= $1
cd /var/log/dirName
counter=0 #these variable will be used as the counter
x=0
#--------------------------------------------------------------------------------------------------------------
for currItem in *
do
  if [ -d $currItem ]
  then
    namesArr[$counter]=$currItem
  fi
    echo "${namesArr[$counter]}" >>  /tmp/server.txt    #writing server names to a file.
  let " counter=counter+1"
done
#--------------------------------------------------------------------------------------------------------------
#mysql -u root -D network_logs -e "LOAD DATA LOCAL INFILE '/tmp/server.txt' INTO TABLE server FIELDS TERMINATED BY ';' LINES TERMINATED BY '\n' IGNORE 1 LINES (@col1) set serverName=@col1;"
# get all server names so we can compare with the severs in the directory
#-----------------------------------------------------------------------------------------------------------------
#checkServers
function checkServers()
{
   #  get all server names so we can compare with the severs in the directory
   query=$(mysql -N -u root -ppointers -h 10.8.11.225 -D network_logs -e "select server_name FROM network_logs_server;")
   DBservers=($(for currServer in $query; do echo $currServer ; done))
#  echo "1"  ${DBservers[@]}
   #check how many servers are stored int the array
   count=$(echo ${#DBservers[@]})
   # echo $count
   #echo  "${DBserver[@]}"
   true > /tmp/network_logs_server.txt
   # now do the check if there are servers that needs to be uploaded into the db
   for ((x=0; x<$counter; x++))
   do
     echo "${namesArr[x]}"
      for ((y=0; y<$count; y++))
      do
          if [[ "${namesArr[$x]}" = "${DBservers[$y]}" ]]
          then
             exist="1"
             break
          fi
      done
      if [[ "$exist" != "1" ]]
      then
          echo "${namesArr[$x]}" >> /tmp/network_logs_server.txt
      fi
  done
     if [[ -f "/tmp/network_logs_server.txt" && -s "/tmp/network_logs_server.txt" ]]
     then
       echo "loading data"
#       mysql -u root -D network_logs -e "LOAD DATA LOCAL INFILE '/tmp/server.txt' INTO TABLE server FIELDS TERMINATED BY ';' LINES TERMINATED BY '\n' (@col1) set serverName=@col1;"
      mysqlimport --fields-terminated-by=';' --columns=server_name --verbose --local -u root -ppointers -h 10.8.11.225  network_logs  /tmp/network_logs_server.txt
       echo "done"
     else
        echo "file empty or no new servers found"
     fi
}
#----------------------------------------------------------------------------------------------------------------
function loadData()
{
  dateCnt=0
  for ((x=0;x<$counter;x++))
  do
   cd /var/log/networks/"${namesArr[$x]}"
      for logDate in *
      do
        if [ -d $logDate ]
        then
           cd "${logDate}" # && echo "$(pwd)" # && cat local7
           file="$(ls)"
           while read line
           do
              logTime="$(echo ${line} | awk '{print $3}')"
              stringsToRemove="$(echo ${line} | awk '{print $1,$2,$3,$4}')"
              data="$(echo ${line} | sed -r "s/${stringsToRemove}//")"
          # we need the server ID at these point before we write the log to the file thus selecting the correct server in the db is important;
              serverID=$(mysql -u root -N -ppointers -h 10.8.11.225 -D network_logs -e "SELECT serverId FROM network_logs_server WHERE server_name='${namesArr[$x]}';")
         #  echo "${serverID} 1 ${namesArr[$x]}  2 " >> /tmp/ll.txt
           echo "${logDate};${data};${serverID};${logTime}" >>  /tmp/network_logs_log.txt
           done <$file
           cd ..
         fi
      done
    done
mysqlimport --fields-terminated-by=';' --columns=logDate,log_desc,serverID_id,log_time --verbose -h 10.8.11.225 --local -u root -ppointers network_logs  /tmp/network_logs_log.txt
}
#----------Call functions accordingly
  checkServers
  loadData
#clear the tmp files accordingly
#cp /tmp/log.txt /tmp/network_logs_log.txt
#cp /tmp/server.txt /tmp/network_logs_server.txt
true > /tmp/network_logs_server.txt
true > /tmp/network_logs_log.txt
