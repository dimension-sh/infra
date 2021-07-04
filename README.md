# infra

A collection Ansible playbooks and roles to manage the [dimension.sh](https://dimension.sh)
infrastructure and system configuration.

## Playbooks

* `main.yaml` - Run everything playbook.
* `www.yaml` - Run web roles.
* `bootstrap.yaml` - Run initial bootstrapping for new servers.

## Base Roles

* `borgmatic` - Installs and configures Borg and Borgmatic.
* `certbot` - Certbot setup for easy TLS certs.
* `cis` - Applies a subset of the CIS Security Baseline
* `common` - Common to all nodes, mostly Repos and MOTD
* `dovecot` - Simple Dovecot install and configuration
* `efingerd` - Setup Efingerd package and scripts
* `gemini` - Installs and configures a Gemini server using Molly-Brown
* `gopher` - Installs and configures a Gophernicus server
* `news` - Installs the dimension basic news system
* `postfix` - Postfix configuration and installation
* `shell` - The Dimension Shell(tm)
* `www` - Nginix and the website

## Meta Roles

* `build` - Build VMs - For build tasks and bigger work.
* `dev` - Development VMs.
* `mail` - VMs that run mail services.
* `services` - VMs for running bigger services on.
* `shell` - Shell VMs - End user accessible
