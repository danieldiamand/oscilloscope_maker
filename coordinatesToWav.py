import wave
import math
import struct

sampleRate = 44100
loopValue = 441 #will draw shape sampleRate/loopValue number of times
coordinateArray = [[0,-0.25],[0.25,0],[0,0.25],[-0.25,0]] #will draw lines between points in order returning to first point

leftChannel = [
]
rightChannel = [
    ]

loopRate = int(sampleRate/loopValue)
actionRate = int(loopRate/len(coordinateArray))
for _ in range(loopRate):
    for i in range(len(coordinateArray)):
        startCoord = coordinateArray[i]
        if (i == len(coordinateArray)-1):
            endCoord = coordinateArray[0]
        else:
            endCoord = coordinateArray[i+1]
        xMovement = (endCoord[0]-startCoord[0])/actionRate
        yMovement = (endCoord[1]-startCoord[1])/actionRate
        for j in range(actionRate):
            rightChannel.append(startCoord[0]+xMovement*j)
            leftChannel.append(startCoord[1]+yMovement*j)

with wave.open("diamond.wav", "w") as f:
    f.setnchannels(2)
    f.setsampwidth(2)
    f.setframerate(sampleRate)
    for samples in zip(leftChannel, rightChannel):
        for sample in samples:
            sample = int(sample * (2 ** 15 - 1))
            f.writeframes(struct.pack("<h", sample))