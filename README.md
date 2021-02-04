# ecrs-buildspec
Buildspec file to synchronize container images from 3rd party registry to private registry.

## What this buildspec does
On the install phase:
- Define docker:18 as it is needed to work with docker images.
- Install yarnpkg gpg key, as for the time this buildspec created, the gpg key on `aws/codebuild/standard:4.0` image is already expired.
- Install jq to parse and extract information from [config.json](config.json).
- Install latest aws-cli version 2

On the build phase:
- Run a command to get private registry URI, and assign it to `$registry`.
- Run a command to authenticate docker service against our private `$registry` URI.
- Run [ecrsync.py](ecrsync.py) code

## What ecrsync.py does
- Read configuration from [config.json](config.json).
- Define container images to sync, its tag, the 3rd party registry origin, and our private registry URI.
- For each tag of an image, the script will download it one by one and try to push it to our private ECR registry.

## What `config.json` is
[config.json](config.json) is configuration file where we store the:
- name of image we want to download, this is stored in a json file with key `image_name`
- list of tags of a specific image we want to download, this is stored in a json file with key `image_tags`
- external or 3rd party registry url or the source of the container images:
  - If it is not docker hub, you need to specify the full path, from registry name to the image names, example: `gcr.io/distroless/java-debian10`
  - if it is from docker hub, you can just specify the container image name, example: `datadog/agent`
  - this is stored in a json file with key `external_registry_url`
- internal registry url or our private url, this should be a full uri of the ECR repo with format `<account-id>.dkr.ecr.<region>.amazonaws.com/<repositorry-name>`