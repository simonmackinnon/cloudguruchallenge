rm -f ddb-to-firehose.zip

zip ddb-to-firehose.zip ddb-to-firehose.py

aws s3 cp ddb-to-firehose.zip s3://$(aws cloudformation describe-stacks --stack-name core-infrastructure-function-bucket --query "Stacks[0].Outputs[?OutputKey=='BucketName'].OutputValue" --output text)

aws lambda update-function-code \
--function-name $(aws cloudformation describe-stacks --stack-name dashboard-covid-app --query "Stacks[0].Outputs[?OutputKey=='ddbToFirehoseFunction'].OutputValue" --output text) \
--s3-bucket $(aws cloudformation describe-stacks --stack-name core-infrastructure-function-bucket --query "Stacks[0].Outputs[?OutputKey=='BucketName'].OutputValue" --output text) \
--s3-key ddb-to-firehose.zip \
--publish

rm -f ddb-to-firehose.zip