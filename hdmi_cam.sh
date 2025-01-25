#! /usr/bin/bash

display_connected=0

# Check the status file of each display output
check_displays () {
	for d in /sys/class/drm/*/
	do
		if [ -f $d/status ]
		then
			if [ "$(cat $d/status)" = "connected" ]
			then
				display_connected=1
			fi
		fi
	done
}

check_displays

# Just keep checking until a display is detected
if [ $display_connected -eq 0 ]
then 
	echo "Waiting for display to be connected..."
	while [ $display_connected -eq 0 ]
	do
		sleep 5s
		check_displays
	done
	echo "Display connected."
fi

/home/pi/bin/hdmi_cam_ctl.py
