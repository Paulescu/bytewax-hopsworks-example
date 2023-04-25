.PHONY: deploy delete list project-files run

# install Poetry and Python dependencies
init:
	curl -sSL https://install.python-poetry.org | python3 -
	poetry install

# run the feature-pipeline locally
run:
	poetry run python src/dataflow.py

# generate a tar file with project files to send to AWS EC2 instance
project-files:
	tar \
	--exclude={'.git','.gitignore','requirements.txt','poetry.lock','README.md','Makefile','setup-ec2.sh','.venv','*.tar','.DS_Store','__pycache__','images'} \
	-vzcf project-files.tar -C . .

# deploy the feature-pipeline to an EC2 instance on AWS
deploy: project-files
	waxctl aws deploy project-files.tar \
		-f src/dataflow.py \
		--system-setup-file-name ./setup-ec2.sh \
		--region us-east-1 \
		-t t2.micro \
		--name "bytewax2" \
		--python-package \
		--debug \
		-E HOPSWORKS_PROJECT_NAME=${HOPSWORKS_PROJECT_NAME},HOPSWORKS_API_KEY=${HOPSWORKS_API_KEY}

# list all bytewax deployments
list:
	waxctl aws ls --verbose --name "bytewax2"

# stop the feature-pipeline and delete the EC2 instance
delete:
	waxctl aws delete --name "bytewax2" --yes