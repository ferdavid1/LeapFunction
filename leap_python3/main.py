import Leap
import pygame
import numpy as np
pygame.init()

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
        global direction
        scaled = scale(tip)
        direction = pointable.direction
        print(tip, scaled)


def main():
    # Create a sample listener and controller
    listener = SampleListener()
    controller = Leap.Controller()

    # Have the sample listener receive events from the controller
    controller.add_listener(listener)
    # Keep this process running until Enter is pressed
    print("Press Enter to quit...")
    try:
        pygame.draw.line(screen, WHITE, [10, 30], [10, 470], 5) # y axis
        pygame.draw.line(screen, WHITE, [10, 470], [700, 470], 5) # x axis
        s = 45 # number of sections
        l = 15 # length (mm) of sections
        y = 235 # y position
        for f_region in np.arange(15, 15+(s*l), step=l): # frequency ranges
        	pygame.draw.line(screen, DARKGREEN, [f_region, y], [f_region+l - 5, y], 5)
        	pygame.display.flip()
        while True:
	        for f_region in np.arange(15, 15+(s*l), step=l): # frequency ranges
	        	if f_region+l-5 > scaled[0] > f_region:
	        		print(direction)
		        	pygame.draw.line(screen, DARKGREEN, [f_region, y], [f_region+l - 5, y+scaled[1]], 5)
		        	pygame.display.flip()
		        else: 
		        	pass
    except KeyboardInterrupt:
    	pygame.quit()
    	controller.remove_listener(listener)
    finally:
    	# Remove the sample listener when done
    	controller.remove_listener(listener)

if __name__ == "__main__":
    main()