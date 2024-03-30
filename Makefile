playbook   ?= playbooks/main
env        ?= environments/prod

.PHONY: prereq
prereq: ## Install any pre-req roles and collections
	ansible-galaxy collection install -r collections/requirements.yml
	ansible-galaxy role install -r roles/requirements.yml

.PHONY: deploy
deploy: ## Run the main.yaml playbook against the inventory
	@env=$(env) ansible-playbook --inventory-file="$(env)" --diff "$(playbook).yaml" $(ARGS)

.PHONY: ping
ping: ## Ping all hosts in the inventory file
	@env=$(env) ansible -i $(env) -m ping all

.PHONY: lint
lint: ## lint the ansible playbooks
	ansible-lint

.PHONY: build-container
build-container: ## Build the docker container version of the playbook
	docker build .
