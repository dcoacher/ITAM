#!/bin/bash
hostnamectl set-hostname k8s-controller
add-apt-repository universe -y
apt update
apt install -y ansible python3 python3-pip python3-venv git
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
mkdir -p /home/ubuntu/ansible
chown ubuntu:ubuntu /home/ubuntu/ansible
chmod 755 /home/ubuntu/ansible
cat <<'EOF' >/home/ubuntu/ansible/ansible.cfg
[defaults]
inventory = inventory.ini
remote_user = ubuntu
private_key_file = ~/KP.pem
host_key_checking = False
retry_files_enabled = False
deprecation_warnings = False
[ssh_connection]
pipelining = True
EOF
cat <<EOF >/home/ubuntu/ansible/inventory.ini
[control_plane]
control-plane ansible_host="10.0.1.10"
[workers]
worker-1 ansible_host="10.0.1.11"
worker-2 ansible_host="10.0.2.11"
[all:vars]
ansible_python_interpreter=/usr/bin/python3
EOF
cat <<'EOF' >/home/ubuntu/ansible/k8s.yml
- name: Install Kubernetes prerequisites
  hosts: all
  become: yes
  vars:
    pod_network_cidr: "10.244.0.0/16"
  tasks:
    - apt: update_cache=yes cache_valid_time=3600
    - apt: name={{item}} state=present
      with_items: [apt-transport-https,ca-certificates,curl,gnupg,containerd]
    - file: path=/etc/apt/keyrings state=directory mode=0755
    - file: path=/etc/apt/sources.list.d/kubernetes.list state=absent
    - file: path=/etc/apt/keyrings/kubernetes-apt-keyring.gpg state=absent
    - shell: curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.29/deb/Release.key | gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg && chmod 644 /etc/apt/keyrings/kubernetes-apt-keyring.gpg
    - copy: content="deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.29/deb/ /\n" dest=/etc/apt/sources.list.d/kubernetes.list mode=0644
    - apt: update_cache=yes cache_valid_time=0
    - apt: name={{item}} state=present update_cache=yes
      with_items: [kubelet,kubeadm,kubectl]
    - shell: apt-mark hold kubelet kubeadm kubectl
    - systemd: name=containerd enabled=yes state=started
    - modprobe: name=br_netfilter state=present
    - lineinfile: path=/etc/modules-load.d/k8s.conf line=br_netfilter create=yes
    - shell: |
        grep -q "net.bridge.bridge-nf-call-iptables" /etc/sysctl.d/k8s.conf || echo 'net.bridge.bridge-nf-call-iptables = 1' >> /etc/sysctl.d/k8s.conf
        grep -q "net.ipv4.ip_forward" /etc/sysctl.d/k8s.conf || echo 'net.ipv4.ip_forward = 1' >> /etc/sysctl.d/k8s.conf
        sysctl --system
- name: Initialize control-plane node
  hosts: control_plane
  become: yes
  vars:
    pod_network_cidr: "10.244.0.0/16"
  tasks:
    - command: kubeadm init --pod-network-cidr={{ pod_network_cidr }} --ignore-preflight-errors=Mem --cri-socket unix:///var/run/containerd/containerd.sock
      args: creates=/etc/kubernetes/admin.conf
    - command: "{{ item }}"
      with_items: [mkdir -p /home/ubuntu/.kube,cp -i /etc/kubernetes/admin.conf /home/ubuntu/.kube/config,chown ubuntu:ubuntu /home/ubuntu/.kube/config]
    - shell: |
        timeout=300;elapsed=0
        while [ $elapsed -lt $timeout ]; do
          kubectl --kubeconfig=/etc/kubernetes/admin.conf get nodes 2>/dev/null && exit 0
          sleep 10;elapsed=$((elapsed+10))
        done
        exit 1
      register: api_wait
      failed_when: api_wait.rc != 0
    - shell: |
        sleep 30
        for i in {1..10}; do
          cmd=$(kubeadm token create --print-join-command 2>/dev/null) && echo "$cmd" && exit 0
          sleep 15
        done
        exit 1
      register: join_cmd
      changed_when: false
    - copy: content="{{ join_cmd.stdout }} --cri-socket unix:///var/run/containerd/containerd.sock" dest=/home/ubuntu/join-command.sh mode=0700
    - shell: kubectl apply -f https://github.com/flannel-io/flannel/releases/latest/download/kube-flannel.yml
      args: creates=/tmp/flannel-installed
      register: flannel_install
      changed_when: flannel_install.rc == 0
    - shell: |
        sleep 30
        timeout=300;elapsed=0
        while [ $elapsed -lt $timeout ]; do
          flannel_ready=$(kubectl get pods -n kube-flannel --field-selector=status.phase=Running --no-headers 2>/dev/null | wc -l || echo "0")
          [ "$flannel_ready" -ge "1" ] && exit 0
          sleep 10;elapsed=$((elapsed+10))
        done
        exit 0
      register: flannel_wait
      failed_when: false
      when: flannel_install.rc == 0
    - shell: kubectl taint nodes --all node-role.kubernetes.io/control-plane- || true
      ignore_errors: yes
