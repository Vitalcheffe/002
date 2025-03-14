import psutil
from kubernetes import client, config

class AutoScaler:
    def __init__(self):
        config.load_incluster_config()
        self.k8s_api = client.AppsV1Api()
        self.deployment_name = "deepstudy-ai"
        self.namespace = "default"

    async def monitor_and_scale(self):
        cpu_percent = psutil.cpu_percent()
        memory_percent = psutil.virtual_memory().percent

        if cpu_percent > 80 or memory_percent > 80:
            await self.scale_up()
        elif cpu_percent < 20 and memory_percent < 20:
            await self.scale_down()

    async def scale_up(self):
        """Augmente le nombre de replicas"""
        current_deployment = self.k8s_api.read_namespaced_deployment(
            name=self.deployment_name,
            namespace=self.namespace
        )
        current_replicas = current_deployment.spec.replicas
        
        self.k8s_api.patch_namespaced_deployment(
            name=self.deployment_name,
            namespace=self.namespace,
            body={"spec": {"replicas": current_replicas + 1}}
        ) 