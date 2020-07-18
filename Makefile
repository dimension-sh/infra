.DEFAULT_GOAL := help

playbook   ?= main
env        ?= inventory.yaml

.PHONY: help
help:
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
	| sed -n 's/^\(.*\): \(.*\)##\(.*\)/\1\3/p' \
	| column -t  -s ' '

.PHONY: deploy
deploy: ## Run the main.yaml playbook against the inventory
	@env=$(env) ansible-playbook --inventory-file="$(env)" --diff "$(playbook).yaml" -K -u $(shell whoami)

.PHONY: ping
ping: ## Ping all hosts in the inventory file
	@env=$(env) ansible -i $(env) -m ping all

.PHONY: lint
lint: ## make lint [playbook=setup] [env=hosts] [args=<ansible-playbook arguments>] # Check syntax of a playbook
	@env=$(env) ansible-playbook --inventory-file="$(env)" --syntax-check "$(playbook).yaml"
