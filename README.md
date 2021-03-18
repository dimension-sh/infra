# infra

A collection Ansible playbooks and roles to manage the [dimension.sh](https://dimension.sh)
infrastructure and system configuration.

## Playbooks

* `main.yaml` - Run everything playbook.
* `www.yaml` - Run web roles.
* `bootstrap.yaml` - Run initial bootstrapping for new servers.

## Base Roles

* `cis` - Applies a subset of the CIS Security Baseline
* `common` - Common to all nodes, mostly Repos and MOTD
* `dovecot` - Simple Dovecot install and configuration
* `efingerd` - Setup Efingerd package and scripts
* `gopher` - Installs and configures a Gophernicus server
* `news` - Installs the dimension basic news system
* `postfix` - Postfix configuration and installation
* `www` - Nginix and the website

## Meta Roles

* `build` - Configures a build VM.
* `shell` - Configures a shell VM.
