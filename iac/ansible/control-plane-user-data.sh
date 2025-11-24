#!/bin/bash

# Set hostname
hostnamectl set-hostname k8s-controller
add-apt-repository universe
apt update
apt install -y ansible python3 python3-pip python3-venv git

mkdir -p /etc/ansible


# Create Ansible hosts file (Inventory)
cat <<EOF > /etc/ansible/hosts

[app]
10.10.2.10
10.10.3.10

[app:vars]
ansible_user=ubuntu
ansible_python_interpreter=/usr/bin/python3
ansible_ssh_private_key_file=/home/ubuntu/KP.pem

[all:vars]
ansible_ssh_common_args=-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null

EOF

# Create ansible.cfg file
cat <<EOF > /etc/ansible/ansible.cfg



[defaults]
inventory = /etc/ansible/hosts

EOF

# Playbook Creation for Applications installation and Git repository cloning
cat > /home/ubuntu/playbook.yaml <<'YAML'
---
- hosts: all
  become: true
  tasks:
    - name: Update & install packages (apt)
      apt:
        update_cache: yes
        name:
          - git
          - python3-pip
          - python3-venv
          - python3-flask
        state: present

    - name: Clone repo if missing
      shell: test -d it-asset-management || git clone https://github.com/dcoacher/it-asset-management
      args:
        chdir: /home/ubuntu
      become_user: ubuntu

    - name: Create venv and install Flask
      shell: |
        python3 -m venv website/.venv
        website/.venv/bin/pip install -U pip Flask
      args:
        chdir: /home/ubuntu/it-asset-management

    - name: Start Flask (background)
      shell: |
        nohup /home/ubuntu/it-asset-management/website/.venv/bin/flask --app app run --host=0.0.0.0 --port=5000 \
          > /var/log/flask-asset.log 2>&1 &
      args:
        chdir: /home/ubuntu/it-asset-management/website
YAML

# Setting permissions for the playbook
chown ubuntu:ubuntu /home/ubuntu/playbook.yaml
chmod 0644 /home/ubuntu/playbook.yaml