.PHONY: upgrade-pip deploy delete list

# generate the requirements.txt file from the pyproject.toml file
requirements.txt: pyproject.toml
	pip-compile -o requirements.txt pyproject.toml --resolver=backtracking

# upgrade pip to the latest version
upgrade-pip:
	python -m pip install --upgrade pip

# deploy the feature-pipeline to an EC2 instance on AWS
deploy: requirements.txt
	tar -czvf src.tar ./src
	waxctl aws deploy src.tar \
		-f src/dataflow.py \
		-r requirements.txt \
		--system-setup-file-name ./setup-ec2.sh \
		--region us-east-1 \
		-t t2.micro \
		--name "bytewax" \
		--debug

# stop the feature-pipeline and delete the EC2 instance
delete:
	waxctl aws delete --name "bytewax" --yes

list:
	waxctl aws ls --verbose