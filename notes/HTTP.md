# HTTP

## Protocaol Specification

### property

client-server
runs on TCP/UDP
request based

### Request

### Response

#### Status Codes

[A Really Funny Website](https://httpstatusdogs.com/)

100s Informational responses

200s Successfunl responses

300s Redirection messages

400s Client error

500s Server error

### HTTP headers

Not mandatory

Three classes

#### Request

#### Response

#### Representation

## Examples

```shell
telnet google.com 80
```

## Seppding Up HTTP

### Pipelining

Allow multiple requests to be pipelined over the same TCP connection.

**Trade-off**: The server must maintain more open connections. 
Attacker could overwhelm the server by request.

### Cache

#### Private 

Owned and used by a single user, **not shared**.

#### Proxy

Provided by ISP(Internet Sercive Provider) or somebody else (not the client or server)

##### Problem

1. Clients need to be redirected to the proxy cache somehow

Possible Approach:

DNS resolver could lie and say,"server's IP address is [proxy cache address]."

2. Contains outdate information

Because the Proxy cache is separate from Origin Server

#### Managed

Opreated by the server

### Implement Caching

1. Static
2. Dynamic

HTTP header (Expries Header)
- Request to cache. Not enforce

# Content Delivery Networks (CDNs)

**Closer** to the user

## Deployment

## Directing Clients to Caches

### Anycast

![Problem](image-24.png)

### DNS-Based Load Balancing

### Application-Level Mapping

# Newer HTTP Versions

## HTTPS (security)

## HTTP/2.0

## HTTP/3.0