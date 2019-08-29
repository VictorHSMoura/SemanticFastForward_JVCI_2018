import os
from hyperlapseExceptions import InputError
from video import Video

class Stabilizer(object):
    def __init__(self, originalVideo, acceleratedVideo, velocity):
        self.originalVideo = originalVideo
        self.acceleratedVideo = acceleratedVideo
        self.velocity = velocity

    def correctPath(self, path):
        splittedPath = path.split(' ')
        finalPath = '"'
        for i in splittedPath:
            finalPath += (i + '&#32;')
        return finalPath[:-5] + '"'

    def generateXML(self): # pragma: no cover
        videoPath = self.correctPath(self.acceleratedVideo.path())
        videoName = self.acceleratedVideo.name()
        videoFile = self.correctPath(self.acceleratedVideo.file())
        oldVideoFile = self.correctPath(self.originalVideo.file())
        velocity = str(int(self.velocity))
        
        xmlFile = 'experiment_hyperlapse.xml'
        tags = [
            'video_path', 'video_name', 'output_path', 'original_video_filename',
            'selected_frames_filename', 'read_masterframes_filename',
            'semantic_costs_filename',  'segmentSize', 'runningParallel',
            'saveMasterFramesInDisk', 'saveVideoInDisk'
        ]

        values = [
            videoPath, videoName, videoPath, oldVideoFile,
            videoPath[:-1] + '/selected_frames_and_speedups.csv"', '',
            oldVideoFile[:-1] + '_SemanticCosts_' + velocity + 'x.csv"',
            '4', 'true', 'true', 'true']

        file = open(xmlFile, 'w')
        file.write('<?xml version=\"1.0\" ?>\n<opencv_storage>\n')
        for i in range(len(tags)):
            file.write('\t<' + tags[i] + '>\n')
            file.write('\t\t' + values[i] + '\n')
            file.write('\t</' + tags[i] + '>\n\n')
        file.write('</opencv_storage>\n')
        file.close()

        return xmlFile

    def run(self, writeFunction): #pragma: no cover
        write = writeFunction

        write('5/6 - Stabilizing\n', 'title')

        os.chdir('AcceleratedVideoStabilizer')
        xmlFile = self.generateXML()
        
        if not os.path.isdir('build') or not os.path.isfile('build/VideoStabilization'):
            write('Please compile the Stabilizer and run it again.\n', 'normal')
        else:
            os.chdir('build')
            os.system('./VideoStabilization ' + "../" + xmlFile)
        write('6/6 - Finished\n', 'title')



