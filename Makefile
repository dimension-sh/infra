.DEFAULT_GOAL := help
.PHONY: help

help:
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
	| sed -n 's/^\(.*\): \(.*\)##\(.*\)/\1\3/p' \
	| column -t  -s ' '

deploy: ## Run the main.yaml playbook against the inventory
	ansible-playbook -i ./inventory main.yaml -K -u $(shell whoami)

ping: ## Ping all hosts in the inventory file
	ansible -i ./inventory -m ping all