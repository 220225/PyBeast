from BeastPython.beastPython import *
import sys

class BeastPythonException(Exception):
    def __init__(self, value):
        self.parameter = value
    def __str__(self):
        return repr(sel.parameter)
        
def apiCall(_status):
    """docstring for checkStatus"""
    if _status != ILB_ST_SUCCESS:
        raise BeastPythonException(_status)

def findCachedMesh(_bmh, _meshName, _target):
    """docstring for findCachedMesh"""

    findRes = ILBFindMesh(_bmh, _meshName, _target)
    if findRes == ILB_ST_SUCCESS:
        print "Found the mesh: " + _meshName + ", in the cache"
        return True
    elif findRes == ILB_ST_UNKNOWN_OBJECT:
        print "Didn't find the mesh: " + _meshName + ", creating it!"
        return False

    raise Exception, str(findRes)

def findCachedTexture(_bmh, _texName, _target):
    """docstring for findCachedTexture"""

    findRes = ILBFindTexture(_bmh, _texName, _target)
    if findRes == ILB_ST_SUCCESS:
        print "Found the texture: " + _texName + ", in the cache"
        return True
    elif findRes == ILB_ST_UNKNOWN_OBJECT:
        print "Didn't find the texture: " + _texName + ", creating it!"
        return False

    raise Exception, str(findRes)


def renderJob(_job, _returnWhenComplete = False, _destroyJob = True, _distribution = ILB_RD_AUTODETECT):
    returnWhenComplete = ILB_SR_CLOSE_WHEN_DONE if _returnWhenComplete == True else ILB_SR_KEEP_OPEN
    apiCall( ILBStartJob(_job, returnWhenComplete, _distribution))

    isRunning = ILBBool(True)
    firstJob = ILBBool(True)
    completed = ILBBool(False)
    oldProgress = 0

    while isRunning.value:
        apiCall( ILBWaitJobDone(_job, sys.maxint) )

        if not completed.value:
            apiCall( ILBIsJobCompleted(_job, completed) )
            if completed.value == True:
                print "Job is complete. It might still be running if the user has selected ILB_SR_KEEP_OPEN"

        apiCall( ILBIsJobRunning(_job, isRunning) )
        if isRunning.value == True:
            newProgress = ILBBool(True)
            newActivity = ILBBool(True)
            apiCall( ILBJobHasNewProgress(_job, newActivity, newProgress))
            if newProgress.value == True:
                taskName = createNewStringHandle()
                progress = ILBInt32(0)
                apiCall( ILBGetJobProgress(_job, taskName, progress) )
                jobNameString = convertStringHandle(taskName)

                if newActivity.value == True:
                    if not firstJob and oldProgress < 100:
                        for i in range((100-oldProgress)/5):
                            sys.stdout.write("-")
                        print "]"
                    else:
                        firstJob = False
                    print jobNameString
                    print "[",

                for i in range((progress.value-oldProgress)/5):
                    sys.stdout.write("-")
                if progress.value == 100 and oldProgress < 100:
                    print "]"

                oldProgress = progress.value

    status = createNewJobStatus()
    apiCall( ILBGetJobResult(_job, status) )

    if status.value == ILB_JS_SUCCESS:
        print "Job Done"
    else:
        if status.value == ILB_JS_CANCELLED:
            print "User canceled rendering"
        elif status.value == ILB_JS_INVALID_LICENSE:
            print "Problem with the Beast License!"
        elif status.value == ILB_JS_CMDLINE_ERROR:
            print "Error parsing Beast command line!"
        elif status.value == ILB_JS_CONFIG_ERROR:
            print "Error parsing Beast config files!"
        elif status.value == ILB_JS_CRASH:
            print "Error: Beast crashed!"
        elif status.value == ILB_JS_OTHER_ERROR:
            print "Other error unning Beast."

        return False

    if _destroyJob == True:
        apiCall( ILBDestroyJob(_job) )

    return True
                
