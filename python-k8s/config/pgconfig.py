import yaml
from os import environ, path
from jinja2 import Template

K8S_NAMESPACE = environ.get("K8S_NAMESPACE", "test")
SERVICE_NAME = environ.get("SERVICE_NAME", "hello-service")
INGRESS_NAME = environ.get("INGRESS_NAME", "hello-ingress")
MIRROR_SERVICE = environ.get("MIRROR_SERVICE", "hello-mirror")
NGINX_MIRROR_CONFIG_PATH = "nginx-mirror.yaml"
# load mirror configurations yaml
with open(path.join("config", NGINX_MIRROR_CONFIG_PATH)) as yf:
    template = Template(yf.read())
NGINX_MIRROR_CONFIG = yaml.safe_load(
    template.render(
        namespace=K8S_NAMESPACE, service=SERVICE_NAME, mirror=MIRROR_SERVICE
    )
)
print(f"Mirror configuration loaded. {NGINX_MIRROR_CONFIG}")

DEPLOYEMNT_NAME = "hello-app-deployment"
IMAGE_V2 = "gcr.io/google-samples/hello-app:1.0"
