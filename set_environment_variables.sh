#!/bin/bash

echo "Please enter HOPSWORKS_PROJECT_NAME:"
read HOPSWORKS_PROJECT_NAME

echo "Please enter HOPSWORKS_API_KEY:"
read HOPSWORKS_API_KEY

export HOPSWORKS_PROJECT_NAME=$HOPSWORKS_PROJECT_NAME
export HOPSWORKS_API_KEY=$HOPSWORKS_API_KEY

echo "Variables set as environment variables"