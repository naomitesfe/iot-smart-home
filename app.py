import RPi.GPIO as GPIO
import Adafruit_DHT  # new library for the DHT11 sensor
from flask import Flask, render_template, request

app = Flask(__name__)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#define sensors GPIOs
button = 20
senPIR = 16
dht11_sensor = 4  # new DHT11 sensor connected to GPIO pin 4

#define actuators GPIOs
ledRed = 13
ledYlw = 23
ledGrn = 24

#initialize GPIO status variables
buttonSts = 0
senPIRSts = 0
ledRedSts = 0
ledYlwSts = 0
ledGrnSts = 0

# Define button, PIR sensor and DHT11 sensor pins as an input
GPIO.setup(button, GPIO.IN)   
GPIO.setup(senPIR, GPIO.IN)

# Define led pins as output
GPIO.setup(ledRed, GPIO.OUT)   
GPIO.setup(ledYlw, GPIO.OUT) 
GPIO.setup(ledGrn, GPIO.OUT) 

# turn leds OFF 
GPIO.output(ledRed, GPIO.LOW)
GPIO.output(ledYlw, GPIO.LOW)
GPIO.output(ledGrn, GPIO.LOW)

@app.route("/")
def index():
  # Read Sensors Status
  buttonSts = GPIO.input(button)
  senPIRSts = GPIO.input(senPIR)
  humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, dht11_sensor) # new line to read from DHT11 sensor

  ledRedSts = GPIO.input(ledRed)
  ledYlwSts = GPIO.input(ledYlw)
  ledGrnSts = GPIO.input(ledGrn)

  templateData = {
          'button'  : buttonSts,
          'senPIR'  : senPIRSts,
          'temperature' : temperature, # new line to send temperature data to the template
          'humidity' : humidity, # new line to send humidity data to the template
          'ledRed'  : ledRedSts,
          'ledYlw'  : ledYlwSts,
          'ledGrn'  : ledGrnSts,
        }
  return render_template('index.html', **templateData)

@app.route("/<deviceName>/<action>")
def action(deviceName, action):
  if deviceName == 'ledRed':
    actuator = ledRed
  if deviceName == 'ledYlw':
    actuator = ledYlw
  if deviceName == 'ledGrn':
    actuator = ledGrn

  if action == "on":
    GPIO.output(actuator, GPIO.HIGH)
  if action == "off":
    GPIO.output(actuator, GPIO.LOW)

  buttonSts = GPIO.input(button)
  senPIRSts = GPIO.input(senPIR)
  humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, dht11_sensor) # new line to read from DHT11 sensor

  ledRedSts = GPIO.input(ledRed)
  ledYlwSts = GPIO.input(ledYlw)
  ledGrnSts = GPIO.input(ledGrn)

  templateData = {
    'button'  : buttonSts,
          'senPIR'  : senPIRSts,
          'temperature' : temperature, # new line to send temperature data to the template
          'humidity' : humidity, # new line to send humidity data to the template
          'ledRed'  : ledRedSts,
          'ledYlw'  : ledYlwSts,
          'ledGrn'  : ledGrnSts,
  }
  return render_template('index.html', **templateData)

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=80, debug=True)
