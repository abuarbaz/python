1 print "You enter a dark room with two doors. Do you go through door #1 or door #2?"
2
3 door = raw_input("> ")
4
5 if door == "1":
6 print "There's a giant bear here eating a cheese cake. What do you do?"
7 print "1. Take the cake."
8 print "2. Scream at the bear."
9
10 bear = raw_input("> ")
11
12 if bear == "1":
13 print "The bear eats your face off. Good job!"
14 elif bear == "2":
15 print "The bear eats your legs off. Good job!"
16 else:
17 print "Well, doing %s is probably better. Bear runs away." % bear
18
19 elif door == "2":
20 print "You stare into the endless abyss at Cthuhlu's retina."
21 print "1. Blueberries."
22 print "2. Yellow jacket clothespins."
23 print "3. Understanding revolvers yelling melodies."
24
25 insanity = raw_input("> ")
26
91
Learn Python The Hard Way, Release 2.0
27 if insanity == "1" or insanity == "2":
28 print "Your body survives powered by a mind of jello. Good job!"
29 else:
30 print "The insanity rots your eyes into a pool of muck. Good job!"
31
32 else:
33 print "You stumble around and fall on a knife and die. Good job!"

