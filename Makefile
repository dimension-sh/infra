PHONY: prereqs
prereqs:
	uv run ansible-galaxy install -r requirements.yml

PHONY: lint
lint: prereqs
	uv run ansible-lint

PHONY: deploy
deploy: prereqs
	uv run ansible-playbook -i environments/prod playbooks/main.yaml --vault-password-file .pass --diff $(extra_args)
