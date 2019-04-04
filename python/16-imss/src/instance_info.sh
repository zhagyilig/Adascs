#!/bin/bash
# 查询实例的tag和内网ip

while read line
do
    aws ec2 describe-instances --filter Name=tag:Name,Values=$line --query 'Reservations[*].Instances[*].[Tags[?Key==`Name`].Value|[0],PrivateIpAddress]' --output text  --profile lsg >> hostname.txt
done <  instance_tag.txt
