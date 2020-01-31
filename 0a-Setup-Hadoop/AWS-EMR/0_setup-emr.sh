# aws cli script to create AWS EMR demo instance
# update the values for your AWS account, region, etc..
# IMPORTANT: script must be run as a single line in the `aws cli` tool

aws emr create-cluster 
    --applications Name=Ganglia Name=Spark Name=Zeppelin 
    --ec2-attributes 
        '{"KeyName":"demo-hadoop",
          "InstanceProfile":"EMR_EC2_DefaultRole",
          "SubnetId":"subnet-0535efab2f83696e8",
          "EmrManagedSlaveSecurityGroup":
          "sg-0e07777bbdf196db0","EmrManagedMasterSecurityGroup":
          "sg-09c90b947497bb876"}' 
    --service-role EMR_DefaultRole 
    --enable-debugging 
    --release-label emr-5.29.0 
    --log-uri 's3n://aws-logs-<yourAwsAccountNum>-us-east-1/elasticmapreduce/' 
    --name 'demo-hadoop' 
    --instance-groups 
        '[{"InstanceCount":1,
        "EbsConfiguration":{"EbsBlockDeviceConfigs":[
            {"VolumeSpecification":{"SizeInGB":32,"VolumeType":"gp2"},
            "VolumesPerInstance":2}]},
            "InstanceGroupType":"MASTER",
            "InstanceType":"m5.xlarge",
            "Name":"Master Instance Group"},
            {"InstanceCount":2,
            "EbsConfiguration":
                {"EbsBlockDeviceConfigs":[
                        {"VolumeSpecification":
                            {"SizeInGB":32,
                            "VolumeType":"gp2"},
                            "VolumesPerInstance":2}]},
                            "InstanceGroupType":"CORE",
                            "InstanceType":"m5.xlarge",
                            "Name":"Core Instance Group"}]' 
    --configurations '[{"Classification":"spark","Properties":{}}]' 
    --scale-down-behavior TERMINATE_AT_TASK_COMPLETION 
    --region us-east-1