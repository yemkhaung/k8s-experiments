import os

K8S_CONTEXT = os.environ.get("K8S_CONTEXT", "docker-desktop")
K8S_NAMESPACE = os.environ.get("K8S_NAMESPACE", "test")

INGRESS_NAME = os.environ.get("INGRESS_NAME", "sample-ingress")
DOWNSTREAM_SERVICE = "sample-shadow-service"
NGINX_MIRROR_ANNOTATION = {
    "nginx.org/location-snippets": "mirror  /mirror;\n",
    "nginx.org/server-snippets": 'resolver kube-dns.kube-system valid=10s;\n\
        location = /mirror {\n    \
        internal;\n    set $shadow_service_name "{DOWNSTREAM_SERVICE}";\n    \
        proxy_set_header X-Mirror-Request  true;\n    \
        proxy_set_header X-Shadow-Service  \
        $shadow_service_name;\n    \
        proxy_set_header X-Real-IP  \
        $remote_addr;\n    \
        proxy_set_header X-Forwarded-For  \
        $proxy_add_x_forwarded_for;\n    \
        proxy_set_header Host  $host;\n    \
        proxy_pass http://{DOWNSTREAM_SERVICE}$request_uri;\n}\n',
}

DEPLOYEMNT_NAME = "hello-app-deployment"
IMAGE_V2 = "gcr.io/google-samples/hello-app:1.0"
