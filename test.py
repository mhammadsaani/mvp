from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from kubernetes import client, config
import boto3
import os
import datetime

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def read_index():
    with open("./templates/index.html", "r") as f:
        content = f.read()
    return HTMLResponse(content=content)

# Store AWS credentials temporarily
aws_credentials = None

@app.post("/set-aws-credentials")
async def set_aws_credentials(credentials: dict):
    global aws_credentials

    # Get AWS credentials from the request
    aws_access_key_id = credentials.get("access_key_id")
    aws_secret_access_key = credentials.get("secret_access_key")
    aws_region = credentials.get("region")

    try:
        # Set up AWS session with provided credentials
        session = boto3.Session(
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=aws_region
        )
        
        # Get temporary credentials to interact with EKS
        global aws_credentials
        aws_credentials = session.get_credentials()
        
        # Return success if AWS credentials are set correctly
        return JSONResponse(content={"success": True})
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})

@app.get("/namespaces")
async def get_namespaces():
    if not aws_credentials:
        return JSONResponse(status_code=400, content={"message": "AWS credentials not set."})

    try:
        # Set up Kubernetes client with the AWS credentials
        session = boto3.Session(
            aws_access_key_id=aws_credentials.access_key,
            aws_secret_access_key=aws_credentials.secret_key,
            region_name="us-east-1"  # You can pass this dynamically if needed
        )

        # Get the EKS token
        eks_token = aws_credentials.get_frozen_credentials().token

        # Setup Kubernetes client configuration
        k8s_client = config.new_client_from_config()
        k8s_client.configuration.api_key['authorization'] = f"Bearer {eks_token}"

        # Get Kubernetes API instance
        api = client.CoreV1Api(k8s_client)
        namespaces = api.list_namespace()

        return JSONResponse(content={"namespaces": [ns.metadata.name for ns in namespaces.items]})
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})
    
    
import subprocess
@app.get("/pods/{namespace}")
async def get_pods(namespace: str):
    if not aws_credentials:
        return JSONResponse(status_code=400, content={"message": "AWS credentials not set."})

    try:
        # Set up Kubernetes client with the AWS credentials
        session = boto3.Session(
            aws_access_key_id=aws_credentials.access_key,
            aws_secret_access_key=aws_credentials.secret_key,
            region_name="us-east-1"  # You can pass this dynamically if needed
        )

        # Get the EKS token
        eks_token = aws_credentials.get_frozen_credentials().token

        # Setup Kubernetes client configuration
        k8s_client = config.new_client_from_config()
        k8s_client.configuration.api_key['authorization'] = f"Bearer {eks_token}"

        # Get Kubernetes API instance
        api = client.CoreV1Api(k8s_client)
        pods = api.list_namespaced_pod(namespace)

        return JSONResponse(content={"pods": [pod.metadata.name for pod in pods.items]})
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})

def check_kubectl():
    try:
        # Run 'kubectl version' to verify kubectl is installed and configured correctly
        result = subprocess.run(["kubectl", "version", "--short"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print("kubectl is present")
        if result.returncode != 0:
            raise Exception(f"Error with kubectl: {result.stderr}")
        return True
    except Exception as e:
        raise Exception(f"kubectl is not installed or not configured correctly: {str(e)}")
from fastapi import FastAPI
from fastapi.responses import JSONResponse, FileResponse
import subprocess
import os
import re
from datetime import datetime, timedelta


@app.get("/logs/{namespace}/{pod}")
async def get_filtered_logs(namespace: str, pod: str):
    try:
        # Step 1: Dump full logs with timestamps using kubectl
        full_logs_cmd = ["kubectl", "logs", pod, "-n", namespace, "--timestamps"]
        result = subprocess.run(full_logs_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        if result.returncode != 0:
            return JSONResponse(
                status_code=500,
                content={"message": "Error fetching logs", "error": result.stderr.strip()}
            )

        all_logs = result.stdout.splitlines()

        # Step 2: Compute the cutoff time (26h15m ago in ISO 8601 format)
        cutoff_time = (datetime.utcnow() - timedelta(hours=26, minutes=15)).strftime("%Y-%m-%dT%H:%M:%S")

        # Step 3: Filter logs by timestamp
        iso8601_pattern = re.compile(r'^(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})')

        filtered_logs = [
            line for line in all_logs
            if (match := iso8601_pattern.match(line)) and match.group(1) >= cutoff_time
        ]

        # Step 4: Save filtered logs to file
        os.makedirs("logs", exist_ok=True)
        filename = f"{pod}_{namespace}_filtered.log"
        filepath = os.path.join("logs", filename)

        with open(filepath, "w") as f:
            f.write("\n".join(filtered_logs))

        return FileResponse(filepath, filename=filename)

    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})
