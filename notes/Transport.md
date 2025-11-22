# Transport Layer Design Goals

## Problem 

1. IP offers the best effort delicery. (It means packets could be lost and ...)

2. Applications don't want to care about the packets and best-effort
Programmers want to think in terms of a more convenient abstraction.

(Transport 实现的 更像是 第三层的一个补丁 处理第三层会发生的问题 提供一个简洁的接口给 Application)

## De-Multiplexing

We have multiple choose. We had to choose just one.

1. ports
Each running application on your computer is associatedd with a port number.
A logical port is a number in the Layer 4 header to disambiguate which application a packet belongs to.

2. In the IP header, there is a protocal field. It tells us which portocal we will choose in the layer 4.

# Impleamenting Reliability

## Single Packet

### Goals

1. Correctness: The destination receives every packet, uncorrupted, in order.

2. Timeliness: Minimize time until data is transferred.

3. Efficiency: Minimize use of bandwidth.
    Avoid sending packets unnecessarily.
    Example of inefficient protocol: Send 1000 copies of every packet.

### Definition 

1. At-least-once delivery

2. Give up, but must announce it to the application.
    For example, computer not connect to Internet.

### ack

When the recipient receive message, the recipient replies with an acknowledgment (ack).
给 sender 报平安 :)

### Problem

大部分呢情况 resend 可以解决问题
所以更重要的是 timeout 时的 resend 间隔 

### RTT (round-trip time)

RTT is when you expected to see the ack.

决定了什么时候重传

## Multiple Packets (Windows)

It's spamming data into the network possibly over flooding the network and causing cues to build up and packets to be dropped.

要考虑率一整条链路的承载能力

Limit the amount of packet in flight.
![alt text](image-10.png)

### How big should the Window be?

窗口大小 指的是 How many packets in flight.
就是发送的能力

$W = RTT * bandwidth$

当然了 就像上面说的那样 还要考虑 recepient and network 的承载能力 ( 短板效应 )

## Avoiding Overload 

### Flow Control & Congestion Control

recepient 的 buffer 是有限的

比如说 buffer = 2
如果传入了 1 2 但是 3 丢失了 那么recepient 将不会接受 4 5 而是将其放在 buffer 中等到 3 传入再接受后面的

为了避免重传的问题 这里还要继续下降 W 的大小

## Smarter ack

### Individual acks

为对应的已经接收到的 packet 发送对应的 ack

如果 ack 丢失 需要重发 packet 

与 packet 相比 ，ack 的大小更小 所以重发得不偿失

### full information acks

When you receive a packet, send an ack listing every packet received.

```cpp
int n = ack.size();
for (int i = n - 1; i >= 0; i--) {
    // 倒序遍历 优化
    // 避免重复计数
    if (seen.count(ack[i])) {
        break;
    }
    seen.insert(ack[i]);
}
```

这样的写法有问题
![alt text](image-11.png)
如果是这样的情况 那么优化反而会出问题

### cumulative acks

只发送已经完整接收到哪里 比如说前十二个到了 那么就发送 received all packet up to 12

这样效率更高 反正如果不是连起来的 (像上面的例子) recepient 也不会接受

## Detecting Loss Early

如何尽早发现丢包？

根据 end-to-end rule 不能够让 router 检查

那么只有让 host 检查了 
之前提到过 timeout 如果在规定时间内没有收到对应的 ack 那么就要重传 那么可不可以更快一些呢？
将 ack 中的信息利用起来 
> Declare a packet lost if k subsequent packets are acked.
> k = 3 is common.

### Individual acks

```cpp
int curr;
int k = 3;

bool check(acks) {
    int curr = 0;
    for (ack in acks) {
        if (ack.packet_number == curr) {
            curr++;
        } else {
            k--;
            if (k < 0) {
                return false;
            }
        }
    }
    return true;
}
```

### Full Information acks

We can see the gap in the acks

### Cumulative acks

```cpp
int last_ack = -1;
int dup_count = 0;

bool detect_loss(ack_number):
    if (ack_number == last_ack):
        dup_count++;
        if (dup_count == 3):   // 3 DUP ACKs
            return true;       // packet presumed lost
    else:
        last_ack = ack_number;
        dup_count = 0;

    return false;

```

