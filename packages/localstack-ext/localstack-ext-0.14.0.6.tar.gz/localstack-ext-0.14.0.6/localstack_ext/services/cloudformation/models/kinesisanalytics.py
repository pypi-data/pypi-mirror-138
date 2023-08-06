from localstack.services.cloudformation.service_models import REF_ID_ATTRS,GenericBaseModel
frzqi=staticmethod
frzqg=super
class KinesisAnalyticsApplicationOutput(GenericBaseModel):
 @frzqi
 def cloudformation_type():
  return "AWS::KinesisAnalytics::ApplicationOutput"
 def get_cfn_attribute(self,attribute_name):
  if attribute_name in REF_ID_ATTRS:
   app_name=self.props.get("ApplicationName")
   output_name=self.props.get("Output",{}).get("Name")
   if app_name and output_name:
    return "%s!%s"%(app_name,output_name)
  return frzqg(KinesisAnalyticsApplicationOutput,self).get_cfn_attribute(attribute_name)
class KinesisAnalyticsApplication(GenericBaseModel):
 @frzqi
 def cloudformation_type():
  return "AWS::KinesisAnalytics::Application"
 def get_cfn_attribute(self,attribute_name):
  if attribute_name in REF_ID_ATTRS:
   app_name=self.props.get("ApplicationName")
   if app_name:
    return app_name
  return frzqg(KinesisAnalyticsApplication,self).get_cfn_attribute(attribute_name)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
