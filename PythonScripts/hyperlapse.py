import matlab.engine
import os
from subprocess import Popen, PIPE, STDOUT
from hyperlapseExceptions import InputError
from video import Video
from stabilizer import Stabilizer

class SemanticHyperlapse(object):
    def __init__(self, video, extractor, velocity, alpha, beta, gama, eta):
        self.video = video
        self.path = os.getcwd()
        self.extractor = extractor
        self.velocity = velocity
        self.maxVel = 10 * velocity
        self.alpha = alpha
        self.beta = beta
        self.gama = gama
        self.eta = eta

        self.checkParameters()

    def checkExtractor(self):
        if self.isEmpty(self.extractor):
            raise InputError('Please select an extractor')

    def checkAndSetVelocity(self):
        if self.isEmpty(self.velocity):
            raise InputError('Please insert speedup')
        try:
            self.isVelocityValidNumber()
            self.velocity = float(int(self.velocity))
        except ValueError:
            raise InputError('Invalid speedup value')
    
    def checkVideoInput(self):
        self.video.checkInput('Input')

    def checkAndSetWeights(self):
        weights = [self.alpha, self.beta, self.gama, self.eta]
        for i in range(len(weights)):
            try:
                weights[i] = self.convertWeights(weights[i])
            except ValueError:
                raise InputError('Please fill correctly all weights inputs')

    def isVelocityValidNumber(self):
        velocity = int(self.velocity) #raises ValueError if it isn't a number
        if velocity <= 1:
            raise InputError('Error: speedup <= 1')

    def isEmpty(self, inputText):
        if inputText == '':
            return True
        return False

    def convertWeights(self, weights):
        for i in range(len(weights)):
            weights[i] = int(weights[i])	#if it isn't a number, it'll raises a ValueError
        return weights

    def opticalFlowExists(self):
        videoFile = self.video.file()
        outputFile = videoFile[:-4] + '.csv'

        return os.path.isfile(outputFile)

    def opticalFlowCommand(self):
        videoFile = self.correctPath(self.video.file())
        command = './optflow'
        videoParam = ' -v ' + videoFile
        configParam = ' -c default-config.xml'
        outputParam = ' -o ' + videoFile[:-4] + '.csv'

        fullCommand = command + videoParam + configParam + outputParam
        
        return fullCommand

    def runOpticalFlow(self): # pragma: no cover
        os.chdir('Vid2OpticalFlowCSV')

        if not self.opticalFlowExists():
            os.system(self.opticalFlowCommand())
        else:
            print 'OpticalFlow already extracted.'
        
        os.chdir(self.path)

    def runMatlabSemanticInfo(self, eng): # pragma: no cover
        videoFile = self.video.file()
        extractionFile = videoFile[:-4] + '_face_extracted.mat'
        extractor = self.extractor

        eng.ExtractAndSave(videoFile, extractor, nargout=0)
        (aux, nonSemanticFrames, semanticFrames) = eng.GetSemanticRanges(extractionFile, nargout=3)

        return (float(nonSemanticFrames), float(semanticFrames))

    def getSemanticInfo(self, eng): # pragma: no cover
        eng.cd('SemanticScripts')
        eng.addpath(self.video.path())
        eng.addpath(os.getcwd())
        
        nonSemanticFrames, semanticFrames = self.runMatlabSemanticInfo(eng)
        
        eng.cd(self.path)
        return (nonSemanticFrames, semanticFrames)

    def speedUp(self, eng, nonSemanticFrames, semanticFrames): # pragma: no cover
        eng.addpath(os.getcwd())
        eng.addpath('Util')
    
        alpha = matlab.double([self.alpha])
        beta = matlab.double([self.beta])
        gama = matlab.double([self.gama])
        eta = matlab.double([self.eta])
    
        (ss, sns) = eng.FindingBestSpeedups(nonSemanticFrames, semanticFrames,
                                            self.velocity, True, nargout=2)
            
        videoName = eng.SpeedupVideo(
            self.video.path(), self.video.name(), self.extractor, ss, sns,
            alpha, beta, gama, eta, nargout=1
        )
        return videoName

    def checkParameters(self):	
        self.checkVideoInput()
        self.checkExtractor()
        self.checkAndSetVelocity()
        self.checkAndSetWeights()

    def speedUpPart(self, writeFunction): # pragma: no cover
        write = writeFunction
        
        write('1/6 - Running Optical Flow\n', 'title')
        self.runOpticalFlow()
    
        write('2/6 - Starting Matlab\n', 'title')
        eng = matlab.engine.start_matlab('-nodisplay')
    
        write('3/6 - Getting Semantic Info\n', 'title')
        (nonSemanticFrames, semanticFrames) = self.getSemanticInfo(eng)

        write('4/6 - Speeding-Up Video\n', 'title')
        videoName = self.speedUp(eng, nonSemanticFrames, semanticFrames)
        eng.quit()
    
        return Video(videoName + '.avi')

    def stabilizePart(self, acceleratedVideo, writeFunction):
        stabilizer = Stabilizer(self.video, acceleratedVideo, self.velocity)
        stabilizer.run(writeFunction)
        os.chdir(self.path)

    def run(self, writeFunction): # pragma: no cover
        acceleratedVideo = self.speedUpPart(writeFunction)
        self.stabilizePart(acceleratedVideo, writeFunction)

    def correctPath(self, path):
        splittedPath = path.split(' ')
        finalPath = ''
        for i in splittedPath:
            finalPath += (i + '\ ')
        return finalPath[:-2]
