import sys
import Tkinter as tk
from tkFileDialog import askopenfilename
from trackBarVideo import run
from motionTrack import runMotionTrack
from motionTrack import readvid
from utility import saveSkeleton
import os.path
from Pose_estimator.applications.predict_pose import run_predict_pose

inputName = "noname" #name of the input file without extension
ske = []

def openfile():
   global inputName, ske
   filename = askopenfilename(parent=root)
   # obj,fps,width,height=readvid(filename)
   # ske = run_predict_pose(obj, width, height)
   if (len(filename) <> 0):
       listName = filename.split('/')
       inputFile = listName[-1].split('.')
       inputName = inputFile[0]
       if not os.path.exists(filename[0:filename.rfind('/')]+'/'+inputName+'.skeleton'):
           print filename[0:filename.rfind('/')]+inputName+'.skeleton'
           lblText.config(text='Corresponding skeleton file does not exist')
       if not os.path.exists(filename[0:filename.rfind('/')]+'/lookup.skeleton'):    
           lblText.config(text='Lookup skeleton file does not exist')
       else:
           ske = run(filename)

def callMotionTrack():
   global inputName, ske
   filename = askopenfilename(parent=root)
      
   if (len(filename) <> 0):
       listName = filename.split('/')
       inputFile = listName[-1].split('.')
       inputName = inputFile[0]
       if not os.path.exists(filename[0:filename.rfind('/')]+'/'+inputName+'.skeleton'):
           print filename[0:filename.rfind('/')]+inputName+'.skeleton'
           lblText.config(text='Corresponding skeleton file does not exist')
       if not os.path.exists(filename[0:filename.rfind('/')]+'/lookup.skeleton'):    
           lblText.config(text='Lookup skeleton file does not exist')
       else:
           runMotionTrack(filename)
                      
   
def openAbout():
    t = tk.Toplevel()
    t.wm_title("About Us")
    l = tk.Label(t, text="Founded from 2008, Human Machine Interaction (HMI) Laboratory, FIT-UET-VNU focuses its research on the fields to develop advanced interface and design methodology for the interactions between human and machines. Our primary activities include collaborative research and publication.", wraplength = 200, justify='left')
    l.pack(side="left", fill="x", expand=True, padx=0, pady=0)

def create_skeleton():
    # global ske, inputName
    # output = inputName + ".skeleton"
    # try:
    #     saveSkeleton(ske, output)
    # except Exception, e:
    #     lblText.config(text = e)
    # lblText.config(text = "Saved successfully")

    global inputName, ske
    filename = askopenfilename(parent=root)
    if len(filename) <> 0:
      rawname = filename.split('/')[-1].split('.')[0]
      obj,fps,width,height=readvid(filename)
      ske = run_predict_pose(obj, width, height)
      saveSkeleton(ske, rawname + ".skeleton")
      lblText.config(text='skeleton file is created')
    
# Main
root = tk.Tk()
root.wm_title("Skeleton Joints Matching Tool")
lblText = tk.Label(root, text = "Please select input video")
lblText.pack()
imBrowse = tk.PhotoImage(file="res/browse.png").subsample(5,5)
btnBrowse = tk.Button(root, text="Open video file", compound=tk.TOP, width=80, height=80, 
                      bg='white', image=imBrowse, command = openfile)
btnBrowse.pack(side = tk.LEFT, padx=5, pady = 5)

imKeyframe = tk.PhotoImage(file="res/key_frame1.png").subsample(5,5)
btnKeyframe = tk.Button(root, text="Keyframe", compound=tk.TOP, width=80, height=80, 
                      bg='white', image=imKeyframe, command = callMotionTrack)
btnKeyframe.pack(side = tk.LEFT, padx=5, pady = 5)

imExport = tk.PhotoImage(file="res/pose.png").subsample(5,5)
btnExport = tk.Button(root, text="Pose", compound=tk.TOP, width=80, height=80, 
                      bg='white', image=imExport, command = create_skeleton)
btnExport.pack(side = tk.LEFT, padx=5, pady = 5)

imAbout = tk.PhotoImage(file="res/info.png").subsample(5,5)
btnAbout = tk.Button(root, text="About", command = openAbout, compound=tk.TOP, width=80, height=80, 
                      bg='white', image=imAbout)
btnAbout.pack(side = tk.RIGHT, padx=5, pady = 5)
root.mainloop()