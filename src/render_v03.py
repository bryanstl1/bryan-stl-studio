# BRYAN.STL STUDIO — v0.3 renderer
# Requires: Python 3, numpy, opencv-python, FFmpeg.
# Procedural XYZ projection; not Blender/PBR.
import os, math, subprocess, wave
import numpy as np, cv2
ROOT=os.path.dirname(os.path.dirname(__file__))
OUT=os.path.join(ROOT,"output")
os.makedirs(OUT,exist_ok=True)
W,H,FPS,N=540,960,30,240
SR=48000
T=np.arange(SR*8)/SR
kick=np.sin(2*np.pi*(53*T-17*np.mod(T,.5)**2))*np.exp(-24*np.mod(T,.5))
hat=np.random.default_rng(23).normal(size=len(T))*np.exp(-36*np.mod(T,.25))
lead=np.sin(2*np.pi*(220*T+9*np.sin(2*np.pi*.25*T)))+.5*np.sin(2*np.pi*330*T)
audio=(.36*kick+.04*hat+.11*lead)*np.clip((4-T)*80,0,1)
wav=os.path.join(OUT,"cue.wav")
with wave.open(wav,"wb") as f:
 f.setnchannels(1);f.setsampwidth(2);f.setframerate(SR)
 f.writeframes((np.clip(audio,-1,1)*32767).astype("<i2").tobytes())
def frame(i):
 t=i/FPS; active=t<4
 im=np.zeros((H,W,3),np.uint8)
 for y in range(H):
  q=y/H;im[y,:]=(int(21-13*q),int(12-8*q),int(24-18*q)) if active else (int(11-5*q),)*3
 cx=.85*math.sin(t*.48);camz=-10+1.15*t
 def proj(v):
  x,y,z=v;s=730/max(1,z-camz)
  return (int(W/2+(x-cx)*s),int(H*.62-y*s))
 def line(a,b,c,w=2):cv2.line(im,proj(a),proj(b),c,w,cv2.LINE_AA)
 def poly(v,c):cv2.fillConvexPoly(im,np.array([proj(p) for p in v],np.int32),c,cv2.LINE_AA)
 poly([(-7,-2,17),(7,-2,17),(7,-.7,17),(-7,-.7,17)],(70,53,64) if active else (24,24,24))
 poly([(-6,-.6,20),(6,-.6,20),(6,7,20),(-6,7,20)],(39,18,42) if active else (20,20,20))
 for x in (-6,6):
  for z in (17,22):line((x,-2,z),(x,8,z),(112,96,117) if active else (36,36,36),4)
 for j in range(5):
  z=19+j*.55;w=4.8-j*.48;h=5.5-j*.43
  c=(145,40+30*j,175) if active else (27,27,27)
  for a,b in [((-w,-.4,z),(-w,h,z)),((-w,h,z),(w,h,z)),((w,h,z),(w,-.4,z))]:line(a,b,c,3)
 for x in np.arange(-14,15,2):line((x,-2,0),(x,-2,29),(40,28,53) if active else (17,17,17))
 for z in range(1,29,3):line((-14,-2,z),(14,-2,z),(35,25,42) if active else (17,17,17))
 if active:
  glow=np.zeros_like(im)
  for k in range(12):
   a=k*.55+t*1.7;origin=(-5 if k%2 else 5,6,18)
   end=(13*math.sin(a),-2,4+10*abs(math.cos(a*.65)))
   cv2.line(glow,proj(origin),proj(end),(155,75,110),12,cv2.LINE_AA)
   line(origin,end,(240,120,140),2)
  im=cv2.addWeighted(im,1,cv2.GaussianBlur(glow,(0,0),15),.38,0)
  for k in range(120):
   z=2+k*.11;a=k*.19-t*7;r=1.8+.4*math.sin(k*.1-t*5)
   cv2.circle(im,proj((r*math.cos(a),2.2+r*math.sin(a),z)),2,(240,185,115),-1)
 for k in range(170):
  x=((k*7.131)%20)-10;z=2+((k*3.71)%13)
  bob=.17*math.sin(t*7+k) if active else 0
  cv2.circle(im,proj((x,-1.55+bob,z)),max(2,int(65/(z-camz))),(9,8,14),-1)
 if not active:cv2.putText(im,"SILENCIO",(77,198),cv2.FONT_HERSHEY_SIMPLEX,1.45,(210,210,210),3)
 else:cv2.putText(im,"ANTES DEL DROP",(48,198),cv2.FONT_HERSHEY_SIMPLEX,.95,(237,225,229),2)
 cv2.putText(im,"BRYAN.STL",(361,924),cv2.FONT_HERSHEY_SIMPLEX,.43,(122,122,122),1)
 return im
out=os.path.join(OUT,"prototype-v03.mp4")
cmd=["ffmpeg","-y","-loglevel","error","-f","rawvideo","-pix_fmt","bgr24","-s",f"{W}x{H}","-r",str(FPS),"-i","pipe:0","-i",wav,"-vf","scale=1080:1920:flags=lanczos","-c:v","libx264","-preset","veryfast","-crf","23","-pix_fmt","yuv420p","-c:a","aac","-b:a","160k","-t","8","-movflags","+faststart",out]
p=subprocess.Popen(cmd,stdin=subprocess.PIPE)
shots=[]
for i in range(N):
 f=frame(i)
 if i in (0,30,60,90,119,120,150,210):shots.append(cv2.resize(f,(270,480)))
 p.stdin.write(f.tobytes())
p.stdin.close()
if p.wait():raise RuntimeError("ffmpeg failed")
cv2.imwrite(os.path.join(OUT,"contact-sheet-v03.jpg"),np.vstack([np.hstack(shots[:4]),np.hstack(shots[4:])]))
print(out)
