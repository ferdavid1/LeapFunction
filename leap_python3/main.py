import Leap
import pygame
import numpy as np
import time
import serial
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
	p = pyaudio.PyAudio()
	stream = self.p.open(format=pyaudio.paFloat32,
                         channels=1,
                         rate=48000,
                         output=True,
                         output_device_index=1
                         )
	# Assuming you have a numpy array called samples
	data = audioarray.astype(np.float32).tostring()
	stream.write(data)
	stream.close()

def main():
    # Create a sample listener and controller
    listener = SampleListener()
    controller = Leap.Controller()

    # Have the sample listener receive events from the controller
    controller.add_listener(listener)
    # Keep this process running until Enter is pressed
    print("Press Control+C to quit...\n")
    def drawgame():
    	t = True
    	start = input("Press s to start.\n")
    	while serialArduino.inWaiting()==0:
    		pass
    	val = serialArduino.readline()
    	# the following statement will be replaced with a start button attached to the pi
    	if val == 10: # replace with pi gpio button input read
	        s = 45 # number of sections
	        l = 15 # length (mm) of sections
	        y = 235 # y position
	        bands = np.arange(15, 15+(s*l), step=l)
	        audioval = np.array([])
	        try:
		        while t == True:
		        	val = serialArduino.readline()
		        	if val == 01:
		        		t == False # to kill the loop
			        pygame.draw.line(screen, WHITE, [10, 30], [10, 470], 5) # y axis
			        pygame.draw.line(screen, WHITE, [10, 470], [700, 470], 5) # x axis
			        for f_region in bands: # frequency ranges
			        	if f_region+l-5 > scaled[0] > f_region:
				        	pygame.draw.line(screen, DARKGREEN, [f_region, y], [f_region+l - 5, 470-scaled[1]], 5) # changed "y+scaled" to "y-scaled" because y increases in the -y direction for some reason
				        	pygame.display.flip()
				        	audioval += scaled[1] # these are the raw interpreted audio values we will connect
				        	time.sleep(0.02)
				        else:
					        pygame.draw.line(screen, DARKGREEN, [f_region, y], [f_region+l - 5, y], 5)
				        	pygame.display.flip()
		        	screen.fill(pygame.Color("black")) # clear the screen
		    	# u only get to here if the while loop is broken
		    	# here u now have all the values needed to output audio
		    	print(audioval)
		    	# add parameter for frequency/pitch
		    	play(audioval)
		    	drawgame()
	        except KeyboardInterrupt:
	        	pygame.quit()
	        	controller.remove_listener(listener)

if __name__ == "__main__":
	main()