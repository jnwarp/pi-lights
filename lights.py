from os import system
import pigpio
import time

# define pins
rgb1 = (0, 16, 21)
rgb2 = (19, 13, 26)

class LightStrip():
	def __init__(self, pins = (20, 16, 21)):
		# initialize pigpio
		self.pi = pigpio.pi()

		# define colors
		colors = {}
		colors['red']		= (255, 0, 0)
		colors['green']		= (0, 255, 30)
		colors['blue']		= (0, 130, 255)
		colors['white']		= (255, 255, 255)

		colors['black'] 	= (0, 0, 0)
		colors['orange']	= (255, 35, 0)
		colors['dorange']	= (255, 15, 0)
		colors['seagreen']	= (0, 255, 50)
		colors['skyblue']	= (0, 255, 255)
		colors['lblue']		= (0, 220, 255)
		colors['dblue']		= (0, 50, 255)
		colors['pink']		= (255, 0, 30)
		colors['purple']	= (255, 0, 200)

		self.colors = colors

		# set initial light color
		self.pins = pins
		self.currentColor = (255, 255, 255, 0)
		self.setColor((255, 255, 255))
	
	def setColor(self, color = 'white', brightness = 255):
		# get the rgb color value ex (255, 255, 0)
		if type(color) == str:
			rgb = self.colors[color]
		else:
			rgb = color

		for i in range(3):
			# skip unset pins
			if self.pins[i] < 1:
				continue

			# set the color for each pin
			level = int(rgb[i] * (brightness / 255))
			self.pi.set_PWM_dutycycle(self.pins[i], level)

		# save the current color
		rgbNow = list(rgb)
		rgbNow.append(brightness)
		self.currentColor = tuple(rgbNow)
	
	def fadeColor(self, color = 'white', brightness = 255):
		# get the rgb color value ex (255, 255, 0)
		if type(color) == str:
			rgb = self.colors[color]
		else:
			rgb = color

		rgbNow = list(self.currentColor)

		# use while loop to fade
		flag = True
		while flag:
			flag = False

			if rgbNow[3] > brightness:
				rgbNow[3] -= 1
				flag = True
			elif rgbNow[3] < brightness:
				rgbNow[3] += 1
				flag = True

			# adjust each color up / down by 1
			for i in range(3):
				if rgbNow[i] > rgb[i]:
					rgbNow[i] -= 1
					flag = True

				elif rgbNow[i] < rgb[i]:
					rgbNow[i] += 1
					flag = True

			# set the colors
			self.setColor(tuple(rgbNow), brightness)


def redAlert():
	system('mpg321 short_red_alert.mp3 &')

	time.sleep(0.5)
	for i in range(5):
		print('beep')
		strip1.setColor('orange') 
		strip2.setColor('orange') 
		time.sleep(1)
		print('boop')
		strip2.setColor('dorange') 
		time.sleep(.5)
		print('boop')
		strip1.setColor('dorange') 
		time.sleep(.4)

def fadeColors(color):
	print(color)
	strip2.fadeColor(color)
	strip1.fadeColor(color)

def setColors(color):
	print(color)
	strip2.setColor(color)
	strip1.setColor(color)

def portalWakeUp():
	system('mpg321 portal.mp3 &')
	time.sleep(4.2)
	fadeColors('white')

	time.sleep(63)

	setColors('orange')

	time.sleep(31)

	fadeColors('dorange')

	time.sleep(42.5)
	fadeColors('skyblue')

	time.sleep(70)
	fadeColors('seagreen')
	

if __name__ == "__main__":
	strip1 = LightStrip(rgb1)
	strip2 = LightStrip(rgb2)

	fadeColors('black')

