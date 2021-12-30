#!/usr/bin/python3
# -*- coding:utf-8 -*-
import sys
import os
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd2in7
import time
from PIL import Image,ImageDraw,ImageFont

import netifaces as ni
import traceback

logging.basicConfig(level=logging.DEBUG)

try:

    logging.info("epd2in7 Demo")
    epd = epd2in7.EPD()

    '''2Gray(Black and white) display'''
    logging.info("init and Clear")
    epd.init()
    epd.Clear(0xFF)
#    font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
#    font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)
#    font35 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 35)
    font18 = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', 18)
    font10 = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', 10)
    font12 = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', 12)
    font9 = ImageFont.truetype('/usr/share/fonts/truetype/noto/NotoMono-Regular.ttf', 9)
    # Drawing on the Horizontal image
    logging.info("1.Drawing on the Horizontal image...")
    Himage = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
    draw = ImageDraw.Draw(Himage)
#    IP=os.popen("hostname -I").read().split()
    try:
      NETINFO0=ni.ifaddresses('eth0')
      IP0=NETINFO0[2][0]['addr']
    except ValueError:
      IP0="Not Detected"
    except KeyError:
      IP0="Not Detected"

    try:
      NETINFO1=ni.ifaddresses('wlan0')
      IP1=NETINFO1[2][0]['addr']
    except ValueError:
      IP1="Not Detected"
    except KeyError:
      IP1="Not Detected"

    HNAME=os.popen('hostname').read().rstrip()
    UPTIME=os.popen('uptime | cut -d"," -f1').read().rstrip()
    STOSIZE=os.popen("df -h | grep -A1 Filesystem | tail -1 | awk '{print $2}'").read().rstrip()
    STOUSED=os.popen("df -h | grep -A1 Filesystem | tail -1 | awk '{print $3}'").read().rstrip()
    STOPERC=os.popen("df -h | grep -A1 Filesystem | tail -1 | awk '{print $5}'").read().rstrip()

    draw.text((10, 5), "[ "+HNAME+" ]", font = font18, fill = 0)
    draw.text((10, 25),  'eth0 : '+IP0, font = font18, fill = 0)
    draw.text((10, 45), 'wlan0: '+IP1, font = font18, fill = 0)
#    draw.text((10, 140), os.popen('df -h | grep -A1 Filesystem').read(), font=font9, fill=0)
    draw.text((10, 100), 'Power off ...', font = font18, fill=0)

    draw.text((10, 120), "Storage: "+STOUSED+"/"+STOSIZE+","+STOPERC, font=font12,fill=0)
    draw.text((10, 134), "Uptime :"+UPTIME, font=font12, fill=0)
    draw.text((10, 154), "[Key1=Refresh] [Key2=PowerOFF]", font=font12, fill=0)



    epd.display(epd.getbuffer(Himage))
    time.sleep(2)

#    logging.info("Clear...")
#    epd.Clear(0xFF)
    logging.info("Goto Sleep...")
    epd.sleep()

except IOError as e:
    logging.info(e)

except KeyboardInterrupt:
    logging.info("ctrl + c:")
    epd2in7.epdconfig.module_exit()
    exit()
