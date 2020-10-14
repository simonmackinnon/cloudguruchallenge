rm -rf package
rm -rf v-env
rm -f CovidDataFunction.zip

virtualenv v-env
source v-env/bin/activate
pip3 install --prefix= --target ./package -r requirements.txt
deactivate

cd v-env/lib/python3.6/site-packages
zip -r9 ${OLDPWD}/CovidDataFunction.zip .
cd $OLDPWD
zip -g CovidDataFunction.zip *.py

aws s3 cp CovidDataFunction.zip s3://$(aws cloudformation describe-stacks --stack-name core-infrastructure-function-bucket --query "Stacks[0].Outputs[?OutputKey=='BucketName'].OutputValue" --output text)

rm -rf package
rm -rf v-env
rm -f CovidDataFunction.zip
