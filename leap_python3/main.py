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
        tip = [tip[0], tip[1]] # x and y axes only
        while True:
			pygame.draw.line(screen, WHITE, [10, 30], [10, 470], 5) # y axis
			pygame.draw.line(screen, WHITE, [10, 470], [700, 470], 5) # x axis
			s = 45 # number of sections
			l = 15 # length (mm) of sections
			y = 235 # y position
			for f_region in np.arange(15, 15+(s*l), step=l): # frequency ranges
				pygame.draw.line(screen, DARKGREEN, [f_region, y], [f_region+l - 5, y], 5)
			pygame.display.flip()


def main():
    # Create a sample listener and controller
    listener = SampleListener()
    controller = Leap.Controller()

    # Have the sample listener receive events from the controller
    controller.add_listener(listener)
    # Keep this process running until Enter is pressed
    print("Press Enter to quit...")
    try:
        while True:
            pass
    except KeyboardInterrupt:
        controller.remove_listener(listener)
    finally:
        # Remove the sample listener when done
        controller.remove_listener(listener)


if __name__ == "__main__":
    main()