import traceback
from kubernetes import client, config
from config.pgconfig import (
    K8S_CONTEXT,
    K8S_NAMESPACE,
    DEPLOYEMNT_NAME,
    IMAGE_V2,
    INGRESS_NAME,
    NGINX_MIRROR_ANNOTATION,
)


class K8sController:
    """
    Calling k8s API with python client

    For process to be run in k8s cluster, use load_incluster_config()

    For client-side, e.g local machine. use load_kube_config() to read k8s
    configuration from local `.kube` path
    """

    def __init__(self, context=K8S_CONTEXT, namespace=K8S_NAMESPACE):
        self.ns = namespace
        self.ctx = context

        # config.load_kube_config(context=self.ctx)
        # print(f"Selected context: {self.ctx}")
        config.load_incluster_config()

        self.app_api = client.AppsV1Api()
        self.core_api = client.CoreV1Api()
        self.net_api = client.NetworkingV1beta1Api()

    def update_deployemnt(self, name):
        print(f"Finding deployment:{name} in [{self.ns}] namespace...")
        res = self.app_api.list_namespaced_deployment(self.ns)
        for item in res.items:
            print(
                f"NAME:{item.metadata.name}, READY: {item.status.ready_replicas}/{item.status.available_replicas}"
            )
            if item.metadata.name == name:
                print(
                    f"Found target resource. name={item.metadata.name}. Updating deployment..."
                )
                item.spec.template.spec.containers[0].image = IMAGE_V2
                res = self.app_api.patch_namespaced_deployment(
                    name=name, namespace=self.ns, body=item
                )
                print(
                    f"Deployment updated. status={res.status.ready_replicas}/{res.status.available_replicas}"
                )
                return

    def update_ingress(self, name):
        print(f"Finding ingress:{name} in [{self.ns}] namespace...")
        res = self.net_api.list_namespaced_ingress(self.ns)
        for item in res.items:
            print(f"NAME:{item.metadata.name}, HOSTS:{item.spec.rules}")
            if item.metadata.name == name:
                print(
                    f"Found target resource. name={item.metadata.name}. Updating ingress ..."
                )
                # item.metadata.annotations = {"nginx.org/location-snippets": "", "nginx.org/server-snippets": ""}
                item.metadata.annotations = NGINX_MIRROR_ANNOTATION
                res = self.net_api.patch_namespaced_ingress(
                    name=name, namespace=self.ns, body=item
                )
                print(f"Ingress updated. {res.status}")
                return

    def run(self):
        self.update_deployemnt(DEPLOYEMNT_NAME)
        self.update_ingress(INGRESS_NAME)


if __name__ == "__main__":
    try:
        kctrl = K8sController()
        kctrl.run()
    except Exception as e:
        print(f"Error occurred. {e}")
        print(traceback.format_exc())
