#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
#libraries needed to declare GPIO pins
import mraa

#import times
import time
from time import ctime
from datetime import date

#libraries needed to convert audio to text
import speech_recognition as sr
from pydub import AudioSegment

#libraries needed to record audion from the webcam
import pyaudio
import wave
import os

#libraries for weather
import python_weather
import asyncio

#extra libraries for resonses
from gtts import gTTS
import requests, json
from random import randint

#setting up GPIO pins
E = mraa.Gpio(35)
RS = mraa.Gpio(37)
gpio0 = mraa.Gpio(40)
gpio1 = mraa.Gpio(38)
gpio2 = mraa.Gpio(36)
gpio3 = mraa.Gpio(32)
gpio4 = mraa.Gpio(33)
gpio5 = mraa.Gpio(31)
gpio6 = mraa.Gpio(29)
gpio7 = mraa.Gpio(23)

#GPIO pins for push buttons
Red = mraa.Gpio(3)
Blue = mraa.Gpio(5)

#setting up directions for GPIO pins
E.dir(mraa.DIR_OUT)
RS.dir(mraa.DIR_OUT)
gpio0.dir(mraa.DIR_OUT)
gpio1.dir(mraa.DIR_OUT)
gpio2.dir(mraa.DIR_OUT)
gpio3.dir(mraa.DIR_OUT)
gpio4.dir(mraa.DIR_OUT)
gpio5.dir(mraa.DIR_OUT)
gpio6.dir(mraa.DIR_OUT)
gpio7.dir(mraa.DIR_OUT)

#setting up directions for GPIO pins for push buttons
Red.dir(mraa.DIR_IN)
Blue.dir(mraa.DIR_IN)

#push button flags
bflag = 0
rflag = 0

#LCD printing code 
#command function to initialize the LCD screen
def command(reset,g7,g6,g5,g4,g3,g2,g1,g0):
	RS.write(reset)
	gpio0.write(g0)
	gpio1.write(g1)
	gpio2.write(g2)
	gpio3.write(g3)
	gpio4.write(g4)
	gpio5.write(g5)
	gpio6.write(g6)
	gpio7.write(g7)
	E.write(1)
	time.sleep(0.01)
	E.write(0)
	time.sleep(0.01)
	
	
	
#print function to write into the LCD screen
def printLCD(string):
	for i in range(len(string)):
		char = string[i]
		l = ord(char)
		RS.write(1)
		gpio0.write(l & 1)
		gpio1.write((l & 2) >> 1)
		gpio2.write((l & 4) >> 2)
		gpio3.write((l & 8) >> 3)
		gpio4.write((l & 16) >> 4)
		gpio5.write((l & 32) >> 5)
		gpio6.write((l & 64) >> 6)
		gpio7.write((l & 128) >> 7)
		E.write(1);
		time.sleep(0.010)
		E.write(0);
		time.sleep(0.010)
		command(0,0,0,0,1,1,0,0,0)#command to move the cursor to the left
		time.sleep(0.2)


#begin function to intialize the LCD screen
def begin():
	time.sleep(0.040)
	command(0,0,0,1,1,0,0,0,0) #commands to set one line in the LCD screen
	command(0,0,0,1,1,0,0,0,0) #commands to set one line in the LCD screen
	command(0,0,0,0,0,1,1,1,1) #command to set the Display on
	command(0,0,0,0,0,0,0,0,1) #command to clear the LCD screen
	command(0,0,0,0,0,0,1,1,0) #command for LCD entry mode 
	command(0,1,0,0,0,1,1,1,1) #command to display into the LCD screen by setting the DDRAM address
							   #sets cursor to the top right of the screen
	


	
	


#function to record audio from the webcam
def recordAudio():
	chunk = 1024  # Record in chunks of 1024 samples
	sample_format = pyaudio.paInt16  # 16 bits per sample
	channels = 2
	fs = 44100  # Record at 44100 samples per second
	seconds = 5
	filename = "output1.wav"

	p = pyaudio.PyAudio()  # Create an interface to PortAudio

	print('Recording')

	stream = p.open(format=sample_format,
					channels=channels,
					rate=fs,
					frames_per_buffer=chunk,
					input=True)

	frames = []  # Initialize array to store frames

	# Store data in chunks for 3 seconds
	for i in range(0, int(fs / chunk * seconds)):
		data = stream.read(chunk)
		frames.append(data)

	# Stop and close the stream 
	stream.stop_stream()
	stream.close()
	# Terminate the PortAudio interface
	p.terminate()

	print('Finished recording')

	# Save the recorded data as a WAV file
	wf = wave.open(filename, 'wb')
	wf.setnchannels(channels)
	wf.setsampwidth(p.get_sample_size(sample_format))
	wf.setframerate(fs)
	wf.writeframes(b''.join(frames))
	wf.close()


