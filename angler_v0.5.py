import board
import displayio
import adafruit_displayio_ssd1306
import terminalio
from adafruit_display_text import label
from adafruit_bitmap_font import bitmap_font
import time
import array
import math
import adafruit_bno055
#import audiobusio
#import adafruit_apds9960.apds9960
#import adafruit_bmp280
#import adafruit_lis3mdl
import adafruit_lsm6ds.lsm6ds33
#import adafruit_sht31d

# Hardware Definition

displayio.release_displays()

i2c = board.I2C()
display_bus = displayio.I2CDisplay(i2c, device_address=0x3c, reset=board.D9)
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=32)
dof_sensor = adafruit_bno055.BNO055_I2C(i2c)

## Feather Sense Sensors

#apds9960 = adafruit_apds9960.apds9960.APDS9960(i2c)
#bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)
#lis3mdl = adafruit_lis3mdl.LIS3MDL(i2c)
accelerometer = adafruit_lsm6ds.lsm6ds33.LSM6DS33(i2c)
#sht31d = adafruit_sht31d.SHT31D(i2c)
#microphone = audiobusio.PDMIn(board.MICROPHONE_CLOCK, board.MICROPHONE_DATA,
#                              sample_rate=16000, bit_depth=16)


## Make the display context
splash = displayio.Group(max_size=10)
display.show(splash)

#color_bitmap = displayio.Bitmap(128, 32, 1)
#color_palette = displayio.Palette(1)
#color_palette[0] = 0xFFFFFF  # White

#bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
#splash.append(bg_sprite)

## Draw a smaller inner rectangle
#inner_bitmap = displayio.Bitmap(124, 28, 1)
#inner_palette = displayio.Palette(1)
#inner_palette[0] = 0x000000  # Black
#inner_sprite = displayio.TileGrid(inner_bitmap, pixel_shader=inner_palette, x=1, y=1)
#splash.append(inner_sprite)

## Draw a label
#text = "Hello World!"
#text_area = label.Label(terminalio.FONT, text=text, color=0xFFFF00, x=1, y=1)
#splash.append(text_area)

# Software Definition

## Load Font
font = bitmap_font.load_font("/AmericanTypewriter-Semibold-16.bdf")
font.load_glyphs(b"' AEFGHIJKMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789")
text = "Initializing..."
text_area = label.Label(font, text=text, color=0xFFFF00, x=5, y=15)
splash.append(text_area)


# Function Definition

x0 = 0.1
y0 = -.09
z0 = 10.11

def normalized_rms(values):
    minbuf = int(sum(values) / len(values))
    return int(math.sqrt(sum(float(sample - minbuf) *
                             (sample - minbuf) for sample in values) / len(values)))


def calc_angle(x, y, z):
    x = x - x0
    y = y - y0
    z = z = z0
    x2 = x*x
    y2 = y*y
    z2 = z*z
    result = math.sqrt(x2 + z2)
    result = y/result
    # assuming accelerometer returns (z, x, y)
    angle = (math.atan(result)*100)
    return angle

def calc_cos_angle(x, y):
    x2 = x*x
    y2 = y*y
    angle = (math.cos(x2/y2))*100
    angle = 90 - angle
    return angle

# Global Variables

#apds9960.enable_proximity = True
#apds9960.enable_color = True

### Set this to sea level pressure in hectoPascals at your location for accurate altitude reading.
#bmp280.sea_level_pressure = 1013.25

# Main Loop

while True:
    #samples = array.array('H', [0] * 160)
    #microphone.record(samples, len(samples))
    '''acc = accelerometer.acceleration
    x = acc[0]
    y = acc[1]
    z = acc[2]
    print("x = ", acc[0])
    print("y = ", acc[1])
    print("z = ", acc[2])
    text = "{:.1f} {:.1f} {:.1f}".format(*accelerometer.acceleration)
    print("Acceleration: {:} {:} {:} m/s^2".format(*accelerometer.acceleration))
    angle = calc_angle(x, y, z)
    angle2 = calc_cos_angle(y,z)
    print("y angle = ", angle)
    print("y cos angle = ", angle2)
    '''
    dof = dof_sensor.euler
    angle = dof[2]
    text = "Angle: {:.1f}".format(angle)
    print("text = ", text)
    print("Euler angle: {}".format(dof_sensor.euler))
    #text_area = label.Label(font, text=text, color=0xFFFF00, x=5, y=15)
    #splash.append(text_area)
    text_area.text = text
    time.sleep(0.01)
    #splash.pop()
#    splash.pop(text_area)
    #print("\nFeather Sense Sensor Demo")
    #print("---------------------------------------------")
    #print("Proximity:", apds9960.proximity)
    #print("Red: {}, Green: {}, Blue: {}, Clear: {}".format(*apds9960.color_data))
    #print("Temperature: {:.1f} C".format(bmp280.temperature))
    #print("Barometric pressure:", bmp280.pressure)
    #print("Altitude: {:.1f} m".format(bmp280.altitude))
    #print("Magnetic: {:.3f} {:.3f} {:.3f} uTesla".format(*lis3mdl.magnetic))
    #print("Acceleration: {:.2f} {:.2f} {:.2f} m/s^2".format(*lsm6ds33.acceleration))
    #print("Gyro: {:.2f} {:.2f} {:.2f} dps".format(*lsm6ds33.gyro))
    #print("Humidity: {:.1f} %".format(sht31d.relative_humidity))
    #print("Sound level:", normalized_rms(samples))