import os
import traceback
from kubernetes import client, config
from config.pconfig import (
    K8S_CONTEXT,
    K8S_NAMESPACE,
    INGRESS_NAME,
    NGINX_MIRROR_ANNOTATION
)

"""
GOAL:
List ingress resources and update the target ingress
(with specified label) with configurations
"""
class K8sController:
    def __init__(self, context=K8S_CONTEXT, namespace=K8S_NAMESPACE):
        self.ns = namespace
        self.ctx = context

        # load kube config
        config.load_kube_config(context=self.ctx)
        print(f"Selected context: {self.ctx}")

        self.app_api = client.AppsV1Api()
        self.core_api = client.CoreV1Api()
        self.net_api = client.NetworkingV1beta1Api()

    def update_nginx_mirror_config(self, name, ingress):
        print(f"Updating config of [{name}]...")
        ingress.metadata.annotations = {}  # NGINX_MIRROR_ANNOTATION
        res = self.net_api.patch_namespaced_ingress(
            name=name, namespace=self.ns, body=ingress)
        print(f"Ingress updated. status={res.status}")

    def run(self):
        print(f"Listing ingress from [{self.ns}] namespace...")
        res = self.net_api.list_namespaced_ingress(self.ns)
        for item in res.items:
            if(item.metadata.name == INGRESS_NAME):
                print(
                    f"Found target ingress. name={item.metadata.name}, host={item.spec.rules[0].host}")
                self.update_nginx_mirror_config(
                    name=INGRESS_NAME, ingress=item)
                break


if __name__ == "__main__":
    try:
        kctrl = K8sController()
        kctrl.run()
    except Exception as e:
        print(f"Error occurred. {e}")
        print(traceback.format_exc())
