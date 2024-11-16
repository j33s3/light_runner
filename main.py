# For lights
import board
from pixel_controller import PixelController




# Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
# NeoPixels must be connected to D10, D12, D18 or D21 to work.
pixel_pin = board.D18

# The number of NeoPixels
num_pixels = 300







def main():
    controller = PixelController(board.D18, 300)

    controller.set_state(True)


    while controller.get_state():
        print(
'''******************
Please enter a choice
0. Power Off
1. Power On
2. Change Brightness
3. Change Color
******************''')

        option = int(input(">"))

        if(option == 0):
            controller.set_state(False)
            break
        elif(option == 1):
            controller.set_state(True)
        elif(option == 2):
            while True:
                brightness = float(input("Enter a number between 0 and 100 "))
                if(brightness <= 100 and brightness >= 0):
                    controller.set_brightness(brightness / 100.0)
                    controller.save_state()

                    break
                print("Please enter a valid number")
        else:

            red = -1
            while red < 0 or red > 255:
                red = int(input("Enter a value for red (0 - 255)"))

            green = -1
            while green < 0 or green > 255:
                green = int(input("Enter a value for red (0 - 255)"))

            blue = -1
            while blue < 0 or blue > 255:
                blue = int(input("Enter a value for red (0 - 255)"))

            controller.set_color((red, green, blue))

    controller.save_state()
    

if __name__ == "__main__":
    main()