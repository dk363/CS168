# IP Routers

## Router Components

1. data plane
    packet arrives and needs to be forwarded
2. control plane
    communicating with other rouers
3. management plane
    Operator uses network management system (NMS) to interact with router.
![alt text](image-1.png)

## Packet Type

1. User packet
2. Control plane traffic
3. Punt traffic

## Forwarding in Hardware

1. Receive the packet from other systems.
PHY (physical layer): Decode the optical/electrical signal into 1s and 0s.
MAC (link layer): Perform link-layer operations.
These are implemented in hardware.
2. Process the packet.
Parse the packet to understand its headers, e.g. IPv4 or IPv6.
Look up the next hop in the forwarding table.
Update the packet.
Decrement TTL, update checksum, fragment packet if it's too big, etc.
3. Send the packet onwards.
Fabric interconnect chip sends packets to other linkcards via inter-chassis links.


## Efficient Forwarding with Tries

采用通配符的方法将port相同的destination聚合

![alt text](image.png)
In this case, i found we should keep another variety `last port` to prevent we falling down the tries.

simple relalization
```cpp
struct TrieNode {
    TrieNode* son[26]{};
    bool isEnd = false;
    int port;
};

#define DEFAULT_PORT_NUMBER // define by yourself

class PortTrie {
private:
    TrieNode* root;

public:
    PortTrie() {
        root = new TrieNode();
        // default port number
        root->port = DEFAULT_PORT_NUMBER;
    }

    void insert(string preFix, int port) {
        TrieNode* cur = root;
        for (int i = 0; i < preFix.size(); ++i) {
            c -= 'a';
            if (cur->son[c] == nullptr) {
                cur->son[c] = new TrieNode();
            }
            cur = cur->son[c];
        }
        cur->isEnd = true;
        cur->port = port;
    }

    int findLongestPreFixPort(string dream_port) {
        TrieNode* cur = root;
        int lastValidPort = root->port;

        for (char c : dream_port) {
            c -= 'a';
            if (cur->son[c] == nullptr) {
                break;
            } else {
                if (cur->isEnd) {
                    lastValidPort = cur->port;
                }
                cur = cur->son[c];
            }
        }
        return lastValidPort;
    }
}

```

# summarize

总的来说，这一节先讲 router 的物理结构
然后将 packet 转发的过程同物理结构相结合
然后点出转发过程中的最难点 也就是最耗费时间的 查表功能
最后提出用字典树的方法 O(1) 解决查表