#function to turn audio into text
def audioToText():
	recognizer = sr.Recognizer()

	with sr.AudioFile("output1.wav") as source:
		audio_file = recognizer.record(source)
		try:
			voice = recognizer.recognize_google(audio_file)
			return voice
		except sr.UnknownValueError:
			print("Could not understand")


#____________________________
#response code			
async def getweather():
    # declare the client. format defaults to metric system (celcius, km/h, etc.)
	client = python_weather.Client(format=python_weather.IMPERIAL)

    # fetch a weather forecast from a city
	weather = await client.find("Syracuse")

    # returns the current day's forecast temperature (int)
	print("the current temperature is " , weather.current.temperature)
	printLCD("the current temperature is " + str(weather.current.temperature))

    # close the wrapper once done
	await client.close()

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("I am listening...")
        audio = r.listen(source)
    data = ""
    try:
        data = r.recognize_google(audio)
        print("You said: " + data)
    except sr.UnknownValueError:
        print("Google Speech Recognition did not understand audio")
    except sr.RequestError as e:
        print("Request Failed; {0}".format(e))
    return data



    
jokes = ["I went to buy some camo pants but couldn’t find any", 
	"I used to have a handle on life, but then it broke",
	"When life gives you melons, you might be dyslexic", 
	"It takes a lot of balls to golf the way I do",
	"Don’t you hate it when someone answers their own questions? I do",
	"Why did the football coach go to the bank? To get his quarter back",
	"Why did the orange lose the race? It ran out of juice",
	"Why are fish so smart? They live in schools!", 
	"I used to think I was indecisive. But now I’m not so sure.",
	"A termite walks into the bar and asks, ‘Is the bar tender here?’",
	"I told my girlfriend she drew her eyebrows too high. She seemed surprised."]

def digital_assistant(data):
	if "how are you" in data or "how you doing" in data:
	        print("I am well") #response
	        printLCD("I am well")
	elif "what is the weather" in data or "what's the weather" in data or "tell me the weather" in data:
	        loop = asyncio.get_event_loop()
	        loop.run_until_complete(getweather())
	elif "what time is it" in data or "what's the time" in data or "tell me the time" in data:
        	t = time.localtime()
       		current_time = time.strftime("%H:%M:%S", t)
        	print(current_time)
	        printLCD(str(current_time))
	elif "stop listening" in data:
	        print('Listening stopped by voice')
	        printLCD('Listening stopped by voice')
	elif "what is the date" in data or "what's the date" in data or "tell me the date" in data:
		today=date.today()
		d2 = today.strftime("%B %d, %Y")
		print(d2)
		printLCD(d2)
	elif "tell me a joke" in data:
		value = randint(0,10)
		print(value)
		print(jokes[value])
		printLCD(jokes[value])
	elif "what's your name" in data or "what is your name" in data:
		print("My name is Ace")
		printLCD("My name is Ace")
	else:
		print("I don't have a response to that")
		printLCD("I don't have a response to that")
	
    
    
def main(): 
	begin() #initializing the LCD screen
	
	'''recordAudio() #record a new audio
	speech = audioToText() #turning audio to text
	
	printLCD(speech) #printing a message into the LCD creen 
	print(speech) #printing into the termnial once again'''
	while True:
		if Blue.read() == 1 and bflag == 0:
			begin()
			recordAudio() #record a new audio
			speech = audioToText() #turning audio to text
	
			printLCD(speech) #printing a message into the LCD screen 
			print(speech) #printing into the termnial once again
		
			bflag = 1
		elif Blue.read() == 0:
			bflag = 0
		
		if Red.read() == 1 and rflag == 0:
			begin()
			print("Hi!, what can I do for you?")
			printLCD("Hi!, what can I do for you? ")
			listening = True
			#while listening == True:
			try:
				data = listen()
				begin()
				listening = digital_assistant(data)
			except UnboundLocalError as e:
				print("Audio was not found, try next time")
				printLCD("Audio was not found, try next time")
				#pass
			rflag = 1
		elif Red.read() == 0:
			rflag = 0

main()
