#!/bin/sh

# Copyright (C) 2017-2018 Vilniaus Blokas UAB, https://blokas.io/pisound
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the BSD license.  See the LICENSE file for details.
#

. /usr/local/pisound/scripts/common/start_puredata.sh
PATCH="$1"
shift

echo
echo "$PATCH"
echo "$@"


start_puredata(){
	flash_leds 1

	if [ -z `which puredata` ]; then
		log "Pure Data was not found! Install by running: sudo apt-get install puredata"
		flash_leds 100
		exit 1
	fi

	log "Killing all Pure Data instances!"
	killall puredata 2> /dev/null

	PATCH="$1"
	PATCH_DIR=$(dirname "$PATCH")
	shift

	log "Launching Pure Data."
	cd "$PATCH_DIR" && puredata -path /usr/local/bellasynth/pd/lib/ -stderr $NO_GUI -send ";pd dsp 1" "$PATCH" $@ &
	PD_PID=$!

	log "Pure Data started!"
	flash_leds 1
	sleep 0.3
	flash_leds 1
	sleep 0.3
	flash_leds 1

	python3 /usr/local/bellasynth/scripts/ui.py &
	UI_PID=$!

	wait_process $PD_PID
	wait_process $UI_PID
}


(
	# Connect the osc2midi bridge to the MIDI Inputs and to Pure Data.
	sleep 4
	/usr/local/pisound-ctl/connect_osc2midi.sh "pisound-ctl"
	aconnect "pisound-ctl" "Pure Data";
	aconnect -d "Pure Data:1" "pisound-ctl"
) &


start_puredata "$PATCH" $@