# Ethernet

## Connectiong Local Hosts

### Shared Media

interfere or collide

## Multiple Access Protocols

### Multiplexing

Fixed slice of resources to each node

#### Frequency-based

fixed-frequency FM AM radio broadcast

#### Time-based

fixed-time-slice

#### Problem

Wasteful (a kind of like reservation bandwidth)

### Taking Turns

If someone has nothing to say, immediately move on.  
**No more time wasted no idling**

#### Token passing

hold token -> talk

#### Polling Protocols

A coordinator decides when each node can speak.

#### Problem

Complexity  
1. implement inter-node communication  
2. how to select central coordinator  
3. two nodes both think they have the token (token duplication)

### Random Access

#### ALOHA

Collision corrupts the packets -> wait some random amount of time, then resend.  
If waiting is fixed, collisions repeat.

#### CSMA (Carrier Sense Multiple Access)

Listen first; only send when quiet.

##### Problem

Propagation delay

#### CSMA/CD

before sending --> listening  
sending --> listening

##### binary exponential backoff

After every collision, wait up to twice as long before resending.

## Sending Packets

In the same LAN can exchange messages directly at Layer 2.

### MAC address (Media Access Control)

48 bits.  
Globally unique.  
Burned in machine.

#### Unicast

Destination = recipient's MAC

#### Broadcast

FF:FF:FF:FF:FF:FF  
special case of multicast (first bit = 1)

#### Multicast

First bit 1 → Group address

## Layer 2 Networks

Routing protocols from Layer 3 can also be used at Layer 2.  
Cannot be aggregated.

# Layer 2 Routing

RECALL: 
Unicast: send the packet to everyone. The end host checks whether the packet is for it.

1. Watate bandwidth
2. loop

## Learning switches

更像是通过 learning 方式的 distance-vector

We will not use solutions we have seen before in IP(distance-vector or link-state)

1. high churn. 

```cpp
class Switch {
    map<MAC, port> table;

    on_receive(frame, in_port):
        table[frame.src] = in_port   // learn source

        if (frame.dest in table):
            out_port = table[frame.dest]
            send(frame, out_port)    // unicast
        else:
            flood(frame, except=in_port)
}
```

## Spanning Tree Protocol

### Broadcast storms

### Three flags

## Implementing STP with BPDU(Bridge Protocol Data Units)



