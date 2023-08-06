from localstack.utils.aws import aws_models
lLfkQ=super
lLfkg=None
lLfkm=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  lLfkQ(LambdaLayer,self).__init__(arn)
  self.cwd=lLfkg
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.lLfkm.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,lLfkm,env=lLfkg):
  lLfkQ(RDSDatabase,self).__init__(lLfkm,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,lLfkm,env=lLfkg):
  lLfkQ(RDSCluster,self).__init__(lLfkm,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,lLfkm,env=lLfkg):
  lLfkQ(AppSyncAPI,self).__init__(lLfkm,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,lLfkm,env=lLfkg):
  lLfkQ(AmplifyApp,self).__init__(lLfkm,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,lLfkm,env=lLfkg):
  lLfkQ(ElastiCacheCluster,self).__init__(lLfkm,env=env)
class TransferServer(BaseComponent):
 def __init__(self,lLfkm,env=lLfkg):
  lLfkQ(TransferServer,self).__init__(lLfkm,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,lLfkm,env=lLfkg):
  lLfkQ(CloudFrontDistribution,self).__init__(lLfkm,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,lLfkm,env=lLfkg):
  lLfkQ(CodeCommitRepository,self).__init__(lLfkm,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
