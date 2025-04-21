# Important Commands Used During the API Escape Room Challenge

This document contains the most significant commands used during the implementation of the API and Kubernetes integration challenge, with explanations of their purpose.

## API Script Development

```bash
# Create Python script for API calls
vim api_script.py

# Test the script locally with proper credentials
python3 api_script.py

# Create Dockerfile
vim Dockerfile

# Create requirements file for Python dependencies
echo "requests==2.28.2" > requirements.txt

# Build Docker image
docker build -t api-script:latest .

# Verify image was created
docker images | grep api-script


# Install kind (Kubernetes IN Docker)
curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.20.0/kind-linux-amd64
chmod +x ./kind
sudo mv ./kind /usr/local/bin/

# Create a Kubernetes cluster
kind create cluster --name api-escape-room

# Load Docker image into kind
kind load docker-image api-script:latest --name api-escape-room

# Create Kubernetes manifests
vim api-credentials-secret.yaml
vim api-data-pvc.yaml
vim api-job.yaml

# Apply Kubernetes resources
kubectl apply -f api-credentials-secret.yaml
kubectl apply -f api-data-pvc.yaml
kubectl apply -f api-job.yaml

# Monitor Kubernetes resources
kubectl get pods
kubectl get jobs
kubectl logs $(kubectl get pods --selector=job-name=api-job -o jsonpath='{.items[0].metadata.name}')

# Create a directory for output data
mkdir -p output

# Create a pod to access data
kubectl apply -f - <<EOF
apiVersion: v1
kind: Pod
metadata:
  name: data-access-pod
spec:
  containers:
  - name: data-access
    image: busybox
    command: ["sleep", "3600"]
    volumeMounts:
    - name: data-volume
      mountPath: /data
  volumes:
  - name: data-volume
    persistentVolumeClaim:
      claimName: api-data-pvc
EOF

# Copy data from the pod
kubectl cp data-access-pod:/data/compliance_data.csv ./output/compliance_data.csv

# View the CSV data
cat ./output/compliance_data.csv


# Initialize Git repository
git init

# Add files to Git
git add api_script.py Dockerfile requirements.txt api-job.yaml api-credentials-secret.yaml api-data-pvc.yaml README.md output/compliance_data.csv

# Commit changes
git commit -m "Initial commit: API and Kubernetes integration project"

# Add remote repository
git remote add origin https://github.com/la-belle-femme/api-escape-room-project.git

# Push to GitHub
git push -u origin main




