.PHONY: build
build: ## Builds all FPF containers.
	DOCKER_CONTENT_TRUST=1 \
		ansible-playbook -vv --diff playbook.yml
