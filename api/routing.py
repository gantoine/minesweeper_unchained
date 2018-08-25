from channels.generic.websockets import WebsocketDemultiplexer
from channels.routing import route_class
from .subscriptions import BoardSubscription, CellSubscription


class AppDemultiplexer(WebsocketDemultiplexer):
    consumers = {
      'boards': BoardSubscription.get_binding().consumer,
      'cells': CellSubscription.get_binding().consumer
    }


app_routing = [
    route_class(AppDemultiplexer)
]
