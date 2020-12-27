#!/usr/bin/env python3

#import logging

import os
import re
import random
from time import sleep

import RPi.GPIO as GPIO
from omxplayer.player import OMXPlayer

#logging.basicConfig(level=logging.DEBUG)

# Set up regex to check for qualifying files.
vid_files = re.compile('\.(mkv|mp4)$', re.IGNORECASE)

# Set up buttons to BCM GPIO and directories
button_red = {'gpio': 26, 'dir': '/home/pi/Videos/button_red/', 'episodes': []}
button_blue = {'gpio': 21, 'dir': '/home/pi/Videos/button_blue/', 'episodes': []}
button_green = {'gpio': 20, 'dir': '/home/pi/Videos/button_green/', 'episodes': []}

# Choose an active cartoon to autostart
active_cartoon = "button_red"

# Set up GPIO to BCM and pull up pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(button_red['gpio'], GPIO.IN, GPIO.PUD_UP)
GPIO.setup(button_blue['gpio'], GPIO.IN, GPIO.PUD_UP)
GPIO.setup(button_green['gpio'], GPIO.IN, GPIO.PUD_UP)

class ToonPlayer(object):
    """omxplayer-wrapper throws an exception if it can't find an
    active dbus listing.  This isn't really what I want so I'll
    fix that with my own class and some composition.

    -b is here to black out the background terminal.
    """

    def __init__(self, source):
        self._player = OMXPlayer(source, '-b')
        sleep(2)
    
    def play(self, source):
        self._player.load(source)

    def seek(self, time):
        self._player.seek(time)

    def active(self):
        try:
            if self._player.is_playing():
                return True
            else:
                return False
        except Exception as ex:
            return False


def verify_episodes(cartoon):
    """ This uses regex to match qualifying video files."""
    episode_list = []

    for _file in os.listdir(cartoon):
        if vid_files.search(_file):
            episode_list.append(_file)

    return episode_list


# Funtion to play cartoon.
def play_cartoon(cartoon):
    """ Play the cartoon passed in, pop the episode off of the list,
    and return the cartoon name to be used for continious play.

    I'm sure I could save some reduntant code here.
    """

    if cartoon == 'button_red':
        player.play(button_red['dir'] + button_red['episodes'].pop())
        sleep(2)

    elif cartoon == 'button_blue':
        player.play(button_blue['dir'] + button_blue['episodes'].pop())
        sleep(2)

    elif cartoon == 'button_green':
        player.play(button_green['dir'] + button_green['episodes'].pop())
        sleep(2)

    else:
        pass
    
    return cartoon


# Load valid videos
button_red['episodes'] = verify_episodes(button_red['dir'])
button_blue['episodes'] = verify_episodes(button_blue['dir'])
button_green['episodes'] = verify_episodes(button_green['dir'])

# Shuffle episodes
random.shuffle(button_red['episodes'])
random.shuffle(button_blue['episodes'])
random.shuffle(button_green['episodes'])

if __name__ == '__main__':
    # Instantiate player with autostart episode
    player = ToonPlayer(button_red['dir'] + button_red['episodes'].pop())

    # Blocking loop
    while True:
    
        # Reload and re-shuffle episode lists if they're empty.
        if len(button_red['episodes']) < 1:
            button_red['episodes'] = verify_episodes(button_red['dir'])
            random.shuffle(button_red['episodes'])
    
        if len(button_blue['episodes']) < 1:
            button_blue['episodes'] = verify_episodes(button_blue['dir'])
            random.shuffle(button_blue['episodes'])
    
        if len(button_green['episodes']) < 1:
            button_green['episodes'] = verify_episodes(button_green['dir'])
            random.shuffle(button_green['episodes'])
    
    
        # Pole buttons for presses.
        if GPIO.input(button_red['gpio']) == 0:
            active_cartoon = play_cartoon('button_red')
            print(active_cartoon)
    
        if GPIO.input(button_blue['gpio']) == 0:
            active_cartoon = play_cartoon('button_blue')
            print(active_cartoon)
    
        if GPIO.input(button_green['gpio']) == 0:
            active_cartoon = play_cartoon('button_green')
            print(active_cartoon)
    
    
        # Continue playing active cartoon.
        if not player.active():
            play_cartoon(active_cartoon)
            print(active_cartoon)
    
        sleep(0.03)

