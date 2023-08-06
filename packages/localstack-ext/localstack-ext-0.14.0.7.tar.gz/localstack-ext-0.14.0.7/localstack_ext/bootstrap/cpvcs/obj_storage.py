import abc
RhUJQ=None
RhUJl=str
RhUJr=classmethod
RhUJP=bool
RhUJE=False
RhUJL=True
RhUJb=isinstance
import logging
import os
from typing import Dict,List,Union
from localstack_ext.bootstrap.cpvcs.models import CPVCSObj,Revision,Version
from localstack_ext.bootstrap.cpvcs.utils.common import config_context
from localstack_ext.bootstrap.cpvcs.utils.serializers import CPVCSSerializer,txt_serializers
LOG=logging.getLogger(__name__)
class StateFileLocator(abc.ABC):
 location="_none_"
 active_instance=RhUJQ
 @abc.abstractmethod
 def get_state_file_location_by_key(self,key:RhUJl)->RhUJl:
  pass
 @RhUJr
 def get(cls,requested_file_locator:RhUJl):
  if not cls.active_instance or cls.active_instance.location!=requested_file_locator:
   for clazz in cls.__subclasses__():
    if clazz.location==requested_file_locator:
     cls.active_instance=clazz()
  return cls.active_instance
class StateFileLocatorLocal(StateFileLocator):
 location="local"
 def get_state_file_location_by_key(self,key:RhUJl)->RhUJl:
  return os.path.join(config_context.get_obj_store_path(),key)
class ObjectStorageProvider(abc.ABC):
 location="_none_"
 active_instance=RhUJQ
 @RhUJr
 def get(cls,state_file_locator:RhUJl,requested_storage:RhUJl,serializers:Dict[RhUJl,CPVCSSerializer]):
  if not cls.active_instance or cls.active_instance.location!=requested_storage:
   state_file_locator=StateFileLocator.get(requested_file_locator=state_file_locator)
   for clazz in cls.__subclasses__():
    if clazz.location==requested_storage:
     cls.active_instance=clazz(state_file_locator=state_file_locator,serializers=serializers)
  return cls.active_instance
 def __init__(self,state_file_locator:StateFileLocator,serializers:Dict[RhUJl,CPVCSSerializer]):
  self.state_file_locator=state_file_locator
  self.serializers=serializers
 @abc.abstractmethod
 def get_terminal_revision(self,revision_path_root:Revision):
  pass
 @abc.abstractmethod
 def get_state_file_location_by_key(self,key:RhUJl)->RhUJl:
  pass
 @abc.abstractmethod
 def get_version_by_key(self,key:RhUJl)->Version:
  pass
 @abc.abstractmethod
 def get_revision_by_key(self,key:RhUJl)->Revision:
  pass
 @abc.abstractmethod
 def get_revision_or_version_by_key(self,key:RhUJl)->Union[Revision,Version]:
  pass
 @abc.abstractmethod
 def get_delta_file_by_key(self,key:RhUJl)->RhUJl:
  pass
 @abc.abstractmethod
 def upsert_objects(self,*args:CPVCSObj)->List[RhUJl]:
  pass
 @abc.abstractmethod
 def update_revision_key(self,old_key:RhUJl,new_key:RhUJl,referenced_by_version:RhUJl=RhUJQ):
  pass
 @abc.abstractmethod
 def version_exists(self,key:RhUJl)->RhUJP:
  pass
 @abc.abstractmethod
 def merge_remote_into_local_version(self,remote_location:RhUJl,key:RhUJl):
  pass
 @abc.abstractmethod
 def _update_key(self,old_key:RhUJl,new_key:RhUJl,base_path:RhUJl)->RhUJP:
  pass
 @abc.abstractmethod
 def _serialize(self,*args:CPVCSObj)->List[RhUJl]:
  pass
 @abc.abstractmethod
 def _deserialize(self,key_serializer:Dict[RhUJl,RhUJl],remote_location:RhUJl=RhUJQ)->List[CPVCSObj]:
  pass
class ObjectStorageLocal(ObjectStorageProvider):
 location="local"
 def get_terminal_revision(self,revision_path_root:Revision)->Revision:
  result=revision_path_root
  while result.assoc_commit:
   result=self.get_revision_by_key(result.assoc_commit.head_ptr)
  return result
 def get_state_file_location_by_key(self,key:RhUJl)->RhUJl:
  return self.state_file_locator.get_state_file_location_by_key(key)
 def get_version_by_key(self,key:RhUJl)->Version:
  return self._deserialize({key:"version"})[0]
 def get_revision_by_key(self,key:RhUJl)->Revision:
  return self._deserialize({key:"revision"})[0]
 def get_revision_or_version_by_key(self,key:RhUJl)->Union[Revision,Version]:
  revision=self._deserialize({key:"revision"})[0]
  if revision:
   return revision
  version=self._deserialize({key:"version"})[0]
  if version:
   return version
  LOG.warning(f"No revision or version found with key {key}")
 def get_delta_file_by_key(self,key:RhUJl)->RhUJl:
  path=os.path.join(config_context.get_delta_log_path(),key)
  if os.path.isfile(path):
   return path
  LOG.warning(f"No state file found for key: {key}")
 def upsert_objects(self,*args:CPVCSObj)->List[RhUJl]:
  return self._serialize(*args)
 def update_revision_key(self,old_key:RhUJl,new_key:RhUJl,referenced_by_version:RhUJl=RhUJQ):
  updated=self._update_key(old_key,new_key,config_context.get_rev_obj_store_path())
  if not updated:
   LOG.warning(f"No revision found with key {old_key} to update")
   return
  if referenced_by_version:
   version=self.get_version_by_key(referenced_by_version)
   version.active_revision_ptr=new_key
   version.outgoing_revision_ptrs.remove(old_key)
   version.outgoing_revision_ptrs.add(new_key)
   self.upsert_objects(version)
 def version_exists(self,key:RhUJl)->RhUJP:
  return os.path.isfile(os.path.join(config_context.get_ver_obj_store_path(),key))
 def merge_remote_into_local_version(self,remote_location:RhUJl,key:RhUJl):
  local_version=self.get_version_by_key(key)
  remote_version=self._deserialize({key:"version"},remote_location)[0]
  local_version.outgoing_revision_ptrs.update(remote_version.outgoing_revision_ptrs)
  self.upsert_objects(local_version)
 def _update_key(self,old_key:RhUJl,new_key:RhUJl,base_path:RhUJl)->RhUJP:
  path_old_key=os.path.join(base_path,old_key)
  if not os.path.isfile(path_old_key):
   return RhUJE
  path_new_key=os.path.join(base_path,new_key)
  os.rename(path_old_key,path_new_key)
  return RhUJL
 def _serialize(self,*args:CPVCSObj)->List[RhUJl]:
  hash_refs=[]
  for cpvcs_obj in args:
   if RhUJb(cpvcs_obj,Version):
    hash_refs.append(self.serializers["version"].store_obj(cpvcs_obj))
   elif RhUJb(cpvcs_obj,Revision):
    hash_refs.append(self.serializers["revision"].store_obj(cpvcs_obj))
  return hash_refs
 def _deserialize(self,key_serializer:Dict[RhUJl,RhUJl],remote_location:RhUJl=RhUJQ)->List[Union[Revision,Version]]:
  return[self.serializers[serializer].retrieve_obj(key,remote_location)for key,serializer in key_serializer.items()]
default_storage=ObjectStorageProvider.get(state_file_locator="local",requested_storage="local",serializers=txt_serializers)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
