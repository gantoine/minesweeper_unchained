from channels import include


project_routing = [
    include("api.routing.app_routing", path=r"^/ws"),
]
