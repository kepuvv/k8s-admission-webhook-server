from flask import Flask, request, jsonify
import json
import base64

app = Flask(__name__)

@app.route('/mutate', methods=['POST'])
def mutate():
    request_info = request.get_json()
    pod = request_info['request']['object']
    uid = request_info['request']['uid']

    patch = []

    if 'metadata' in pod and 'labels' in pod['metadata']:
        labels = pod['metadata']['labels']
        if 'env' not in labels:
            patch.append({
                "op": "add",
                "path": "/metadata/labels/env",
                "value": "lab"
            })
    else:
        patch.append({
            "op": "add",
            "path": "/metadata/labels",
            "value": {"env": "lab"}
        })

    patch_str = json.dumps(patch)
    patch_base64 = base64.b64encode(patch_str.encode("utf-8")).decode("utf-8")

    admission_response = {
        "apiVersion": "admission.k8s.io/v1",
        "kind": "AdmissionReview",
        "response": {
            "uid": uid,
            "allowed": True,
            "patchType": "JSONPatch",
            "patch": patch_base64
        }
    }

    return jsonify(admission_response)

@app.route('/validate', methods=['POST'])
def validate():
    request_info = request.get_json()
    pod = request_info['request']['object']
    uid = request_info['request']['uid']

    is_allowed = False if pod.get('spec', {}).get('containers', []) else True
    reason = "All containers must have resource requests and limits defined."

    for container in pod.get('spec', {}).get('containers', []):
        if container.get('resources', {}).get('requests') and container.get('resources', {}).get('limits'):
            is_allowed = True
            break

    admission_response = {
        "apiVersion": "admission.k8s.io/v1",
        "kind": "AdmissionReview",
        "response": {
            "uid": uid,
            "allowed": is_allowed
        }
    }

    if not is_allowed:
        admission_response["response"]["status"] = {
            "code": 403,
            "message": reason
        }

    return jsonify(admission_response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
