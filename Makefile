-include .env
export

lint:
	make lint/callable build_target=gov_uk_search
	make lint/callable build_target=gov_uk_acronyms
	make lint/callable build_target=wikipedia

lint/callable:
	cd src/${build_target}/ && make lint

build_artifacts/ci:
	mkdir -p -- build out build/layers build/packages
	make build/callable build_target=gov_uk_search
	make build/callable build_target=gov_uk_acronyms
	make build/callable build_target=wikipedia

build_artifacts/local:
	docker run --rm -v "${PWD}:/var/task" -w /var/task --platform linux/amd64 python:3.12 \
		sh -c "pip install uv && make build_artifacts/ci"

build/callable:
	cd src/${build_target}/ && make build

## Terraform 
workspace = $(env)
tf_build_args = -var-file="./variables/global.tfvars" -var-file="./variables/$(env).tfvars"
TF_BACKEND_CONFIG=backend.hcl

tf_set_workspace:
	terraform -chdir=terraform/${instance} workspace select $(workspace)

tf_new_workspace:
	terraform -chdir=terraform/${instance} workspace new $(workspace)

tf_set_or_create_workspace:
	make tf_set_workspace || make tf_new_workspace

tf_init_and_set_workspace:
	make tf_init && make tf_set_or_create_workspace

.PHONY: tf_init
tf_init:
	terraform -chdir=./terraform/${instance} init \
		-backend-config=$(TF_BACKEND_CONFIG) \
		-backend-config="dynamodb_table=i-dot-ai-$(env)-dynamo-lock" \
		-reconfigure

.PHONY: tf_fmt
tf_fmt:
	terraform fmt

.PHONY: tf_plan
tf_plan:
	make tf_init_and_set_workspace && \
	terraform -chdir=./terraform/${instance} plan ${tf_build_args} ${args}

.PHONY: tf_apply
tf_apply:
	make tf_init_and_set_workspace && \
	terraform -chdir=./terraform/${instance} apply ${tf_build_args} ${args}

.PHONY: tf_destroy
tf_destroy: 
	make tf_init_and_set_workspace && \
	terraform -chdir=./terraform/${instance} destroy ${tf_build_args} ${args}

.PHONY: tf_auto_apply
tf_auto_apply:
	if [ ${instance} == "infra" ]; then make check_docker_tag_exists repo=$(ECR_REPO_NAME); fi
	make tf_init_and_set_workspace && \
	terraform -chdir=./terraform/${instance} apply ${tf_build_args} ${args} -auto-approve

.PHONY: release
release: 
	chmod +x ./release.sh && ./release.sh $(env)

.PHONY: docker_update_tag
docker_update_tag: # dummy setting
	@:
