.PHONY all
all: build package upload

.PHONY clean
clean:
	rm -rf package
	rm -rf v-env
	rm -f CovidDataFunction.zip

.PHONY build
build:
    virtualenv v-env
    source v-env/bin/activate
    pip3 install --prefix= --target ./package -r requirements.txt
    deactivate
    

.PHONY package
package:
	cd v-env/lib/python3.6/site-packages
    zip -r9 ${OLDPWD}/CovidDataFunction.zip .
    cd $OLDPWD
    zip -g CovidDataFunction.zip *.py

.PHONY upload
upload:
	aws s3 cp CovidDataFunction.zip s3://core-infrastructure-function-bucket-s3bucket-izixjpai4jrm
