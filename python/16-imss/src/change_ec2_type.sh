#!/bin/bash

instance_id=$1
instance_type=$2
profile_id=$3

if [[ $profile_id == "" ]] ; then
    profile_id="lsg"
fi

aws ec2 stop-instances --instance-id $instance_id --profile $profile_id
sleep(8)
aws ec2 modify-instance-attribute --instance-id $instance_id   --instance-type "{\"Value\": \"$instance_type\"}" --profile $profile_id
sleep(8)
aws ec2 start-instances  --instance-id $instance_id --profile $profile_id


