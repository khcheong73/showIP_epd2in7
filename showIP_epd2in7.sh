#!/bin/bash

SECONDS=0
TIMEOUT=1800
python3 /root/epd/showIP_epd2in7.py

while :; do
  if [ $SECONDS -gt $TIMEOUT ]; then
    SECONDS=0
    python3 /root/epd/showIP_epd2in7.py
  fi

  # If Key 1 is pressed, display will be refreshed
  if [ $(gpio read 21) -eq 0 ]; then
    SECONDS=0
    python3 /root/epd/showIP_epd2in7.py
  fi
  if [ $(gpio read 22) -eq 0 ]; then
    SECONDS=0
    python3 /root/epd/showPWROFF_epd2in7.py
    sudo shutdown -h now
  fi


  sleep 1
done
