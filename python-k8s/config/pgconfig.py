from os import environ

K8S_NAMESPACE = environ.get("K8S_NAMESPACE", "test")

INGRESS_NAME = environ.get("INGRESS_NAME", "hello-ingress")
DOWNSTREAM_SERVICE = environ.get("DOWNSTREAM_SERVICE", "hello-shadow-service")
NGINX_MIRROR_CONFIG = "nginx-mirror.yaml"

DEPLOYEMNT_NAME = "hello-app-deployment"
IMAGE_V2 = "gcr.io/google-samples/hello-app:1.0"
