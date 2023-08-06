from localstack.utils.aws import aws_models
aqnxS=super
aqnxk=None
aqnxK=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  aqnxS(LambdaLayer,self).__init__(arn)
  self.cwd=aqnxk
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.aqnxK.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,aqnxK,env=aqnxk):
  aqnxS(RDSDatabase,self).__init__(aqnxK,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,aqnxK,env=aqnxk):
  aqnxS(RDSCluster,self).__init__(aqnxK,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,aqnxK,env=aqnxk):
  aqnxS(AppSyncAPI,self).__init__(aqnxK,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,aqnxK,env=aqnxk):
  aqnxS(AmplifyApp,self).__init__(aqnxK,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,aqnxK,env=aqnxk):
  aqnxS(ElastiCacheCluster,self).__init__(aqnxK,env=env)
class TransferServer(BaseComponent):
 def __init__(self,aqnxK,env=aqnxk):
  aqnxS(TransferServer,self).__init__(aqnxK,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,aqnxK,env=aqnxk):
  aqnxS(CloudFrontDistribution,self).__init__(aqnxK,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,aqnxK,env=aqnxk):
  aqnxS(CodeCommitRepository,self).__init__(aqnxK,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
