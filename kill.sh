PID=$(ps aux | grep 'python runner' | grep -v grep | awk '{ print $2}' )
echo $PID
kill -9 $PID
