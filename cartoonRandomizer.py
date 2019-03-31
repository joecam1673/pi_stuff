#!/usr/bin/python3

import RPi.GPIO as GPIO
from omxplayer import OMXPlayer
import os, random

# set up the GPIO stuff for the PI buttons
GPIO.setmode(GPIO.BOARD)

simpsonsButton = 13
disenchantmentButton = 16
futuramaButton = 33

GPIO.setup(simpsonsButton, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(disenchantmentButton, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(futuramaButton, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 

simpsonsDir = "/home/pi/Videos/Simpsons/"
disenchantmentDir = "/home/pi/Videos/Disenchantment/"
futuramaDir = "/home/pi/Videos/Futurama/"

simpsonsEpisodes = os.listdir(simpsonsDir)
disenchantmentEpisodes = os.listdir(disenchantmentDir)
futuramaEpisodes = os.listdir(futuramaDir)

#        if GPIO.input(disenchantmentButton) == 1:
#            playDisenchantment()

if __name__ == "__main__":
    while True:
        if GPIO.input(simpsonsButton) == 1:
            try:
                if player.is_playing():
                    if len(simpsonsEpisodes) == 0:
                        simpsonsEpisodes = os.listdir(simpsonsDir)

                    os.chdir(simpsonsDir)
                    simpsonsEpisode = random.choice(simpsonsEpisodes)
                    simpsonsEpisodes.remove(simpsonsEpisode)
                    player.load(simpsonsEpisode)

            except:
                    os.chdir(simpsonsDir)
                    simpsonsEpisode = random.choice(simpsonsEpisodes)
                    simpsonsEpisodes.remove(simpsonsEpisode)
                    player = OMXPlayer(simpsonsEpisode, '-b')

#        if GPIO.input(disenchantmentButton) == 1:
#            os.chdir(disenchantmentDir)
#            episode = random.choice(disenchantmentEpisodes)
#            disenchantmentEpisodes.remove(episode)
#            player = OMXPlayer(episode, '-b')
#
#        if GPIO.input(futuramaButton) == 1:
#            os.chdir(futuramaDir)
#            episode = random.choice(futuramaEpisodes)
#            futuramaEpisodes.remove(episode)
#            player = OMXPlayer(episode, '-b')
