# IP header

## What did the router do?

1. Forward the packet
2. Send the packet back
3. Handle Errors(TTL is 0, links are down)
4. Routing 

## What did the host do?

1. Check the packet's payload is correct.

## IPv4 header Fields

### Handle Errors: Fragment

| 位序号（从高到低） | 名称                      | 含义                              |
| --------- | ----------------------- | ------------------------------- |
| bit 0     | **Reserved (保留位)**      | 永远为 0（历史上为将来用途预留）               |
| bit 1     | **DF (Don't Fragment)** | 1 表示禁止分片，若必须分片则丢弃数据报并返回 ICMP 错误 |
| bit 2     | **MF (More Fragments)** | 1 表示后面还有分片；0 表示这是最后一个分片（或未分片）   |

### Option

> Options lead to more complex implementation.
> Options are variable-length, so routers have to check header length.
> Higher processing overhead for routers.
> On the modern Internet, we avoid options when possible.
>
如果将option 制表 根据对应的序号采取不同的措施，这样option的长度就是定长了。可不可以？

IPv6 中采用了更好的办法 将这些 option 称作 `next header`

### Explicit Congestion Notification bit(ECN)

Congested routers can set this bit

## Security

IP protocal 设计的一些漏洞

### Spoofing 

Lie about the source address

#### Attack a destination

Denial-of-service (DoS) attack: Overwhelm a service by flooding it with packets.

Without spoofing: The service can block your source address. 在检测到某一个地址发送了大量数据包之后 将这个地址发来的流量判定为异常 然后屏蔽即可

Spoofing makes DoS more effective: Server doesn't know which packets to block. 因为用了不同的地址 所以上面的方法就不管用了

#### Attack a User

Attacker pretends to be Bob and sends a virus.

Now Bob is wrongly blamed for sending the virus.

Return traffic (e.g. angry messages) goes to Bob instead.

### Type of Service

If anybody can set ToS bits, attackers can make their own packets high-priority.

Network prefers attacker traffic.

Today, ToS bits are mostly set/used by operators, not end hosts.

### TTL

Trace Route


