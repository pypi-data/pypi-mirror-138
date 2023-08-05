import logging
lPJxH=bool
lPJxW=hasattr
lPJxO=set
lPJxh=True
lPJxI=False
lPJxk=isinstance
lPJxw=dict
lPJxT=getattr
lPJxg=None
lPJxE=str
lPJxy=Exception
lPJxL=open
import os
from typing import Any,Callable,List,OrderedDict,Set,Tuple
import dill
from localstack.utils.common import ObjectIdHashComparator
API_STATES_DIR="api_states"
KINESIS_DIR="kinesis"
DYNAMODB_DIR="dynamodb"
LOG=logging.getLogger(__name__)
def check_already_visited(obj,visited:Set)->Tuple[lPJxH,Set]:
 if lPJxW(obj,"__dict__"):
  visited=visited or lPJxO()
  wrapper=ObjectIdHashComparator(obj)
  if wrapper in visited:
   return lPJxh,visited
  visited.add(wrapper)
 return lPJxI,visited
def get_object_dict(obj):
 if lPJxk(obj,lPJxw):
  return obj
 obj_dict=lPJxT(obj,"__dict__",lPJxg)
 return obj_dict
def is_composite_type(obj):
 return lPJxk(obj,(lPJxw,OrderedDict))or lPJxW(obj,"__dict__")
def api_states_traverse(api_states_path:lPJxE,side_effect:Callable[...,lPJxg],mutables:List[Any]):
 for dir_name,_,file_list in os.walk(api_states_path):
  for file_name in file_list:
   try:
    subdirs=os.path.normpath(dir_name).split(os.sep)
    region=subdirs[-1]
    service_name=subdirs[-2]
    side_effect(dir_name=dir_name,fname=file_name,region=region,service_name=service_name,mutables=mutables)
   except lPJxy as e:
    msg=(f"Failed to apply {side_effect.__name__} for {file_name} in dir {dir_name}: {e}")
    LOG.warning(msg)
    if LOG.isEnabledFor(logging.DEBUG):
     LOG.exception(msg)
    continue
def load_persisted_object(state_file):
 if not os.path.isfile(state_file):
  return
 import dill
 with lPJxL(state_file,"rb")as f:
  try:
   content=f.read()
   result=dill.loads(content)
   return result
  except lPJxy as e:
   LOG.debug("Unable to read pickled persistence file %s: %s",state_file,e)
def persist_object(obj,state_file):
 with lPJxL(state_file,"wb")as f:
  result=f.write(dill.dumps(obj))
  return result
# Created by pyminifier (https://github.com/liftoff/pyminifier)
