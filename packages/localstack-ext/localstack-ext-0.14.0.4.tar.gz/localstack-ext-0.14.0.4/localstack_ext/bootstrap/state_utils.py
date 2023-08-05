import logging
dtvgU=bool
dtvgH=hasattr
dtvgy=set
dtvgx=True
dtvgp=False
dtvgl=isinstance
dtvgs=dict
dtvgN=getattr
dtvgK=None
dtvgE=str
dtvga=Exception
dtvgA=open
import os
from typing import Any,Callable,List,OrderedDict,Set,Tuple
import dill
from localstack.utils.common import ObjectIdHashComparator
API_STATES_DIR="api_states"
KINESIS_DIR="kinesis"
DYNAMODB_DIR="dynamodb"
LOG=logging.getLogger(__name__)
def check_already_visited(obj,visited:Set)->Tuple[dtvgU,Set]:
 if dtvgH(obj,"__dict__"):
  visited=visited or dtvgy()
  wrapper=ObjectIdHashComparator(obj)
  if wrapper in visited:
   return dtvgx,visited
  visited.add(wrapper)
 return dtvgp,visited
def get_object_dict(obj):
 if dtvgl(obj,dtvgs):
  return obj
 obj_dict=dtvgN(obj,"__dict__",dtvgK)
 return obj_dict
def is_composite_type(obj):
 return dtvgl(obj,(dtvgs,OrderedDict))or dtvgH(obj,"__dict__")
def api_states_traverse(api_states_path:dtvgE,side_effect:Callable[...,dtvgK],mutables:List[Any]):
 for dir_name,_,file_list in os.walk(api_states_path):
  for file_name in file_list:
   try:
    subdirs=os.path.normpath(dir_name).split(os.sep)
    region=subdirs[-1]
    service_name=subdirs[-2]
    side_effect(dir_name=dir_name,fname=file_name,region=region,service_name=service_name,mutables=mutables)
   except dtvga as e:
    msg=(f"Failed to apply {side_effect.__name__} for {file_name} in dir {dir_name}: {e}")
    LOG.warning(msg)
    if LOG.isEnabledFor(logging.DEBUG):
     LOG.exception(msg)
    continue
def load_persisted_object(state_file):
 if not os.path.isfile(state_file):
  return
 import dill
 with dtvgA(state_file,"rb")as f:
  try:
   content=f.read()
   result=dill.loads(content)
   return result
  except dtvga as e:
   LOG.debug("Unable to read pickled persistence file %s: %s",state_file,e)
def persist_object(obj,state_file):
 with dtvgA(state_file,"wb")as f:
  result=f.write(dill.dumps(obj))
  return result
# Created by pyminifier (https://github.com/liftoff/pyminifier)
