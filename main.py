# For lights
import board
from pixel_controller import PixelController

from Interface import LightInterface




# Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
# NeoPixels must be connected to D10, D12, D18 or D21 to work.
pixel_pin = board.D18

# The number of NeoPixels
num_pixels = 300







def main():
    controller = PixelController(board.D18, 300)

    controller.set_state(True)

    LightInterface(controller).run()
    

if __name__ == "__main__":
    main()