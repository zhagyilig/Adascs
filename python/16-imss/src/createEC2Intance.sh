#!/bin/bash

run_instance() {  
  # 根据配置文件创建EC2，返回instance_id  
  instance_id=$(aws ec2 run-instances --profile lsg --count 1 --cli-input-json file://ec2runinst.json --query 'Instances[0].[InstanceId]' | grep -o -E "i-\w{17}")  
  echo "InstanceId: $instance_id"

  # 为EC2添加tag
  echo "Add tags: Name:$1"
  echo $1 >> instance_tag.txt
  aws ec2 create-tags --profile lsg --resources $instance_id --tags Key=Name,Value="$1"
}  

run_instance $1
