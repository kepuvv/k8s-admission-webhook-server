# Simply webhook server for Kubernetes Dynamic Admission Control

Small Flask-based Kubernetes admission webhook example that provides a mutate and validate endpoint for Pods.

Kubernetes documentation: [Dynamic Admission Control](https://kubernetes.io/docs/reference/access-authn-authz/extensible-admission-controllers)

Quick start

- Run latest version from Docker Hub:

  `docker run -d -p 5001:5001 kepuvv/kube-admission-webhook-server:latest`

Local build:

- Build:

  `docker build -t kube-admission-webhook-server:local .`

- Run:

  `docker run -p 5001:5001 kube-admission-webhook-server:local`

- Test `/validate` with curl (example):

  ```
  curl -X POST http://127.0.0.1:5001/validate \
    -H "Content-Type: application/json" \
    -d '{"request": {"uid": "1234", "object": {"metadata": {"name": "test-pod"}, "spec": {"containers": [{"name": "app", "image": "nginx", "resources": {"requests": {"cpu": "100m","memory": "128Mi"},"limits": {"cpu": "200m","memory": "256Mi"}}}]}}}}'
  ```

Requirements:

- Python 3.12
