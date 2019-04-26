from gpiozero import LED
from time import sleep

pump = LED(17)

print("Turning pump ON!")
pump.on()
sleep(1)
print("Turning pump OFF!\n\n Thank you!\n")
print("Thank fren!")
