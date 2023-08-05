from localstack.utils.aws import aws_models
diXcL=super
diXcO=None
diXcy=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  diXcL(LambdaLayer,self).__init__(arn)
  self.cwd=diXcO
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.diXcy.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,diXcy,env=diXcO):
  diXcL(RDSDatabase,self).__init__(diXcy,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,diXcy,env=diXcO):
  diXcL(RDSCluster,self).__init__(diXcy,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,diXcy,env=diXcO):
  diXcL(AppSyncAPI,self).__init__(diXcy,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,diXcy,env=diXcO):
  diXcL(AmplifyApp,self).__init__(diXcy,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,diXcy,env=diXcO):
  diXcL(ElastiCacheCluster,self).__init__(diXcy,env=env)
class TransferServer(BaseComponent):
 def __init__(self,diXcy,env=diXcO):
  diXcL(TransferServer,self).__init__(diXcy,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,diXcy,env=diXcO):
  diXcL(CloudFrontDistribution,self).__init__(diXcy,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,diXcy,env=diXcO):
  diXcL(CodeCommitRepository,self).__init__(diXcy,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
