FLAGS=


setup:
	make clean && python3 setup.py install

deploy:
	chmod +x scripts/deploy.sh
	. scripts/deploy.sh

invoke:
	chmod +x scripts/invoke.sh
	. scripts/invoke.sh
clean:
	chmod +x scripts/cleanup.sh
	. scripts/cleanup.sh

data:
	chmod +x scripts/create-bucket.sh
	. scripts/create-bucket.sh	

layer:
	chmod +x scripts/build-layer.sh
	. scripts/build-layer.sh

tests:
	chmod +x scripts/tests.sh
	. scripts/tests.sh
