import wave, struct, readObj, rotateVertex

objFileName = "house"
saveFileName = "house"
frameRate = 44100
initRotation = [0,0,-1.5708]
rotationArray = [0.0174533,0,0] #in radians
pausePerRotate = 1 #in frames
rotations = 360
loops = 1 #how many loops it runs for
scale = 0.75

class Line:
    def __init__(self, x1,y1,x2,y2, drawFrames=5):
        self.x1 = x1*scale
        self.y1 = y1*scale
        self.x2 = x2*scale
        self.y2 = y2*scale
        self.drawFrames = drawFrames #how many frames it takes to draw line, ie how long it takes to move between point 1 and 2 
        self.xDif = (self.x2-self.x1)/self.drawFrames
        self.yDif = (self.y2-self.y1)/self.drawFrames

vertices, edges = readObj.readObj(objFileName)
vertices = [rotateVertex.rotateVertex(vertex, initRotation) for vertex in vertices]
lineArray = []


leftChannel = []
rightChannel = []
for m in range(rotations):
    lineArray = []
    for edge in edges:
        lineArray.append(Line(vertices[edge[0]][0],vertices[edge[0]][1], vertices[edge[1]][0], vertices[edge[1]][1],50))
    for _ in range(pausePerRotate):
        for line in (lineArray):
            for i in range(line.drawFrames):
                rightChannel.append(line.x1+(line.xDif*i))
                leftChannel.append(line.y1+(line.yDif*i))
    
    vertices = [rotateVertex.rotateVertex(vertex, rotationArray) for vertex in vertices]
    print("rotation: "+str(m))

print(max(rightChannel))
with wave.open(saveFileName+".wav", "w") as f:
    f.setnchannels(2)
    f.setsampwidth(2)
    f.setframerate(frameRate)
    for samples in zip(leftChannel, rightChannel):
        for sample in samples:
            sample = int(sample * (2 ** 15 - 1))
            f.writeframes(struct.pack("<h", sample))
