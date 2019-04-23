import Leap
import pygame
import numpy as np
import time
import serial
import sounddevice as sd
pygame.init()
serialArduino = serial.Serial('/dev/ttyACM0', 9600)

BLACK = (0,0,0)
WHITE = (255,255,255)
DARKGREEN = (0,122,0)
# BLUE = (0,0,255)

size = (750, 500)
screen = pygame.display.set_mode(size)
scaled = [0.0, 0.0]

def scale(leapcoor): # takes the current leap coordinates 
	# xapp = (xleap - xleapstart)(xapprange/xleaprange) + xappstart
	# where xleaprange = xleapend - xleapstart && xapprange = xappend - xappstart
	xleaprange = float(180*2) # 180 - - 180 = 180 + 180 = 180*2 
	scaledx = (leapcoor[0] + 180.0)*(750.0/xleaprange) # + 0 
	yleaprange = 463.0
	scaledy = (leapcoor[1])*(500.0/yleaprange) # + 0
	return [scaledx, scaledy]

class SampleListener(Leap.Listener):
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']

    def on_init(self, controller):
        print("Initialized")

    def on_connect(self, controller):
        print("Connected")

    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print("Disconnected")

    def on_exit(self, controller):
        print("Exited")

    def on_frame(self, controller):
        # Get the most recent frame and report some basic information
        frame = controller.frame()
        pointable = frame.pointables.frontmost
        tip = pointable.tip_position 
        global scaled 
        scaled = scale(tip)
        # print(scaled)

def play(audioarray):
	audioarray = np.array(audioarray)/40
	for ind, a in enumerate(audioarray[:-1]):
		for r in np.arange(a, audioarray[ind + 1], step=0.02):
			audioarray = np.insert(audioarray, ind + 1, r)
	print(len(audioarray))
	sd.play(audioarray, 24000)
	print("Draw!!")
	# time.sleep(2)

def main():
    # Create a sample listener and controller
    listener = SampleListener()
    controller = Leap.Controller()
    print("Press the first button to start.\n")
    # Have the sample listener receive events from the controller
    controller.add_listener(listener)
    # Keep this process running until Enter is pressed
    def drawgame():
    	audioval = []
    	s = 45 # number of sections
    	l = 15 # length (mm) of sections
    	y = 235 # y position
    	bands = np.arange(15, 15+(s*l), step=l)
    	for x in range(130): # how many times you do this. modulate w a pot
	    	pygame.draw.line(screen, WHITE, [10, 30], [10, 470], 5) # y axis
	    	pygame.draw.line(screen, WHITE, [10, 470], [700, 470], 5) # x axis
	    	for f_region in bands: # frequency ranges
	    		if f_region+l-5 > scaled[0] > f_region:
		    		pygame.draw.line(screen, DARKGREEN, [f_region, y], [f_region+l - 5, 470-scaled[1]], 5) # changed "y+scaled" to "y-scaled" because y increases in the -y direction for some reason
		    		pygame.display.flip()
		    		audioval.append(int(scaled[1] - 240)) # these are the raw interpreted audio values we will connect
		    		# print(len(audioval))
		    		print(int(scaled[1] - 240))
		    		time.sleep(0.01)
		    	else:
		    		pygame.draw.line(screen, DARKGREEN, [f_region, y], [f_region+l - 5, y], 5)
		    		pygame.display.flip()
    		screen.fill(pygame.Color("black")) # clear the screen
    	# print(audioval)
    	play(audioval)
    	drawgame()
    print("Press Control+C to quit...\n")
    try:
    	val = ''
    	for x in range(10000):
    		if val != '10':
	    		val = serialArduino.readline()[:2].decode("cp437")
    		else:
    			break
    	drawgame()
    except KeyboardInterrupt:
    	pygame.quit()
    	controller.remove_listener(listener)

if __name__ == "__main__":
	main()