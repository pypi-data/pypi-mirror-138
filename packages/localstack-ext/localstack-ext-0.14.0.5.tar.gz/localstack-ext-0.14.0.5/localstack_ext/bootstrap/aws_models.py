from localstack.utils.aws import aws_models
Iymxs=super
Iymxi=None
IymxT=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  Iymxs(LambdaLayer,self).__init__(arn)
  self.cwd=Iymxi
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.IymxT.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,IymxT,env=Iymxi):
  Iymxs(RDSDatabase,self).__init__(IymxT,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,IymxT,env=Iymxi):
  Iymxs(RDSCluster,self).__init__(IymxT,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,IymxT,env=Iymxi):
  Iymxs(AppSyncAPI,self).__init__(IymxT,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,IymxT,env=Iymxi):
  Iymxs(AmplifyApp,self).__init__(IymxT,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,IymxT,env=Iymxi):
  Iymxs(ElastiCacheCluster,self).__init__(IymxT,env=env)
class TransferServer(BaseComponent):
 def __init__(self,IymxT,env=Iymxi):
  Iymxs(TransferServer,self).__init__(IymxT,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,IymxT,env=Iymxi):
  Iymxs(CloudFrontDistribution,self).__init__(IymxT,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,IymxT,env=Iymxi):
  Iymxs(CodeCommitRepository,self).__init__(IymxT,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
