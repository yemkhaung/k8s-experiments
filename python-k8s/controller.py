import traceback
from kubernetes import client, config
from config.pgconfig import (
    K8S_CONTEXT,
    K8S_NAMESPACE,
    DEPLOYEMNT_NAME,
    IMAGE_V2,
)


class K8sController:
    """
    CRUD k8s resources with python client
    """

    def __init__(self, context=K8S_CONTEXT, namespace=K8S_NAMESPACE):
        self.ns = namespace
        self.ctx = context

        # load kube config
        config.load_kube_config(context=self.ctx)
        print(f"Selected context: {self.ctx}")

        self.app_api = client.AppsV1Api()
        self.core_api = client.CoreV1Api()
        self.net_api = client.NetworkingV1beta1Api()

    def update(self, name, resource):
        print(f"Updating config of [{name}]...")
        resource.spec.template.spec.containers[0].image = IMAGE_V2
        res = self.app_api.patch_namespaced_deployment(
            name=name, namespace=self.ns, body=resource
        )
        print(f"Resource updated. status={res.status}")

    def run(self):
        print(f"Listing deployments from [{self.ns}] namespace...")
        res = self.app_api.list_namespaced_deployment(self.ns)
        for item in res.items:
            if item.metadata.name == DEPLOYEMNT_NAME:
                print(f"Found target resource. name={item.metadata.name},")
                self.update(name=DEPLOYEMNT_NAME, resource=item)
                return
        print("No deployment found.")


if __name__ == "__main__":
    try:
        kctrl = K8sController()
        kctrl.run()
    except Exception as e:
        print(f"Error occurred. {e}")
        print(traceback.format_exc())
