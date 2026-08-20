# Chapter 1 — Computer Networks and the Internet

Textbook: Kurose & Ross, *Computer Networking: A Top-Down Approach*, Ch. 1

## Animations

| File | Textbook section | Status |
|---|---|---|
| `whats_a_protocol.py` | §1.2 — What is a protocol? | ✅ Done |
| `packet_delays.py` | §1.4 — Delay, Loss, and Throughput in Packet-Switched Networks | ✅ Done |
| `encapsulation.py` | §1.5 — Protocol Layers and Their Service Models (encapsulation) | ⬜ TODO |

## Render

```bash
manim -pql ch01_intro/whats_a_protocol.py WhatsAProtocol
manim -pql ch01_intro/packet_delays.py PacketDelays
```

## Notes

- `whats_a_protocol.py` places a human-conversation sequence diagram
  next to the analogous computer-network exchange (TCP handshake +
  HTTP GET/response) so students see the parallel directly.
- `packet_delays.py` distinguishes the four delay types physically:
  processing (brief pulse), queueing (packet waits), transmission
  (packet stretches onto the wire — "uncoiling a rope"), and
  propagation (fully-formed packet slides to the next router) — plus a
  synchronized timeline bar underneath.
- Encapsulation animation (§1.5) still needs to be rebuilt into a
  standalone script — see the shared library's `place_packet`-style
  helpers if you're recreating the header-stripping-by-layer visual.

## Other §1.x topics not yet animated

- §1.1 — What is the Internet? (network of networks overview)
- §1.3 — The Network Core (circuit vs. packet switching)
- §1.6 — Networks Under Attack (security intro)
- §1.7 — History of Computer Networking and the Internet
