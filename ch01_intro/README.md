# Chapter 1 — Computer Networks and the Internet

Textbook: Kurose & Ross, *Computer Networking: A Top-Down Approach*, Ch. 1

## Animations

| File | Textbook section | Status |
|---|---|---|
| `whats_a_protocol.py` | §1.2 — What is a protocol? | ✅ Done |
| `packet_delays.py` | §1.4 — Delay, Loss, and Throughput (the four delays) | ✅ Done |
| `throughput_bottleneck.py` | §1.4 — Throughput and the bottleneck link | ✅ Done |
| `encapsulation.py` | §1.5 — Protocol Layers and Their Service Models (encapsulation) | ✅ Done |

## Render

```bash
manim -pql ch01_intro/whats_a_protocol.py WhatsAProtocol
manim -pql ch01_intro/packet_delays.py PacketDelays
manim -pql ch01_intro/throughput_bottleneck.py Throughput
manim -pql ch01_intro/encapsulation.py Encapsulation
```

## Notes

- `whats_a_protocol.py` places a human-conversation sequence diagram
  next to the analogous computer-network exchange (TCP connection
  request/response + HTTP GET/response) so students see the parallel
  directly, ending on "other human protocols?" as a discussion prompt.
- `packet_delays.py` distinguishes the four delay types physically:
  processing (brief pulse), queueing (packet waits), transmission
  (packet stretches onto the wire — "uncoiling a rope"), and
  propagation (fully-formed packet slides to the next router) — plus a
  synchronized timeline bar underneath.
- `throughput_bottleneck.py` shows two scenarios (Rs < Rc, then Rs > Rc)
  as literal bit-flow through pipes whose height encodes link capacity.
  Each dot's position and visibility is driven by a single time-based
  function (`UpdateFromAlphaFunc`) rather than chained `.animate` calls,
  so when Rc is the bottleneck a genuine FIFO backlog forms and drains
  at the correct relative pace. Ends on "Throughput = min(Rs, Rc)".
- `encapsulation.py` walks a message down the source's protocol stack
  (gaining H_t, then H_n, then H_l), across the physical medium, and
  back up the destination's stack (stripped in reverse order) — built
  from the shared `layer_stack` / `header_box` / `message_box` /
  `build_packet` / `place_packet` helpers.

## Other §1.x topics not yet animated

- §1.1 — What is the Internet? (network of networks overview)
- §1.3 — The Network Core (circuit vs. packet switching)
- §1.6 — Networks Under Attack — see `ch08_security/network_security_threats.py`,
  which already covers this at the §1.6/§8.1 "bad guys" level (sniffing,
  spoofing, DoS/DDoS); link or duplicate it here if you teach it in Ch.1
- §1.7 — History of Computer Networking and the Internet
