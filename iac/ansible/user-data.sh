- name: Install Kubernetes prerequisites
  hosts: all
  become: yes
  vars:
    kubernetes_version: "1.29.2-00"
    pod_network_cidr: "10.244.0.0/16"
  tasks:
    - name: Ensure apt cache is updated
      apt:
        update_cache: yes
        cache_valid_time: 3600

    - name: Install required packages (base)
      apt:
        name:
          - apt-transport-https
          - ca-certificates
          - curl
          - gnupg
          - containerd
        state: present

    - name: Create keyrings directory
      file:
        path: /etc/apt/keyrings
        state: directory
        mode: '0755'

    - name: Remove existing Kubernetes repository if present
      file:
        path: /etc/apt/sources.list.d/kubernetes.list
        state: absent

    - name: Remove existing GPG key if present
      file:
        path: /etc/apt/keyrings/kubernetes-apt-keyring.gpg
        state: absent

    - name: Download and import Kubernetes GPG key
      shell: |
        curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.29/deb/Release.key | gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg
        chmod 644 /etc/apt/keyrings/kubernetes-apt-keyring.gpg

    - name: Add Kubernetes repository
      copy:
        content: "deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.29/deb/ /\n"
        dest: /etc/apt/sources.list.d/kubernetes.list
        mode: '0644'


    - name: Update apt cache after adding Kubernetes repo
      apt:
        update_cache: yes
        cache_valid_time: 0

    - name: Install Kubernetes packages (latest from repo)
      apt:
        name:
          - kubelet
          - kubeadm
          - kubectl
        state: present
        update_cache: yes

    - name: Hold kube packages at current version
      shell: apt-mark hold kubelet kubeadm kubectl

    - name: Enable and start containerd
      systemd:
        name: containerd
        enabled: yes
        state: started

- name: Initialize control-plane node
  hosts: control_plane
  become: yes
  vars:
    kubernetes_version: "1.29.2-00"
    pod_network_cidr: "10.244.0.0/16"
  tasks:
    - name: Load br_netfilter module
      modprobe:
        name: br_netfilter
        state: present

    - name: Ensure br_netfilter loads at boot
      lineinfile:
        path: /etc/modules-load.d/k8s.conf
        line: br_netfilter
        create: yes

    - name: Configure kernel parameters for Kubernetes
      shell: |
        echo 'net.bridge.bridge-nf-call-iptables = 1' >> /etc/sysctl.d/k8s.conf
        echo 'net.ipv4.ip_forward = 1' >> /etc/sysctl.d/k8s.conf
        sysctl --system

    - name: Initialize Kubernetes control plane
      command: kubeadm init --pod-network-cidr={{ pod_network_cidr }} --ignore-preflight-errors=Mem
      args:
        creates: /etc/kubernetes/admin.conf

    - name: Configure kubeconfig for ubuntu user
      command: "{{ item }}"
      with_items:
        - mkdir -p /home/ubuntu/.kube
        - cp -i /etc/kubernetes/admin.conf /home/ubuntu/.kube/config
        - chown ubuntu:ubuntu /home/ubuntu/.kube/config

    - name: Wait for Kubernetes API server to be ready
      shell: |
        timeout=180
        elapsed=0
        while [ $elapsed -lt $timeout ]; do
          if kubectl --kubeconfig=/etc/kubernetes/admin.conf get nodes 2>/dev/null; then
            echo "API server is ready"
            exit 0
          fi
          echo "Waiting for API server... ($elapsed/$timeout seconds)"
          sleep 5
          elapsed=$((elapsed + 5))
        done
        echo "API server did not become ready in time"
        exit 1
      register: api_wait
      failed_when: api_wait.rc != 0

    - name: Generate join command file
      shell: |
        sleep 15
        for i in {1..5}; do
          if cmd=$(kubeadm token create --print-join-command 2>/dev/null); then
            echo "$cmd"
            exit 0
          fi
          echo "Attempt $i failed, retrying in 10 seconds..."
          sleep 10
        done
        echo "Failed to create join token after 5 attempts"
        exit 1
      register: join_cmd
      changed_when: false

    - name: Save join command locally
      copy:
        content: "{{ join_cmd.stdout }} --cri-socket unix:///var/run/containerd/containerd.sock"
        dest: /home/ubuntu/join-command.sh
        mode: "0700"
