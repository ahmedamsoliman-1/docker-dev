import subprocess
from utils import StreamLogger

stream_logger = StreamLogger()

def run_command(command):
    """Run a shell command and return the output and error."""
    stream_logger.stream_logger.system(command)
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    if output: stream_logger.stream_logger.info(output.decode('utf-8'))
    if error: stream_logger.stream_logger.error(error.decode('utf-8'))

def create_kind_cluster():
    run_command("kind create cluster --image kindest/node:v1.23.6 --config kind.yaml")

def basics():
    run_command("minikube start")
    run_command("kind create cluster --image kindest/node:v1.23.5")
    run_command("kubectl config get-contexts")
    run_command("kubectl config current-context")
    run_command("kubectl config use-context minikube")
    run_command("kubectl config current-context")
    run_command("kubectl get nodes")
    run_command("kubectl get pods")

def get_command():
    run_command("kubectl get pods")
    run_command("kubectl get deployments")
    run_command("kubectl get services")
    run_command("kubectl get nodes")
    run_command("kubectl get secrets")
    run_command("kubectl get configmaps")
    run_command("kubectl get persistentvolumes")
    run_command("kubectl get ingress")
    run_command("kubectl get namespaces")


def namespaces():
    run_command("kubectl get namespaces")
    run_command("kubectl create namespace test")
    run_command("kubectl get namespaces")
    run_command("kubectl delete namespace test")
    run_command("kubectl get namespaces")


def describe():
    run_command("kubectl describe pods -n kube-system")

def version():
    run_command("kubectl version")

def deployment():
    # A Deployment controller provides declarative updates for Pods and ReplicaSets.
    # A Deployment is a set of Pods with the same configuration.

    run_command('kubectl apply -f deployment.yaml')
    run_command('kubectl get deploy')
    run_command('kubectl get po')
    run_command('kubectl describe deployments example-deploy')
    run_command('kubectl logs example-deploy-6c598cf449-fhm2r')
    pass


def config_map():
    # A config map is an API object used to store non-confidential data in key-value pairs.
    # A ConfigMap allows you to decouple environment-specific configuration from your container images,
    # so that your applications are easily portable.

    # Docker example
    # run_command(f'docker run -it -v ${PWD}/golang/configs/:/configs -v ${PWD}/golang/secrets/:/secrets aimvector/golang:1.0.0')
    
    # Kubernetes
    run_command('kubectl apply -f configmap.yaml')
    run_command('kubectl get cm')
    run_command('kubectl get configmaps')
    run_command('kubectl get configmaps example-config -o yaml')
    pass

def secrets():
    # A secret is an API object used to store sensitive data, such as passwords, API keys, and certificates.
    # Secrets can be used to store sensitive data in a Kubernetes cluster,
    # so that it can be accessed by applications running in different environments.

    # Docker example
    # run_command(f'docker run -it -v ${PWD}/golang/configs/:/configs -v ${PWD}/golang/secrets/:/secrets aimvector/golang:1.0.0')

    # Kubernetes
    run_command('kubectl apply -f secret.yaml')
    run_command('kubectl get secret')
    run_command('kubectl get secrets')
    run_command('kubectl get secrets mysecret -o yaml')
    pass

def get_dashboard():
    # Deploy the Dashboard
    run_command('kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v2.6.1/aio/deploy/recommended.yaml')

    # Create Service Account
    run_command('kubectl create serviceaccount dashboard-admin-sa')

    # Create ClusterRoleBinding
    run_command('kubectl create clusterrolebinding dashboard-admin-sa --clusterrole=cluster-admin --serviceaccount=default:dashboard-admin-sa')

    # Get the Secret Name
    run_command('kubectl get secrets')

    # Describe the Secret to get the Token (replace <secret-name> with the actual name)
    run_command('kubectl describe secret <secret-name>')

    # Start the Proxy
    run_command('kubectl proxy')


def load_balance_service_discovery():
    run_command('kubectl get deploy')
    run_command('kubectl get pods --show-labels')
    run_command('kubectl get svc')
    run_command('kubectl apply -f docker-development-youtube-series/kubernetes/services/service.yaml')
    run_command('kubectl get svc')
    run_command('kubectl describe svc example-service')
    pass

