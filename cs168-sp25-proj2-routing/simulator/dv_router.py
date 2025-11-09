"""
Your awesome Distance Vector router for CS 168

Based on skeleton code by:
  MurphyMc, zhangwen0411, lab352
"""

import sim.api as api
from cs168.dv import (
    RoutePacket,
    Table,
    TableEntry,
    DVRouterBase,
    Ports,
    FOREVER,
    INFINITY,
)


# represents a single
class DVRouter(DVRouterBase):

    # A route should time out after this interval
    ROUTE_TTL = 15

    # -----------------------------------------------
    # At most one of these should ever be on at once
    SPLIT_HORIZON = False
    POISON_REVERSE = False
    # -----------------------------------------------

    # Determines if you send poison for expired routes
    POISON_EXPIRED = False

    # Determines if you send updates when a link comes up
    SEND_ON_LINK_UP = False

    # Determines if you send poison when a link goes down
    POISON_ON_LINK_DOWN = False

    def __init__(self):
        """
        Called when the instance is initialized.
        DO NOT remove any existing code from this method.
        However, feel free to add to it for memory purposes in the final stage!
        """
        assert not (
            self.SPLIT_HORIZON and self.POISON_REVERSE
        ), "Split horizon and poison reverse can't both be on"

        self.start_timer()  # Starts signaling the timer at correct rate.

        # Contains all current ports and their latencies.
        # See the write-up for documentation.
        self.ports = Ports()

        # This is the table that contains all current routes
        self.table = Table()
        self.table.owner = self

        ##### Begin Stage 10A #####
        # 如果 force=False，你只应当在某个端口上通告一条路由，
        # 当且仅当该路由与之前你通过该端口发送的路由不同，
        # 或者你之前从未通过该端口发送过该路由。
        # router is different 
        # 如何分辨 router 是不同的？
        # 通过 latency 在同样的 destination 同样的 port 的情况下
        # 通过 latency 分辨不同的 router
        from collections import defaultdict
        self.history = defaultdict(dict) # port, dst
        ##### End Stage 10A #####

    def add_static_route(self, host, port):
        """
        Adds a static route to this router's table.

        Called automatically by the framework whenever a host is connected
        to this router.

        :param host: the host.
        :param port: the port that the host is attached to.
        :returns: nothing.
        """
        # `port` should have been added to `peer_tables` by `handle_link_up`
        # when the link came up.
        assert port in self.ports.get_all_ports(), "Link should be up, but is not."

        ##### Begin Stage 1 #####
        self.table[host] = TableEntry(
            dst = host,
            port = port,
            latency = self.ports.get_latency(port),
            expire_time = FOREVER
        )
        ##### End Stage 1 #####

    def handle_data_packet(self, packet, in_port):
        """
        Called when a data packet arrives at this router.

        You may want to forward the packet, drop the packet, etc. here.

        :param packet: the packet that arrived.
        :param in_port: the port from which the packet arrived.
        :return: nothing.
        当数据包到达此路由器时调用。

        您可能需要在此处转发数据包、丢弃数据包等。

        :param packet: 到达的数据包。
        :param in_port: 数据包到达的端口。
        :return: 无。
        """
        
        ##### Begin Stage 2 #####
        if packet.dst not in self.table:
            return 
        
        entry = self.table[packet.dst]
        if entry.latency >= INFINITY:
            return
        
        self.send(packet, port = entry.port)
        ##### End Stage 2 #####

    
    def _send_route(self, port, destination, latency, force=False):
        """
        Helper method to deal with force == False
        If note force, 
        you will update the only advertise a route out of a port 
        if the route is different from what you previously sent along that port, 
        or if you haven’t previously sent that route along that port before.
        """
        if not force:
            if self.history[port].get(destination, None) == latency:
                return
        # force is True
        # send to everyone
        self.send_route(port, destination, latency)
        self.history[port][destination] = latency

    def send_routes(self, force=False, single_port=None):
        """
        Send route advertisements for all routes in the table.

        :param force: if True, advertises ALL routes in the table;
                      otherwise, advertises only those routes that have
                      changed since the last advertisement.
               single_port: if not None, sends updates only to that port; to
                            be used in conjunction with handle_link_up.
        :return: nothing.
        """
        """
        向表中所有路由发送路由通告。

        :param force: 如果为 True，则通告表中的所有路由；
                      否则，仅通告自上次通告以来发生更改的路由。
               single_port: 如果不为 None，则仅向该端口发送更新；应
                            与 handle_link_up 结合使用。
        :return: 无。
        """
        # 这里是更新self的所有邻居
        ##### Begin Stages 3, 6, 7, 8, 10 #####
        if single_port is not None:
            ports = single_port
        else:
            ports = self.ports.get_all_ports()
        for routers in self.table.values():
            for p in ports:
                if p == routers.port:
                    if self.SPLIT_HORIZON:
                        continue
                    elif self.POISON_REVERSE:
                        self._send_route(p, routers.dst, INFINITY, force)
                        continue
                latency = min(INFINITY, routers.latency)
                self._send_route(p, routers.dst, latency, force)
        ##### End Stages 3, 6, 7, 8, 10 #####

    def expire_routes(self):
        """
        Clears out expired routes from table.
        accordingly.
        """
        
        ##### Begin Stages 5, 9 #####
        routers_to_remove = []
        for router in self.table.values():
            if router.expire_time <= api.current_time():
                routers_to_remove.append(router)

        if self.POISON_EXPIRED:
            for router in routers_to_remove:
                new_entry = TableEntry(
                    dst = router.dst,
                    port = router.port,
                    latency = INFINITY,
                    expire_time = api.current_time() + self.ROUTE_TTL
                )
                self.table[router.dst] = new_entry
        else:
            for router in routers_to_remove:
                self.table.pop(router.dst)
        ##### End Stages 5, 9 #####

    def handle_route_advertisement(self, route_dst, route_latency, port):
        """
        Called when the router receives a route advertisement from a neighbor.

        :param route_dst: the destination of the advertised route.
        :param route_latency: latency from the neighbor to the destination.
        :param port: the port that the advertisement arrived on.
        :return: nothing.
        """
        """
        当路由器从邻居收到路由通告时调用。

        :param route_dst: 通告路由的目的地。
        :param route_latency: 从邻居到目的地的延迟。
        :param port: 通告到达的端口。
        :return: 无。
        
        """        
        ##### Begin Stages 4, 10 #####
        new_latency = route_latency + self.ports.get_latency(port)
        new_entry = TableEntry(
            dst = route_dst,
            port = port,
            latency = new_latency, 
            expire_time = api.current_time() + float(self.ROUTE_TTL),
        )

        if route_dst not in self.table:
            self.table[route_dst] = new_entry
            self.send_routes(force=False)
        else:
            entry = self.table[route_dst]
            if port == entry.port:
                self.table[route_dst] = new_entry
                self.send_routes(force=False)
            elif new_latency < entry.latency:
                self.table[route_dst] = new_entry
                self.send_routes(force=False)
            else:
                pass
        ##### End Stages 4, 10 #####

    def handle_link_up(self, port, latency):
        """
        Called by the framework when a link attached to this router goes up.

        :param port: the port that the link is attached to.
        :param latency: the link latency.
        :returns: nothing.
        """
        self.ports.add_port(port, latency)

        ##### Begin Stage 10B #####
        if self.SEND_ON_LINK_UP:
            self.send_routes(force=False, single_port=port)
        ##### End Stage 10B #####

    def handle_link_down(self, port):
        """
        Called by the framework when a link attached to this router goes down.

        :param port: the port number used by the link.
        :returns: nothing.
        """
        self.ports.remove_port(port)

        ##### Begin Stage 10B #####
        affected = [entry for entry in self.table.values() if entry.port == port]
        
        if self.POISON_ON_LINK_DOWN:
            for entry in affected:
                new_entry = TableEntry(
                    dst = entry.dst,
                    port = entry.port,
                    latency = INFINITY,
                    expire_time = api.current_time() + float(self.ROUTE_TTL)
                )
                self.table[entry.dst] = new_entry

            if affected:
                # don't sent to everyone
                self.send_routes(force=False)

        else:
            for router in affected:
                self.table.pop(router.dst)
                
        ##### End Stage 10B #####

    # Feel free to add any helper methods!
