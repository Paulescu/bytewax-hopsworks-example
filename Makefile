.PHONY: deploy delete list project-files

# generate a tar file with project files
project-files:
	tar \
	--exclude={'.git','.gitignore','requirements.txt','poetry.lock','README.md','Makefile','setup-ec2.sh','.venv','*.tar','.DS_Store'} \
	-vzcf project-files.tar -C . .

# deploy the feature-pipeline to an EC2 instance on AWS
deploy: project-files
	waxctl aws deploy project-files.tar \
		-f src/dataflow.py \
		--system-setup-file-name ./setup-ec2.sh \
		--region us-east-1 \
		-t t2.micro \
		--name "bytewax" \
		--python-package \
		--debug \
		-E HOPSWORKS_PROJECT_NAME=${HOPSWORKS_PROJECT_NAME},HOPSWORKS_API_KEY=${HOPSWORKS_API_KEY}

# stop the feature-pipeline and delete the EC2 instance
delete:
	waxctl aws delete --name "bytewax" --yes

# list all bytewax deployments
list:
	waxctl aws ls --verbose