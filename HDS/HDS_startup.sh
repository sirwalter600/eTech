sudo ifconfig wlan0 down
sudo ifconfig wwan0 down
sudo pon

sudo rfcomm unbind /dev/rfcomm0 10:C6:FC:E3:68:32
sudo rfcomm bind /dev/rfcomm0 10:C6:FC:E3:68:32
rfcomm
