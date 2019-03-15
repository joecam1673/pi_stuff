#!/usr/bin/python

# import probably too much stuff
import RPi.GPIO as GPIO
import os
import sys
import time
import random
import subprocess 


# initiate variables for use in functions
episode = None
omxc = None
previousEpisode = []

# set up the GPIO stuff for the PI buttons
GPIO.setmode(GPIO.BOARD)
simpsonsButton = 13
disenchantmentButton = 16
futuramaButton = 33
GPIO.setup(simpsonsButton, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(disenchantmentButton, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(futuramaButton, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 

# set variables for directories with video files
simpsonsDirectory = "/home/pi/Videos/Simpsons/"
futuramaDirectory = "/home/pi/Videos/Futurama/"
disenchantmentDirectory = "/home/pi/Videos/Disenchantment/"

# functions for each show / button

## works-ish but sloppy and old
def playSimpsons():
    episode = random.choice(os.listdir(simpsonsDirectory))
    os.system('killall omxplayer.bin')
    omxc = subprocess.Popen(['omxplayer', '-b', simpsonsDirectory + episode, ' &'])
    time.sleep(.3)

## works-ish but sloppy and old
def playFuturama():
    episode = random.choice(os.listdir(futuramaDirectory))
    os.system('killall omxplayer.bin')
    omxc = subprocess.Popen(['omxplayer', '-b', futuramaDirectory + episode, ' &'])
    time.sleep(.3)

## works-ish but sloppy and old
def playDisenchantment():
    episode = random.choice(os.listdir(disenchantmentDirectory))
    os.system('killall omxplayer.bin')
    omxc = subprocess.Popen(['omxplayer', '-b', disenchantmentDirectory + episode, ' &'])
    time.sleep(.3)

# main code to wait for button presses.  
try: 
    while True:
        if GPIO.input(simpsonsButton) == 1:
            playSimpsons()
    
        if GPIO.input(futuramaButton) == 1:
            playFuturama()
    
        if GPIO.input(disenchantmentButton) == 1:
            playDisenchantment()

# reset GPIO on ctrl-c
except KeyboardInterrupt:
    GPIO.cleanup()