def ingress_controller_deployment():
    # run_command('kubectl get nodes')
    # run_command('kubectl get ns')
    # run_command('kubectl create ns example-app')
    # run_command('kubectl apply -n example-app -f kubernetes/deployments/deployment.yaml')
    # run_command('kubectl apply -n example-app -f kubernetes/configmaps/configmap.yaml')
    # run_command('kubectl apply -n example-app -f kubernetes/secrets/secret.yaml')
    # run_command('kubectl apply -n example-app -f kubernetes/services/service.yaml')
    # run_command('kubectl -n example-app port-forward example-deploy-6987b76b58-9cf46 5000')

    run_command('kubectl apply -f kubernetes/ingress/controller/nginx/namespace.yaml')
    run_command('kubectl apply -f kubernetes/ingress/controller/nginx/service-account.yaml')
    run_command('kubectl apply -f kubernetes/ingress/controller/nginx/cluster-role.yaml')
    run_command('kubectl apply -f kubernetes/ingress/controller/nginx/cluster-role-binding.yaml')
    run_command('kubectl apply -f kubernetes/ingress/controller/nginx/configMap.yaml')
    run_command('kubectl apply -f kubernetes/ingress/controller/nginx/custom-snippets.configmap.yaml')
    run_command('kubectl apply -f kubernetes/ingress/controller/nginx/deployment.yaml')
    run_command('kubectl apply -f kubernetes/ingress/controller/nginx/service.yaml')
    run_command('kubectl apply -f kubernetes/ingress/controller/nginx/tls-secret.yaml')

    run_command('kubectl apply -f kubernetes/ingress/ingress-nginx-example.yaml')
    # run_command('kubectl')
    # run_command('kubectl')
    # run_command('kubectl')
    # run_command('kubectl')

def nodejs():
    # docker build . -t ahmedalimsolimansd/nodejs:v2
    # docker push ahmedalimsolimansd/nodejs:v2

    # namespace = 'example-nodejs-app'
    # run_command('kubectl get nodes')
    # # run_command(f'kubectl create ns example-nodejs-app')
    # run_command(f'kubectl apply -n example-nodejs-app -f nodejs/deployment/deployment.yaml')
    # run_command(f'kubectl apply -n example-nodejs-app -f nodejs/deployment/service.yaml')
    pass

def monitor_ingress():
    run_command('kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml')

    run_command('kubectl apply -f ingress/monitoring-ingress.yaml')

    run_command('kubectl get pods --all-namespaces')
    pass

def prometheus():
    run_command('kubectl get nodes')
    run_command('kubectl create ns monitoring')

    # prometheus operator
    run_command('kubectl -n monitoring apply -f monitoring/prometheus/kubernetes/1.18.4/prometheus-operator')
    run_command('kubectl -n monitoring apply -f monitoring/prometheus/kubernetes/1.18.4/node-exporter')
    run_command('kubectl -n monitoring apply -f monitoring/prometheus/kubernetes/1.18.4/kube-state-metrics')
    run_command('kubectl -n monitoring apply -f monitoring/prometheus/kubernetes/1.18.4/alertmanager')
    run_command('kubectl -n monitoring apply -f monitoring/prometheus/kubernetes/1.18.4/prometheus-cluster-monitoring')
    run_command('kubectl -n monitoring create -f monitoring/prometheus/kubernetes/1.18.4/grafana')



    run_command('kubectl -n monitoring get pods')

    run_command('kubectl -n monitoring port-forward svc/alertmanager-main 9093')
    run_command('kubectl -n monitoring port-forward svc/grafana 3000')
    run_command('kubectl -n monitoring port-forward svc/prometheus-k8s 9090')

    run_command('kubectl -n monitoring port-forward svc/kube-state-metrics 8443')
    run_command('kubectl -n monitoring port-forward svc/node-exporter 9100')

    run_command('kubectl -n monitoring port-forward svc/prometheus-adapter 443')
    run_command('kubectl -n ingress-nginx port-forward svc/ingress-nginx-controller 80')


def prometheus_II():
    # run_command('kubectl get nodes')
    # run_command('kubectl create -f ./aams/monitoring/manifests/setup/')
    # run_command('kubectl create -f ./aams/monitoring/manifests/')

    run_command('kubectl get deploy -n monitoring')
    run_command('kubectl get svc -n monitoring')
    run_command('kubectl get pods -n monitoring')

def check_cluster():
    run_command('kubectl get nodes')
    run_command('kubectl get ns')

    run_command('kubectl get deploy --all-namespaces')
    run_command('kubectl get svc --all-namespaces')
    run_command('kubectl get po --all-namespaces')

def example_app():
    # run_command('kubectl create ns example-app')
    # run_command('kubectl create -f ./aams/example-app-1/nginx-deployment.yaml')
    # run_command('kubectl create -f ./aams/example-app-1/nginx-svc.yaml')
    run_command('kubectl get po -n example-app')

def main():
    # create_kind_cluster()
    # prometheus_II()
    # prometheus()
    # monitor_ingress()
    # ingress()
    # basics()
    # get_command()
    # namespaces()
    # describe()
    # version()
    # deployment()
    # config_map()
    # load_balance_service_discovery()
    # ingress_controller_deployment()
    # nodejs()
    check_cluster()
    # example_app()
    pass

if __name__ == "__main__":
    main()
    stream_logger.stream_logger.warning("Execution Stopped")
