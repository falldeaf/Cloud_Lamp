import RPi.GPIO as io, time
#io.setmode(io.BCM) 
 
#power_pin = 18
#led_pin = 21
#motor_pin = 17

power_pin = 12
led_pin = 13
motor_pin = 11

io.setup(power_pin, io.OUT)
io.output(power_pin, True)

io.setup(led_pin, io.OUT)
io.output(led_pin, True)

io.setup(motor_pin, io.OUT)
io.output(motor_pin, True)

time.sleep(60)
