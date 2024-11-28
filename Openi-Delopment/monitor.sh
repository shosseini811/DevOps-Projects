#!/bin/bash
while true; do
    clear
    echo "=== Stack Status ==="
    aws cloudformation describe-stacks --stack-name openai-api-stack --query 'Stacks[0].StackStatus' --output text
    echo -e "\n=== Recent Events ==="
    aws cloudformation describe-stack-events --stack-name openai-api-stack --query 'StackEvents[0:5]' --output table
    sleep 5
done 