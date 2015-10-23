import time
import RPi.GPIO as GPIO

# RPi.GPIO Layout verwenden (wie Pin-Nummern)
GPIO.setmode(GPIO.BOARD)

# Pin 18 (GPIO 24) auf Input setzen
GPIO.setup(18, GPIO.IN)

# Pin 11 (GPIO 17) auf Output setzen
GPIO.setup(11, GPIO.OUT)

# Dauersschleife
while 1:
  # LED immer ausmachen
  GPIO.output(11, GPIO.LOW)

  # GPIO lesen
  if GPIO.input(18) == GPIO.HIGH:
    # LED an
    GPIO.output(11, GPIO.HIGH)

    # Warte 100 ms
    time.sleep(0.1)

    # LED aus
    GPIO.output(11, GPIO.LOW)

    # Warte 100 ms
    time.sleep(0.1)
