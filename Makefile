FLAGS=


deploy:
	chmod +x scripts/deploy.sh
	. scripts/deploy.sh

invoke:
	chmod +x scripts/invoke.sh
	. scripts/invoke.sh

clean:
	chmod +x scripts/cleanup.sh
	. scripts/cleanup.sh

upload:
	chmod +x scripts/uplod-data-s3.sh
	. scripts/uplod-data-s3.sh

dynamo:
	chmod +x scripts/prepare-data-dynamodb.sh
	. scripts/prepare-data-dynamodb.sh

layer:
	chmod +x scripts/build-layer.sh
	. scripts/build-layer.sh

pipeline:
	chmod +x scripts/execute-pipeline.sh
	. scripts/execute-pipeline.sh

tests:
	chmod +x scripts/tests.sh
	. scripts/tests.sh
