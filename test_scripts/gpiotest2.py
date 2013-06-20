import RPi.GPIO as GPIO, time
GPIO.setmode(GPIO.BOARD)
 
power_pin = 11
led_pin = 7
#motor_pin = 11

GPIO.setup(power_pin, GPIO.OUT)
GPIO.output(power_pin, True)

GPIO.setup(led_pin, GPIO.OUT)
GPIO.output(led_pin, True)

#GPIO.setup(motor_pin, GPIO.OUT)
#GPIO.output(motor_pin, True)

time.sleep(60)
