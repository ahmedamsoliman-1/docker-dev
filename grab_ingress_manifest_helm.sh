CHART_VERSION="4.4.0"
APP_VERSION="1.5.1"

mkdir ./aams/ingress

helm template ingress-nginx ingress-nginx \
--repo https://kubernetes.github.io/ingress-nginx \
--version ${CHART_VERSION} \
--namespace ingress-nginx \
> ./aams/ingress/nginx-ingress.${APP_VERSION}.yaml