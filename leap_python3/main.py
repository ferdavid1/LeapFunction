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
flip = False
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

def rate_scale(ampl_mult): # modulation scaling for sample rate
    val = ampl_mult / 1300
    scaled = 5 + (val*20)
    return scaled

def play(audioarray, ampl_mult):
    const = 5*ampl_mult
    audioarray = np.array(audioarray)/const
    # print(len(audioarray))
    for ind, a in enumerate(audioarray[:-1]):
        for r in np.arange(a, audioarray[ind + 1], step=.05):
            audioarray = np.insert(audioarray, ind + 1, r)
    # print(len(audioarray))
    sd.play(audioarray, 4000)

def main():
    # Create a sample listener and controller
    listener = SampleListener()
    controller = Leap.Controller()
    print("Press the first button to start.\n")
    # Have the sample listener receive events from the controller
    controller.add_listener(listener)
    # Keep this process running until Enter is pressed
    def drawgame(val):
        print("Draw!!\n")
        audioval = []
        s = 45 # number of sections
        l = 15 # length (mm) of sections
        y = 235 # y position
        global flip
        bands = np.arange(15, 15+(s*l), step=l)
        for x in range(130): # modulate? curr 130
            pygame.draw.line(screen, WHITE, [10, 30], [10, 470], 5) # y axis
            pygame.draw.line(screen, WHITE, [10, 470], [700, 470], 5) # x axis
            for f_region in bands: # frequency ranges
                if f_region+l-5 > scaled[0] > f_region:
                    pygame.draw.line(screen, DARKGREEN, [f_region, y], [f_region+l - 5, 470-scaled[1]], 5) # changed "y+scaled" to "y-scaled" because y increases in the -y direction for some reason
                    pygame.display.flip()
                    audioval.append(int(scaled[1] - 240)) # these are the raw interpreted audio values we will connect
                    # print(len(audioval))
                    # print(int(scaled[1]))
                    time.sleep(0.01)
                else:
                    pygame.draw.line(screen, DARKGREEN, [f_region, y], [f_region+l - 5, y], 5)
                    pygame.display.flip()
            pointlist = list(zip([x+10 for x in bands], [(-x+230) for x in audioval]))
            screen.fill(pygame.Color("black")) # clear the screen
        if len(audioval) > 1:
            # print(pointlist)
            for y in range(5000):
                pygame.draw.line(screen, WHITE, [10, 30], [10, 470], 5) # y axis
                pygame.draw.line(screen, WHITE, [10, 470], [700, 470], 5) # x axis
                pygame.draw.lines(screen, WHITE, False, pointlist, 5)
                pygame.display.flip()
        #break
        val = serialArduino.readline().decode("cp437")
        print(val, "1")
        while True:
            val = serialArduino.readline().decode("cp437")
            if ":" not in val or "," not in val:
                pass
            else:
                if val.startswith("01") and flip == False: # its a hold on the second button, check if the last one was
                    flip = True
                    drawgame(val) 
                elif val.startswith("01") and flip == True:
                    pass    
                else:
                    if val.count(",") > 1:
                        pass 
                    else:
                        try:   
                            print(val, "2")
                            ampl_mult = val[val.index(",")+1:val.index(":")]
                            # interval_mult = val[val.index(":")+1:]
                            play(audioval, rate_scale(int(ampl_mult)))
                            flip = False
                            # time.sleep(0.003*int(interval_mult))
                        except ValueError:
                            pass
    print("Press Control+C to quit...\n")
    try:
        val = ''
        for x in range(10000):
            if not val.startswith('10'):
                val = serialArduino.readline()[:2].decode("cp437")
            else:
                break
        drawgame(val)
    except KeyboardInterrupt:
        pygame.quit()
        controller.remove_listener(listener)

if __name__ == "__main__":
    main()