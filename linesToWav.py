import wave, struct

frameRate = 44100
fileName = "test"
loops = 1 #how many loops it runs for
scale = 1

class Line:
    def __init__(self, x1,y1,x2,y2, drawFrames=100):
        self.x1 = x1*scale
        self.y1 = y1*scale
        self.x2 = x2*scale
        self.y2 = y2*scale
        self.drawFrames = drawFrames #how many frames it takes to draw line, ie how long it takes to move between point 1 and 2 
        self.xDif = (self.x2-self.x1)/self.drawFrames
        self.yDif = (self.y2-self.y1)/self.drawFrames

lineArray = [Line(0,-1,1,0), Line(1,0,0,1), Line(0,1,-1,0), Line(-1,0,0,-1)] #each object represents a line betweeb two coordinates x1,y1,x2,y2

leftChannel = []
rightChannel = []
for _ in range(loops):
    for line in (lineArray):
        for i in range(line.drawFrames):
            rightChannel.append(line.x1+(line.xDif)*i)
            leftChannel.append(line.y1+(line.yDif)*i)

with wave.open(fileName+".wav", "w") as f:
    f.setnchannels(2)
    f.setsampwidth(2)
    f.setframerate(frameRate)
    for samples in zip(leftChannel, rightChannel):
        for sample in samples:
            sample = int(sample * (2 ** 15 - 1))
            f.writeframes(struct.pack("<h", sample))