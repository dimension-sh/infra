#!/bin/bash

ansible-playbook -i ./inventory main.yaml -K -u $(whoami)