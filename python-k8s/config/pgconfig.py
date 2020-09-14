import yaml
from os import path, environ

K8S_CONTEXT = environ.get("K8S_CONTEXT", "docker-desktop")
K8S_NAMESPACE = environ.get("K8S_NAMESPACE", "test")

INGRESS_NAME = environ.get("INGRESS_NAME", "hello-ingress")
DOWNSTREAM_SERVICE = "hello-shadow-service"
with open(path.join(path.dirname(__file__), "nginx-mirror.yaml")) as f:
    conf = yaml.safe_load(f)
    NGINX_MIRROR_ANNOTATION = conf

DEPLOYEMNT_NAME = "hello-app-deployment"
IMAGE_V2 = "gcr.io/google-samples/hello-app:1.0"
