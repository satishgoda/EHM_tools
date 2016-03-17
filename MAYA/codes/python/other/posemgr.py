import maya.cmds as cmds
import maya.mel as mel
import os, cPickle, sys, time

kPoseFileExtension = 'pse'

def showUI():
    """A function to instantiate the pose manager window"""
    return AR_PoseManagerWindow.showUI()

class AR_PoseManagerWindow(object):
    """A class for a basic pose manager window"""
    @classmethod
    def showUI(cls):
        """A function to instantiate the pose manager window"""
        win = cls()
        win.create()
        return win
    def __init__(self):
        """Initialize data attributes"""
        ## a unique window handle
        self.window = 'ar_poseManagerWindow'
        ## window title
        self.title = 'Pose Manager'
        ## window size
        self.size = (300, 174)
        if mel.eval('getApplicationVersionAsFloat()') > 2010.0:
            self.size = (300, 150)
        ## a temporary file in a writable location for storing a pose
        self.tempFile = os.path.join(
            os.path.expanduser('~'),
            'temp_pose.%s'%kPoseFileExtension
        )
        ## current clipboard status message
        self.clipboardStat = 'No pose currently copied.'
        if (os.path.exists(self.tempFile)):
            self.clipboardStat = 'Old pose currently copied to clipboard.'
        ## file filter to display in file browsers
        self.fileFilter = 'Pose (*.%s)'%kPoseFileExtension
    def create(self):
        """Draw the window"""
        # delete the window if its handle exists
        if(cmds.window(self.window, exists=True)):
            cmds.deleteUI(self.window, window=True)
        # initialize the window
        self.window = cmds.window(self.window, title=self.title, wh=self.size, s=False)
        # main form layout
        self.mainForm = cmds.formLayout()
        # frame for copy/paste
        self.copyPasteFrame = cmds.frameLayout(l='Copy and Paste Poses')
        # form layout inside of frame
        self.copyPasteForm = cmds.formLayout()
        # create buttons in a 2-column grid
        self.copyPasteGrid = cmds.gridLayout(cw=self.size[0]/2-2, nc=2)
        self.copyBtn = cmds.button(l='Copy Pose', c=self.copyBtnCmd)
        self.pasteBtn = cmds.button(l='Paste Pose', c=self.pasteBtnCmd)
        # scroll view with label for clipboard status
        cmds.setParent(self.copyPasteForm)
        self.clipboardLayout = cmds.scrollLayout(h=42, w=self.size[0]-4)
        self.clipboardLbl = cmds.text(l=self.clipboardStat)
        # attach controls in the copyPaste form
        ac = []; af = []
        ac.append([self.clipboardLayout,'top',0,self.copyPasteGrid])
        af.append([self.copyPasteGrid,'top',0])
        af.append([self.clipboardLayout,'bottom',0])
        cmds.formLayout(
            self.copyPasteForm, e=True,
            attachControl=ac, attachForm=af
        )
        # frame for save/load
        cmds.setParent(self.mainForm)
        self.loadSaveFrame = cmds.frameLayout(l='Save and Load Poses')
        # create buttons in a 2-column grid
        self.loadSaveBtnLayout = cmds.gridLayout(cw=self.size[0]/2-2, nc=2)
        self.saveBtn = cmds.button(l='Save Pose', c=self.saveBtnCmd)
        self.loadBtn = cmds.button(l='Load Pose', c=self.loadBtnCmd)
        # attach frames to main form
        ac = []; af = []
        ac.append([self.loadSaveFrame,'top',0,self.copyPasteFrame])
        af.append([self.copyPasteFrame,'top',0])
        af.append([self.copyPasteFrame,'left',0])
        af.append([self.copyPasteFrame,'right',0])
        af.append([self.loadSaveFrame,'bottom',0])
        af.append([self.loadSaveFrame,'left',0])
        af.append([self.loadSaveFrame,'right',0])
        cmds.formLayout(
            self.mainForm, e=True,
            attachControl=ac, attachForm=af
        )
        # show the window
        cmds.showWindow(self.window)
        # force window size
        cmds.window(self.window, e=True, wh=self.size)
    def getSelection(self):
        rootNodes = cmds.ls(sl=True, type='transform')
        if rootNodes is None or len(rootNodes) < 1:
            cmds.confirmDialog(t='Error', b=['OK'],
                m='Please select one or more transform nodes.')
            return None
        else: return rootNodes
    def copyBtnCmd(self, *args):
        """Called when the Copy Pose button is pressed"""
        rootNodes = self.getSelection()
        if rootNodes is None: return
        cmds.text(
            self.clipboardLbl, e=True,
            l='Pose copied at %s for %s.'%(
                time.strftime('%I:%M'),
                ''.join('%s, '%t for t in rootNodes)[:-3]
            )
        )
        exportPose(self.tempFile, rootNodes)
    def pasteBtnCmd(self, *args):
        """Called when the Paste Pose button is pressed"""
        if not os.path.exists(self.tempFile): return
        importPose(self.tempFile)
    def saveBtnCmd(self, *args):
        """Called when the Save Pose button is pressed"""
        rootNodes = self.getSelection()
        if rootNodes is None: return
        filePath = ''
        # Maya 2011 and newer use fileDialog2
        try:
            filePath = cmds.fileDialog2(
                ff=self.fileFilter, fileMode=0
            )
        # BUG: Maya 2008 and older may, on some versions of OS X, return the
        # path with no separator between the directory and file names:
        # e.g., /users/adam/Desktopuntitled.pse
        except:
            filePath = cmds.fileDialog(
                dm='*.%s'%kPoseFileExtension, mode=1
            )
        # early out of the dialog was canceled
        if filePath is None or len(filePath) < 1: return
        if isinstance(filePath, list): filePath = filePath[0]
        exportPose(filePath, cmds.ls(sl=True, type='transform'))
    def loadBtnCmd(self, *args):
        """Called when the Load Pose button is pressed"""
        filePath = ''
        # Maya 2011 and newer use fileDialog2
        try:
            filePath = cmds.fileDialog2(
                ff=self.fileFilter, fileMode=1
            )
        except:
            filePath = cmds.fileDialog(
                dm='*.%s'%kPoseFileExtension, mode=0
            )
        # early out of the dialog was canceled
        if filePath is None or len(filePath) < 1: return
        if isinstance(filePath, list): filePath = filePath[0]
        importPose(filePath)

