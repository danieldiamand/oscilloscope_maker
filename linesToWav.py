import wave, math, struct

sampleRate = 44100
loopValue = 441 #will draw shape (sampleRate/loopValue) number of times
scale = 0.25

class Line:
    def __init__(self, x1,y1,x2,y2):
        self.x1 = x1*scale
        self.y1 = y1*scale
        self.x2 = x2*scale
        self.y2 = y2*scale
        self.xDif = (self.x2-self.x1)
        self.yDif = (self.y2-self.y1)

lineArray = [Line(0,-1,1,0), Line(1,0,0,1), Line(0,1,-1,0), Line(-1,0,0,-1)] #each object represents a line made of x1,y1,x2,y2 scaled by scale
loopRate = int(sampleRate/loopValue)
actionRate = int(loopRate/len(lineArray))

leftChannel = [
]
rightChannel = [
    ]

for _ in range(loopRate):
    for line in (lineArray):
        for i in range(actionRate):
            rightChannel.append(line.x1+(line.xDif/actionRate)*i)
            leftChannel.append(line.y1+(line.yDif/actionRate)*i)

with wave.open("test.wav", "w") as f:
    f.setnchannels(2)
    f.setsampwidth(2)
    f.setframerate(sampleRate)
    for samples in zip(leftChannel, rightChannel):
        for sample in samples:
            sample = int(sample * (2 ** 15 - 1))
            f.writeframes(struct.pack("<h", sample))