output "reducto_endpoint" {
    # value = "http://${data.kubernetes_service.reducto.status.0.load_balancer.0.ingress.0.hostname}"
    value = "http://${data.kubernetes_service.nginx.status.0.load_balancer.0.ingress.0.hostname}"
}

