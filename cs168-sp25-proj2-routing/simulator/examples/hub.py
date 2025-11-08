import sim.api as api
from sim.basics import *


class Hub(api.Entity):
    """
    A dumb hub.

    This just sends every packet it gets out of every port.  On the plus side,
    if there's a way for the packet to get to the destination, this will find it.
    On the down side, it's probably pretty wasteful.  On the *very* down side,
    if the topology has loops, very bad things are about to happen.
    """
    """
    一个简单的集线器。

    它只是将收到的每个数据包从所有端口发送出去。优点是，如果数据包有办法到达目的地，它就能找到。
    缺点是，这可能非常浪费。而且，在非常糟糕的情况下，如果拓扑结构中存在环路，接下来就会发生非常糟糕的事情。
    """
    """
    CS-168 网络模拟器
    您可以在很多方面获得帮助。
    例如，如果您加载了一个名为 foo 的模块，请尝试 help(foo)。
    如果您有一个名为 h1a 的主机，请尝试 help(h1a)。
    如果您要检查该主机的方法，请尝试 help(h1a.ping)。
    有关模拟器及其 API 的帮助，请尝试 help(sim) 和 help(api)。
    输入 start() 来启动模拟器（或使用 --start 参数）。
    Ctrl-D 或 exit() 退出。
    祝你好运！
    INFO:web:Webserver 运行在 http://127.0.0.1:4444
    INFO:simulator:正在启动模块 'topos.linear'
    INFO:simulator:s1 已启动！
    INFO:simulator:h1 已启动！
    INFO:simulator:s2 已启动！
    INFO:simulator:h2 已启动！
    INFO:simulator:s3 已启动！
    INFO:simulator:h3 已启动！
    INFO:simulator:开始模拟。
    """

    def handle_rx(self, packet, in_port):
        # We'll just flood the packet out of every port.  Except the one the
        # packet arrived on, since whatever is out that port has obviously
        # seen the packet already!
        self.send(packet, in_port, flood=True)
