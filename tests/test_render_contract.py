import json, subprocess, sys, array, math
from pathlib import Path
p=Path(sys.argv[1] if len(sys.argv)>1 else 'output/prototype-v03.mp4')
assert p.is_file(), f'Missing video: {p}'
info=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(p)]))
v=next(s for s in info['streams'] if s['codec_type']=='video')
a=next(s for s in info['streams'] if s['codec_type']=='audio')
assert (v['width'],v['height'],v['r_frame_rate'],v['codec_name'])==(1080,1920,'30/1','h264')
assert a['codec_name']=='aac'
assert abs(float(info['format']['duration'])-8)<.08
assert int(v.get('nb_frames',240))==240
def rms(start,duration):
 raw=subprocess.check_output(['ffmpeg','-v','error','-ss',str(start),'-i',str(p),'-t',str(duration),'-vn','-ac','1','-ar','8000','-f','s16le','pipe:1'])
 samples=array.array('h');samples.frombytes(raw)
 return math.sqrt(sum(x*x for x in samples)/len(samples))/32768
before=rms(2,.5);after=rms(5,.5)
assert before>.003, f'Audio missing before cutoff: {before}'
assert after<.0005, f'Audio persists after cutoff: {after}'
print(f'PASS video/audio and 4s cut: pre={before:.5f}, post={after:.5f}')
