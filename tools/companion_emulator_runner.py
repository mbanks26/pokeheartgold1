"""Frame-controlled libretro frontend for isolated DS gameplay verification."""
import ctypes as C,json,sys,time,traceback,hashlib,struct,re
from pathlib import Path
from PIL import Image
import numpy as np
import argparse
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--core',type=Path,required=True)
parser.add_argument('--rom',type=Path,required=True)
parser.add_argument('--symbols',type=Path,required=True)
parser.add_argument('--output',type=Path,required=True)
parser.add_argument('--allow-fixture-writes',action='store_true')
args=parser.parse_args()
ROOT=args.output.resolve();ROOT.mkdir(parents=True,exist_ok=True)
map_path=args.symbols
symbols={m.group(2):int(m.group(1),16) for m in re.finditer(r'^\s*([0-9A-Fa-f]{8})\s+[0-9A-Fa-f]{8}\s+\.bss\s+(\w+)',map_path.read_text(),re.M)}
lib=C.CDLL(str(args.core.resolve()))
ENV=C.CFUNCTYPE(C.c_bool,C.c_uint,C.c_void_p);VIDEO=C.CFUNCTYPE(None,C.c_void_p,C.c_uint,C.c_uint,C.c_size_t)
AUDIO=C.CFUNCTYPE(None,C.c_int16,C.c_int16);BATCH=C.CFUNCTYPE(C.c_size_t,C.c_void_p,C.c_size_t)
POLL=C.CFUNCTYPE(None);INPUT=C.CFUNCTYPE(C.c_int16,C.c_uint,C.c_uint,C.c_uint,C.c_uint);LOG=C.CFUNCTYPE(None,C.c_int,C.c_char_p)
class Var(C.Structure):_fields_=[('key',C.c_char_p),('value',C.c_char_p)]
class Game(C.Structure):_fields_=[('path',C.c_char_p),('data',C.c_void_p),('size',C.c_size_t),('meta',C.c_char_p)]
variables={};strings=[str(ROOT).encode()];pixel=2;image=None;buttons=set();touch=None;frame=0;capture=False
names={'B':0,'Y':1,'SELECT':2,'START':3,'UP':4,'DOWN':5,'LEFT':6,'RIGHT':7,'A':8,'X':9,'L':10,'R':11}
options={b'desmume_cpu_mode':b'jit',b'desmume_pointer_mouse':b'enabled',b'desmume_pointer_type':b'touch',b'desmume_firmware_language':b'English',b'desmume_num_cores':b'1',b'desmume_screens_layout':b'top/bottom',b'desmume_gfx_multisampling':b'disabled'}
@LOG
def log(level,fmt):pass
@ENV
def environ(cmd,data):
 global pixel
 if cmd in (9,31):C.cast(data,C.POINTER(C.c_char_p))[0]=strings[0];return True
 if cmd==27:C.cast(data,C.POINTER(C.c_void_p))[0]=C.cast(log,C.c_void_p).value;return True
 if cmd==52:C.cast(data,C.POINTER(C.c_uint))[0]=0;return True
 if cmd==39:C.cast(data,C.POINTER(C.c_uint))[0]=0;return True
 if cmd==16:
  a=C.cast(data,C.POINTER(Var));i=0
  while a[i].key:
   value=a[i].value.split(b'; ',1)[-1].split(b'|')[0];variables[a[i].key]=value;i+=1
  return True
 if cmd==15:
  a=C.cast(data,C.POINTER(Var));key=a.contents.key;value=options.get(key,variables.get(key));a.contents.value=value
  return value is not None
 if cmd==17:C.cast(data,C.POINTER(C.c_bool))[0]=False;return True
 if cmd==10:pixel=C.cast(data,C.POINTER(C.c_int))[0];return True
 if cmd in (11,18,35,37,53,55):return True
 return False
