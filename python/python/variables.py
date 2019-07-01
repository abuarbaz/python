import os

cars = 100

space_in_a_car = 4

drivers = 30
passengers = 90

cars_not_driven = cars -drivers

cars_driven = drivers

carpool_capacity = cars_driven * space_in_a_car

average_passengers_per_car = passengers / cars_driven

my_name = 'Zed A. Shaw'

my_age = 35 # not a lie

my_height = 74 # inches

my_weight = 180 # lbs

my_eyes = 'Blue'

my_teeth = 'White'

my_hair = 'Brown'





print "There are", cars, "cars available."

print "There are only", drivers, "drivers available."

print "There will be", cars_not_driven, "empty cars today."

print "We can transport", carpool_capacity, "people today."

print "We have", passengers, "to carpool today."

print "We need to put about", average_passengers_per_car, "in each car."



print "Let's talk about %s." % my_name

print "He's %d inches tall." % my_height

print "He's %d pounds heavy." % my_weight

print "Actually that's not too heavy."

print "He's got %s eyes and %s hair." % (my_eyes, my_hair)

print "His teeth are usually %s depending on the coffee." % my_teeth

print "If I add %d, %d, and %d I get %d." % (my_age, my_height, my_weight, my_age + my_height + my_weight)











