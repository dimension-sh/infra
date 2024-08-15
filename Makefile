.venv:
	virtualenv .venv
	.venv/bin/pip3 install poetry

PHONY: prereqs
prereqs: .venv
	.venv/bin/python3 -m poetry install --no-root
	.venv/bin/python3 -m poetry run ansible-galaxy install -r requirements.yml

PHONY: lint
lint: prereqs
	.venv/bin/python3 -m poetry run ansible-lint

PHONY: deploy
deploy: prereqs
	.venv/bin/python3 -m poetry run ansible-playbook -i environments/prod playbooks/main.yaml --vault-password-file .pass --diff $(extra_args)