@VIDEO
def video(data,width,height,pitch):
 global image
 if not data or not capture:return
 raw=C.string_at(data,pitch*height)
 if pixel==1:
  a=np.frombuffer(raw,np.uint8).reshape(height,pitch)[:,:width*4].reshape(height,width,4);image=Image.fromarray(a[:,:,[2,1,0]],'RGB')
 else:
  a=np.frombuffer(raw,np.uint16).reshape(height,pitch//2)[:,:width];rgb=np.empty((height,width,3),np.uint8)
  rgb[:,:,0]=((a>>11)&31)*255//31;rgb[:,:,1]=((a>>5)&63)*255//63;rgb[:,:,2]=(a&31)*255//31;image=Image.fromarray(rgb,'RGB')
@AUDIO
def audio(l,r):pass
@BATCH
def batch(data,count):return count
@POLL
def poll():pass
@INPUT
def input_state(port,device,index,id):
 if port!=0:return 0
 if device==1:return int(id in buttons)
 if device==6 and touch is not None:
  if id==2:return 1
  if id==0:return round((touch[0]+.5)/256*65535-32768)
  if id==1:return round((touch[1]+192+.5)/384*65535-32768)
 return 0
for name,cb in [('environment',environ),('video_refresh',video),('audio_sample',audio),('audio_sample_batch',batch),('input_poll',poll),('input_state',input_state)]:getattr(lib,'retro_set_'+name)(cb)
lib.retro_get_memory_data.restype=C.c_void_p;lib.retro_get_memory_size.restype=C.c_size_t
lib.retro_serialize_size.restype=C.c_size_t;lib.retro_serialize.argtypes=[C.c_void_p,C.c_size_t];lib.retro_serialize.restype=C.c_bool
lib.retro_unserialize.argtypes=[C.c_void_p,C.c_size_t];lib.retro_unserialize.restype=C.c_bool
lib.retro_load_game.argtypes=[C.POINTER(Game)];lib.retro_load_game.restype=C.c_bool
rom=args.rom.resolve();lib.retro_init();assert lib.retro_load_game(C.byref(Game(str(rom).encode(),None,0,None)))
ram=lib.retro_get_memory_data(2);size=lib.retro_get_memory_size(2)
print(json.dumps({'ready':True,'rom':rom.name,'sha1':hashlib.sha1(rom.read_bytes()).hexdigest(),'ram_size':size,'options':{k.decode():v.decode() for k,v in options.items()}}),flush=True)
def address(a):
 a=int(a,0) if isinstance(a,str) else a
 if a>=0x2000000:a-=0x2000000
 assert 0<=a<size
 return ram+a
failures=0
rom_sha1=hashlib.sha1(rom.read_bytes()).hexdigest()
logfile=(ROOT/(rom.stem+'-commands.jsonl')).open('a')
logfile.write(json.dumps({'session_start':True,'rom_sha1':rom_sha1,'symbols':str(map_path),'core_sha256':hashlib.sha256(args.core.read_bytes()).hexdigest()})+'\n');logfile.flush()
for line in sys.stdin:
 try:
  command=json.loads(line);started=time.time();result={}
  if 'load' in command:
   assert json.loads((ROOT/(command['load']+'.json')).read_text())['rom_sha1']==rom_sha1,'Cross-ROM save state refused'
   raw=(ROOT/command['load']).read_bytes();buffer=C.create_string_buffer(raw);assert lib.retro_unserialize(buffer,len(raw));result['loaded']=command['load']
  if 'write' in command:
   assert args.allow_fixture_writes,'Raw writes require --allow-fixture-writes and an isolated authored test save'
   a,raw=command['write'];raw=bytes.fromhex(raw);C.memmove(address(a),raw,len(raw));result['fixture_write']=[a,len(raw)]
  if 'talk' in command:
   cycles=0
   for _ in range(command['talk']):
    f=struct.unpack('<I',C.string_at(address(symbols['sFieldSysPtr']),4))[0]
    if 0x2000000<=f<0x2400000 and C.string_at(address(f+16),4)==b'\0'*4:break
    buttons={names[command.get('button','A')]}
    for _ in range(8):lib.retro_run();frame+=1
    buttons=set()
    for _ in range(90):lib.retro_run();frame+=1
    cycles+=1
   result['talk_cycles']=cycles
   capture='shot' in command;lib.retro_run();frame+=1;capture=False
  if 'frames' in command:
   buttons={names[x.upper()] for x in command.get('buttons',[])};touch=command.get('touch');n=command['frames']
   samples=[]
   for i in range(n):
    capture=i==n-1 and 'shot' in command;lib.retro_run();frame+=1
    if command.get('sample'):
     def u(a):return struct.unpack('<I',C.string_at(address(a),4))[0]
     f=u(symbols['sFieldSysPtr']);row={'frame':frame}
     if 0x2000000<=f<0x2400000:
      m=u(f+60)
      if 0x2000000<=m<0x2400000:
       start=u(m+292)
       for j in range(u(m+4)):
        a=start+j*300;id=u(a+8)
        if u(a)&1 and id in (252,253,255):row[str(id)]=[u(a+k) for k in (100,104,108)]
     samples.append(row)
   if samples:
    (ROOT/command['sample']).write_text(json.dumps(samples))
    result['samples']={'frames':len(samples),'companion_present':sum('252' in x for x in samples),'pokemon_present':sum('253' in x for x in samples),'file':command['sample']}
   buttons=set();touch=None;capture=False
  if command.get('inspect'):
   def u(a):return struct.unpack('<I',C.string_at(address(a),4))[0]
   f=u(symbols['sFieldSysPtr']);info={'field_system':hex(f),'battle_paired':u(symbols['sSabrinaPairedBattleArt'])}
   if 0x2000000<=f<0x2400000:
    info.update(map=u(u(f+32)),task=hex(u(f+16)))
    m=u(f+60);v=u(f+64);sd=u(f+12)
    if 0x2000000<=v<0x2400000:info.update(avatar_state=u(v+24),gender=u(v+28))
    if 0x2000000<=m<0x2400000:
     objs=[];start=u(m+292)
     for i in range(u(m+4)):
      a=start+i*300
      if u(a)&1:objs.append({'slot':i,'address':hex(a),'id':u(a+8),'sprite':u(a+16),'script':u(a+32),'xyz':[u(a+k) for k in (100,104,108)],'previous':[u(a+k) for k in (88,92,96)],'direction':u(a+40),'flags':hex(u(a))})
     info['objects']=objs
    if 0x2000000<=sd<0x2400000:
     flags=sd+16+u(sd+0x23014+4*16+8)+0x170*2;tail=C.string_at(address(flags+363),1)[0]
     party=sd+16+u(sd+0x23014+2*16+8)
     info.update(joined=bool(tail&128),initialized=bool(tail&64),save_address=hex(sd),flag_address=hex(flags),party_address=hex(party),party_header=C.string_at(address(party),8).hex())
    info['controller']=[u(symbols['sSabrinaCompanion']+i*4) for i in (0,1,2,71,72,73,74,75,76)]
   result['game']=info
  if 'read' in command:
   a,n=command['read'];result['read']=C.string_at(address(a),n).hex()
  if 'dump' in command:(ROOT/command['dump']).write_bytes(C.string_at(ram,size));result['dump']=command['dump']
  if 'state' in command:
   n=lib.retro_serialize_size();buffer=C.create_string_buffer(n);assert lib.retro_serialize(buffer,n);(ROOT/command['state']).write_bytes(buffer.raw);(ROOT/(command['state']+'.json')).write_text(json.dumps({'rom_sha1':rom_sha1,'frame':frame}));result['state']=command['state']
  if 'shot' in command:
   assert image is not None;image.save(ROOT/command['shot']);result['shot']=command['shot']
  if 'expect' in command:
   info=result['game'];objects=info.get('objects',[])
   for key,value in command['expect'].items():
    if key=='counts':
     for id,n in value.items():assert sum(o['id']==int(id) for o in objects)==n,(id,objects)
    elif key=='directions':
     for id,direction in value.items():assert next(o for o in objects if o['id']==int(id))['direction']==direction,(id,objects)
    elif key=='positions':
     for id,xyz in value.items():assert next(o for o in objects if o['id']==int(id))['xyz']==xyz,(id,objects)
    else:assert info[key]==value,(key,info.get(key),value)
   result['assertions']='PASS'
  result.update(frame=frame,seconds=round(time.time()-started,3));logfile.write(json.dumps({'command':command,'result':result})+'\n');logfile.flush();print(json.dumps(result),flush=True)
  if command.get('exit'):break
 except Exception as error:
  failures+=1
  traceback.print_exc();logfile.write(json.dumps({'command':command,'error':str(error)})+'\n');logfile.flush();print(json.dumps({'failed':str(error)}),flush=True)
lib.retro_unload_game();lib.retro_deinit()
raise SystemExit(1 if failures else 0)