def exportPose(filePath, rootNodes):
    """Save a pose file at filePath for rootNodes and their children"""
    # try to open the file
    try: f = open(filePath, 'w')
    except:
        cmds.confirmDialog(
            t='Error', b=['OK'],
            m='Unable to write file: %s'%filePath
        )
        raise
    # built a list of hierarchy data
    data = saveHiearchy(rootNodes, [])
    # save the serialized data
    cPickle.dump(data, f)
    # close the file
    f.close()

def saveHiearchy(rootNodes, data):
    """Append attribute values for all keyable attributes to data array"""
    # iterate through supplied nodes
    for node in rootNodes:
        # skip non-transform nodes
        nodeType = cmds.nodeType(node)
        if not (nodeType=='transform' or 
            nodeType=='joint'): continue
        # get animated attributes
        keyableAttrs = cmds.listAttr(node, keyable=True)
        if keyableAttrs is not None:
            for attr in keyableAttrs:
                data.append(['%s.%s'%(node,attr), 
                    cmds.getAttr('%s.%s'%(node,attr))])
        # if there are children, repeat the same process and append their data
        children = cmds.listRelatives(node, children=True)
        if children is not None: saveHiearchy(children, data)
    return data

def importPose(filePath):
    """Import the pose data stored in filePath"""
    # try to open the file
    try: f = open(filePath, 'r')
    except:
        cmds.confirmDialog(
            t='Error', b=['OK'],
            m='Unable to open file: %s'%filePath
        )
        raise
    # uncPickle the data
    pose = cPickle.load(f)
    # close the file
    f.close()
    # set the attributes to the stored pose
    errAttrs = []
    for attrValue in pose:
        try: cmds.setAttr(attrValue[0], attrValue[1])
        except:
            try: errAttrs.append(attrValue[0])
            except: errAttrs.append(attrValue)
    # display error message if needed
    if len(errAttrs) > 0:
        importErrorWindow(errAttrs)
        sys.stderr.write('Not all attributes could be loaded.')

def importErrorWindow(errAttrs):
    """An error window to display if there are unknown attributes when importing a pose"""
    win='ar_errorWindow'
    # a function to dismiss the window
    def dismiss(*args):
        cmds.deleteUI(win, window=True)
    # destroy the window if it exists
    if cmds.window(win, exists=True):
        dismiss()
    # create the window
    size = (300, 200)
    cmds.window(
        win, wh=size, s=False,
        t='Unknown Attributes'
    )
    mainForm = cmds.formLayout()
    # info label
    infoLbl = cmds.text(l='The following attributes could not be found.\nThey are being ignored.', al='left')
    # display a list of attributes that could not be loaded
    scroller = cmds.scrollLayout(w=size[0])
    errStr = ''.join('\t- %s\n'%a for a in errAttrs).rstrip()
    cmds.text(l=errStr, al='left')
    # dismiss button
    btn = cmds.button(l='OK', c=dismiss, p=mainForm, h=26)
    # attach controls
    ac = []; af=[];
    ac.append([scroller,'top',5,infoLbl])
    ac.append([scroller,'bottom',5,btn])
    af.append([infoLbl,'top',5])
    af.append([infoLbl,'left',5])
    af.append([infoLbl,'right',5])
    af.append([scroller,'left',0])
    af.append([scroller,'right',0])
    af.append([btn,'left',5])
    af.append([btn,'right',5])
    af.append([btn,'bottom',5])
    cmds.formLayout(
        mainForm, e=True,
        attachControl=ac, attachForm=af
    )
    # show the window
    cmds.window(win, e=True, wh=size)
    cmds.showWindow(win)