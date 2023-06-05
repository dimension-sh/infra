playbook   ?= playbooks/main
env        ?= environments/prod

.venv:
	virtualenv .venv
	.venv/bin/pip install -r requirements.txt

.PHONY: prereq
prereq: .venv
	.venv/bin/ansible-galaxy role install -r requirements.yml
	.venv/bin/ansible-galaxy collection install -r requirements.yml

.PHONY: deploy
deploy: .venv ## Run the main.yaml playbook against the inventory
	@env=$(env) .venv/bin/ansible-playbook --inventory-file="$(env)" --diff "$(playbook).yaml" $(ARGS)

.PHONY: ping
ping: .venv ## Ping all hosts in the inventory file
	@env=$(env) .venv/bin/ansible -i $(env) -m ping all

.PHONY: lint
lint: .venv ## make lint [playbook=setup] [env=hosts] [args=<ansible-playbook arguments>] # Check syntax of a playbook
	@env=$(env) .venv/bin/ansible-lint
