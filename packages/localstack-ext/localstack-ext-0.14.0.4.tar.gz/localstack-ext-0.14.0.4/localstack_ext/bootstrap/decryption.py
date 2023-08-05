import inspect
YISJD=bytes
YISJT=None
YISJU=isinstance
YISJO=list
YISJw=getattr
YISJz=open
YISJN=property
YISJy=Exception
YISJH=setattr
YISJl=True
import os.path
import sys
import traceback
from importlib.abc import MetaPathFinder,SourceLoader
from importlib.util import spec_from_file_location
import pyaes
class DecryptionHandler:
 decryption_key:YISJD
 def __init__(self,decryption_key:YISJD):
  self.decryption_key=decryption_key
 def decrypt(self,content)->YISJD:
  cipher=pyaes.AESModeOfOperationCBC(self.decryption_key,iv="\0"*16)
  decrypter=pyaes.Decrypter(cipher)
  decrypted=decrypter.feed(content)
  decrypted+=decrypter.feed()
  decrypted=decrypted.partition(b"\0")[0]
  return decrypted
class EncryptedFileFinder(MetaPathFinder):
 decryption_handler:DecryptionHandler
 def __init__(self,decryption_handler:DecryptionHandler):
  self.decryption_handler=decryption_handler
 def find_spec(self,fullname,path,target=YISJT):
  if path and not YISJU(path,YISJO):
   path=YISJO(YISJw(path,"_path",[]))
  if not path:
   return YISJT
  name=fullname.split(".")[-1]
  file_path=os.path.join(path[0],name+".py")
  enc=file_path+".enc"
  if not os.path.isfile(enc):
   return YISJT
  if os.path.isfile(file_path):
   return YISJT
  return spec_from_file_location(fullname,enc,loader=DecryptingLoader(enc,self.decryption_handler))
class DecryptingLoader(SourceLoader):
 decryption_handler:DecryptionHandler
 def __init__(self,encrypted_file,decryption_handler:DecryptionHandler):
  self.encrypted_file=encrypted_file
  self.decryption_handler=decryption_handler
 def get_filename(self,fullname):
  return self.encrypted_file
 def get_data(self,filename):
  with YISJz(filename,"rb")as f:
   data=f.read()
  data=self.decryption_handler.decrypt(data)
  return data
def init_source_decryption(decryption_handler:DecryptionHandler):
 sys.meta_path.insert(0,EncryptedFileFinder(decryption_handler))
 patch_traceback_lines()
 patch_inspect_findsource()
def patch_traceback_lines():
 if YISJw(traceback.FrameSummary,"_ls_patch_applied",YISJT):
  return
 @YISJN
 def line(self):
  try:
   return line_orig.fget(self)
  except YISJy:
   self._line=""
   return self._line
 line_orig=traceback.FrameSummary.line
 YISJH(traceback.FrameSummary,"line",line)
 traceback.FrameSummary._ls_patch_applied=YISJl
def patch_inspect_findsource():
 if YISJw(inspect,"_ls_patch_applied",YISJT):
  return
 def findsource(*args,**kwargs):
  try:
   return findsource_orig(*args,**kwargs)
  except YISJy:
   return[],0
 findsource_orig=inspect.findsource
 inspect.findsource=findsource
 inspect._ls_patch_applied=YISJl
# Created by pyminifier (https://github.com/liftoff/pyminifier)