EOF
cat <<EOF >/home/ubuntu/ansible/nfs.yml
- name: Configure NFS server on control plane
  hosts: control_plane
  become: yes
  vars:
    nfs_export_dir: /srv/nfs/k8s
    nfs_clients_cidr: "10.0.0.0/16"
  tasks:
    - apt: name=nfs-kernel-server state=present
    - file: path={{ nfs_export_dir }} state=directory mode=0777
    - lineinfile: path=/etc/exports line="{{ nfs_export_dir }} {{ nfs_clients_cidr }}(rw,sync,no_subtree_check,no_root_squash)" create=yes
    - command: exportfs -ra
    - systemd: name=nfs-kernel-server enabled=yes state=restarted
- name: Configure NFS clients on workers
  hosts: workers
  become: yes
  vars:
    nfs_export_dir: /srv/nfs/k8s
    nfs_mount_dir: /mnt/nfs/k8s
    nfs_server_ip: "10.0.1.10"
  tasks:
    - apt: name=nfs-common state=present
    - file: path={{ nfs_mount_dir }} state=directory mode=0755
    - mount: path={{ nfs_mount_dir }} src={{ nfs_server_ip }}:{{ nfs_export_dir }} fstype=nfs opts=rw state=mounted
EOF
chown -R ubuntu:ubuntu /home/ubuntu/ansible
chmod 640 /home/ubuntu/ansible/*.yml /home/ubuntu/ansible/inventory.ini /home/ubuntu/ansible/ansible.cfg 2>/dev/null || true
mkdir -p /home/ubuntu/helm/templates
chown ubuntu:ubuntu /home/ubuntu/helm
chmod 755 /home/ubuntu/helm /home/ubuntu/helm/templates
cat <<'EOF' >/home/ubuntu/helm/Chart.yaml
apiVersion: v2
name: itam-app
description: ITAM Flask web application
type: application
version: 1.0.0
appVersion: "1.0"
EOF
cat <<'EOF' >/home/ubuntu/helm/values.yaml
replicaCount: 2
image:
  repository: docker.io/dcoacher/itam-app
  tag: "latest"
  pullPolicy: Always
service:
  type: NodePort
  port: 31415
  nodePort: 31415
persistence:
  enabled: true
  storageClass: "nfs-client"
  accessMode: ReadWriteMany
  size: 1Gi
  mountPath: /app/dummy-data
resources:
  requests:
    memory: "128Mi"
    cpu: "100m"
  limits:
    memory: "256Mi"
    cpu: "200m"
EOF
cat <<'EOF' >/home/ubuntu/helm/nfs-pv.yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: itam-nfs-pv
  labels:
    type: nfs
spec:
  capacity:
    storage: 10Gi
  accessModes:
    - ReadWriteMany
  persistentVolumeReclaimPolicy: Retain
  storageClassName: nfs-client
  nfs:
    path: /srv/nfs/k8s
    server: 10.0.1.10
---
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: nfs-client
provisioner: kubernetes.io/no-provisioner
volumeBindingMode: Immediate
EOF
cat <<'EOF' >/home/ubuntu/helm/templates/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ .Chart.Name }}
  labels:
    app: {{ .Chart.Name }}
spec:
  replicas: {{ .Values.replicaCount }}
  selector:
    matchLabels:
      app: {{ .Chart.Name }}
  template:
    metadata:
      labels:
        app: {{ .Chart.Name }}
    spec:
      tolerations:
      - key: node-role.kubernetes.io/control-plane
        operator: Exists
        effect: NoSchedule
      - key: node-role.kubernetes.io/master
        operator: Exists
        effect: NoSchedule
      containers:
      - name: {{ .Chart.Name }}
        image: {{ .Values.image.repository }}:{{ .Values.image.tag }}
        imagePullPolicy: {{ .Values.image.pullPolicy }}
        ports:
        - containerPort: {{ .Values.service.port }}
          name: http
        env:
        - name: ITAM_DATA_DIR
          value: {{ .Values.persistence.mountPath }}
        - name: PORT
          value: "{{ .Values.service.port }}"
        - name: FLASK_DEBUG
          value: "False"
        volumeMounts:
        - name: data
          mountPath: {{ .Values.persistence.mountPath }}
        resources:
          {{- toYaml .Values.resources | nindent 10 }}
      volumes:
      - name: data
        {{- if .Values.persistence.enabled }}
        persistentVolumeClaim:
          claimName: {{ .Chart.Name }}-pvc
        {{- end }}
EOF
cat <<'EOF' >/home/ubuntu/helm/templates/pvc.yaml
{{- if .Values.persistence.enabled }}
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: {{ .Chart.Name }}-pvc
  labels:
    app: {{ .Chart.Name }}
spec:
  accessModes:
    - {{ .Values.persistence.accessMode }}
  storageClassName: {{ .Values.persistence.storageClass }}
  resources:
    requests:
      storage: {{ .Values.persistence.size }}
{{- end }}
EOF
cat <<'EOF' >/home/ubuntu/helm/templates/service.yaml
apiVersion: v1
kind: Service
metadata:
  name: {{ .Chart.Name }}
  labels:
    app: {{ .Chart.Name }}
spec:
  type: {{ .Values.service.type }}
  ports:
  - port: {{ .Values.service.port }}
    targetPort: http
    protocol: TCP
    name: http
    {{- if eq .Values.service.type "NodePort" }}
    nodePort: {{ .Values.service.nodePort }}
    {{- end }}
  selector:
    app: {{ .Chart.Name }}
EOF
cat <<'EOF' >/home/ubuntu/helm/deploy.sh
#!/bin/bash
set -euo pipefail
echo "=== ITAM Application Deployment ==="
echo ""
echo "Step 1: Checking Kubernetes API server..."
MAX_WAIT=300
ELAPSED=0
while [ $ELAPSED -lt $MAX_WAIT ]; do
  if kubectl cluster-info &>/dev/null 2>&1 && kubectl get nodes &>/dev/null 2>&1; then
    echo "✓ API server is ready"
    break
  fi
  echo "Waiting... ($ELAPSED/$MAX_WAIT seconds)"
  sleep 10
  ELAPSED=$((ELAPSED + 10))
done
if ! kubectl cluster-info &>/dev/null 2>&1; then
  echo "ERROR: Cannot connect to Kubernetes API server"
  exit 1
fi
echo ""
echo "Step 2: Deploying NFS storage..."
kubectl apply -f nfs-pv.yaml
sleep 10
PV_STATUS=$(kubectl get pv itam-nfs-pv -o jsonpath='{.status.phase}' 2>/dev/null || echo "NotFound")
echo "PersistentVolume status: $PV_STATUS"
echo ""
echo "Step 3: Deploying application..."
if command -v helm &> /dev/null; then
  helm upgrade --install itam-app . --values values.yaml --timeout 5m --wait=false
else
  kubectl apply -f templates/pvc.yaml
  kubectl apply -f templates/deployment.yaml
  kubectl apply -f templates/service.yaml
fi
echo ""
echo "Step 4: Waiting for deployment..."
MAX_WAIT=600
ELAPSED=0
READY=false
while [ $ELAPSED -lt $MAX_WAIT ]; do
  if ! kubectl cluster-info &>/dev/null 2>&1; then
    echo "Warning: API server unreachable, retrying..."
    sleep 15
    ELAPSED=$((ELAPSED + 15))
    continue
  fi
  if kubectl wait --for=condition=available deployment/itam-app --timeout=15s &>/dev/null 2>&1; then
    READY=true
    break
  fi
  RUNNING=$(kubectl get pods -l app=itam-app --field-selector=status.phase=Running --no-headers 2>/dev/null | wc -l || echo "0")
  TOTAL=$(kubectl get pods -l app=itam-app --no-headers 2>/dev/null | wc -l || echo "0")
  if [ "$TOTAL" -gt 0 ]; then
    echo "Status: $RUNNING/$TOTAL pods running ($ELAPSED/$MAX_WAIT seconds)"
  else
    echo "Waiting for pods... ($ELAPSED/$MAX_WAIT seconds)"
  fi
  sleep 15
  ELAPSED=$((ELAPSED + 15))
done
echo ""
echo "=== Deployment Status ==="
kubectl get pods -l app=itam-app 2>/dev/null || echo "Could not retrieve pods"
echo ""
kubectl get svc itam-app 2>/dev/null || echo "Could not retrieve service"
echo ""
kubectl get pvc 2>/dev/null || echo "Could not retrieve PVC"
echo ""
if [ "$READY" = true ]; then
  echo "✓ Deployment completed successfully"
else
  echo "⚠ Deployment may still be in progress"
  echo "Check status with: kubectl get pods -l app=itam-app"
fi
echo ""
echo "To access the application:"
echo "  - NodePort: http://<node-ip>:31415"
echo "  - Get node IPs: kubectl get nodes -o wide"
EOF
chown -R ubuntu:ubuntu /home/ubuntu/helm
chmod 755 /home/ubuntu/helm /home/ubuntu/helm/deploy.sh
chmod 644 /home/ubuntu/helm/*.yaml /home/ubuntu/helm/Chart.yaml /home/ubuntu/helm/templates/*.yaml 2>/dev/null || true
