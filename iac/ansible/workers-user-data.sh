#!/bin/bash

# Set hostname
hostnamectl set-hostname k8s-worker-temp-hostname

# Update package list
apt update

# Disable SWAP
swapoff -a
sed -i '/ swap / s/^/#/' /etc/fstab

# Load required kernel modules
echo "overlay" > /etc/modules-load.d/k8s.conf
echo "br_netfilter" >> /etc/modules-load.d/k8s.conf
modprobe overlay
modprobe br_netfilter

# Configure network settings
cat <<SYSCTL | tee /etc/sysctl.d/k8s.conf
net.bridge.bridge-nf-call-iptables  = 1
net.bridge.bridge-nf-call-ip6tables = 1
net.ipv4.ip_forward                 = 1
SYSCTL

# Apply network settings
sysctl --system

# Install and configure containerd
apt install -y containerd
mkdir -p /etc/containerd
containerd config default | tee /etc/containerd/config.toml
sed -i 's/SystemdCgroup = false/SystemdCgroup = true/' /etc/containerd/config.toml

# Restart containerd
systemctl restart containerd
systemctl enable containerd

# Install prerequisites for K8s repository
apt install -y apt-transport-https ca-certificates curl gpg

# Get latest Kubernetes version
KUBE_VERSION=$(curl -s https://api.github.com/repos/kubernetes/kubernetes/releases/latest | grep tag_name | cut -d '"' -f 4 | cut -d 'v' -f 2 | cut -d '.' -f 1,2)

# Download GPG key
curl -fsSL https://pkgs.k8s.io/core:/stable:/v$${KUBE_VERSION}/deb/Release.key | gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg

# Add K8s repository
echo "deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v$${KUBE_VERSION}/deb/ /" | tee /etc/apt/sources.list.d/kubernetes.list
apt update

# Install Kubernetes tools
apt install -y kubelet kubeadm kubectl

# Hold Kubernetes packages
apt-mark hold kubelet kubeadm kubectl