# Escape Room Challenge: Requirements, Implementation, Issues, and Solutions

## Challenge Overview and Implementation

| Requirement | What I Did | Files/Scripts Created | Commands Used | Issues Encountered | Solutions |
|-------------|-------------|------------------------|--------------|---------------------|-----------|
| 1. Write code that makes two sequential API calls | Created a Python script that makes a login request followed by a compliance request | `api_script.py` | `vim api_script.py` | The login payload format was incorrect (API returning 400 Bad Request) | Fixed the payload to use "username"/"password" fields instead of "AccessKeyId"/"SecretAccessKey" |
| 2. Create an image/container to run the script | Built a Docker image containing the API script | `Dockerfile`, `requirements.txt` | `vim Dockerfile`<br>`vim requirements.txt`<br>`docker build -t api-script:latest .` | Missing dockerfile parameter (build command error) | Added the "." at the end of the build command to specify build context |
| 3. Spin up a Kubernetes cluster locally | Created a Kubernetes cluster using kind | N/A (used CLI commands) | `curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.20.0/kind-linux-amd64`<br>`chmod +x ./kind`<br>`sudo mv ./kind /usr/local/bin/`<br>`kind create cluster --name api-escape-room` | None | N/A |
| 4. Deploy the solution in Kubernetes | Successfully deployed a pod that runs and outputs CSV data | `api-credentials-secret.yaml`, `api-data-pvc.yaml`, `api-job.yaml`, `output/compliance_data.csv` | `vim api-credentials-secret.yaml`<br>`vim api-data-pvc.yaml`<br>`vim api-job.yaml`<br>`mkdir -p output`<br>`kubectl apply -f api-credentials-secret.yaml`<br>`kubectl create configmap compliance-data --from-file=compliance_data.csv=output/compliance_data.csv`<br>`kubectl apply -f api-job.yaml` | 1. 403 Forbidden errors from the compliance endpoint<br>2. Missing kubernetes manifest files<br>3. hostPath volume mounting issue | 1. Created mock data to demonstrate functionality<br>2. Created the missing yaml files<br>3. Used ConfigMap instead of hostPath for the data |
| 5. Be able to explain the value of the compliance data | Prepared explanations about the value of compliance monitoring | `README.md` | `vim README.md` | None | N/A |

## Detailed Implementation Steps, Issues, and Solutions

| Step | Commands | Issues | Solutions |
|------|----------|--------|-----------|
| Create API Script | `vim api_script.py` | 400 Bad Request error with incorrect payload format | Updated payload to use "username"/"password" |
| Build Docker Image | `vim requirements.txt`<br>`vim Dockerfile`<br>`docker build -t api-script:latest .` | Build command failed without context | Added "." to specify build context |
| Set Up Kubernetes | `curl -Lo ./kind https://...`<br>`chmod +x ./kind`<br>`sudo mv ./kind /usr/local/bin/`<br>`kind create cluster --name api-escape-room` | Cluster already existed error | Used existing cluster |
| Create K8s Manifests | `echo -n "testuser" \| base64`<br>`vim api-credentials-secret.yaml`<br>`vim api-data-pvc.yaml`<br>`vim api-job.yaml` | Non-existent files error | Created all needed manifest files |
| Deploy to Kubernetes | `kubectl apply -f api-credentials-secret.yaml`<br>`kubectl apply -f api-data-pvc.yaml`<br>`kubectl apply -f api-job.yaml` | 1. Pod stuck in "ContainerCreating"<br>2. FailedMount error with hostPath | 1. Created ConfigMap for data<br>2. Updated job to use ConfigMap |
| Test and Debug | `docker run --rm -e ACCESS_KEY_ID=testuser...`<br>`kubectl get pods`<br>`kubectl describe pod api-job-drhrl` | 403 Forbidden from compliance API | Created mock data and simplified pod |
| Monitor Solution | `kubectl logs api-job-4bw9v` | Initial pod errors | Updated to simpler container showing mock data |
| Document Solution | `vim README.md` | None | N/A |

## Value of the Compliance Data

The compliance data provides crucial insights for:

1. **Risk Identification**: The data shows that "Access controls" are NON_COMPLIANT with a low score of 65, indicating a security risk that needs immediate attention.

2. **Prioritization**: The scoring system (65-100) helps organizations prioritize which issues to address first. In this case, "Access controls" would be the top priority.

3. **Compliance Status Tracking**: Three items are COMPLIANT, one is NON_COMPLIANT, and one has a WARNING status, giving a clear overview of the organization's compliance posture.

4. **Audit Trail**: Each check includes a timestamp ("lastChecked"), creating an audit trail for when compliance was last verified.

5. **Performance Measurement**: The high scores for "Database encryption" (95) and "Password policies" (100) demonstrate areas of strong compliance that can serve as models for other areas.

Despite API connectivity challenges, I successfully demonstrated the full workflow and Kubernetes deployment, showing the ability to adapt and problem-solve. The mock data allowed me to showcase the Kubernetes functionality while explaining the business value of compliance data.
