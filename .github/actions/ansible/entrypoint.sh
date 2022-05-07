#!/bin/bash -x

# Write out vault pass
echo "$VAULT_PASS" > ~/.vault_pass.txt

# Setup SSH
mkdir ~/.ssh
echo "$SSH_KEY" > ~/.ssh/id_rsa
chmod 0600 ~/.ssh/id_rsa

# Output version
ansible --version

# Install deps
ansible-galaxy collection install -r collections/requirements.yml
ansible-galaxy role install -r roles/requirements.yaml

# Run playbook
ansible-playbook --vault-password-file ~/.vault_pass.txt -u "$SSH_USER" -i inventory.yaml -l "$TARGET_HOST" --check main.yaml
