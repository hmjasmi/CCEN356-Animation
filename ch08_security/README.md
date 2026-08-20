# Chapter 8 — Security in Computer Networks

Textbook: Kurose & Ross, *Computer Networking: A Top-Down Approach*

## Animations

| File | Textbook section | Status |
|---|---|---|
| `network_security_threats.py` | §8.1 — What Is Network Security? (packet sniffing, IP spoofing, DoS/DDoS) | ✅ Done |
| `tls_handshake.py` | §8.6 — Securing TCP Connections: TLS | ✅ Done |
| _(none yet)_ | §8.2 — Principles of Cryptography | ⬜ TODO |
| _(none yet)_ | §8.3 — Message Integrity and Digital Signatures | ⬜ TODO |
| _(none yet)_ | §8.4 — End-Point Authentication | ⬜ TODO |
| _(none yet)_ | §8.5 — Securing Email | ⬜ TODO |
| _(none yet)_ | §8.7 — Network-Layer Security: IPsec, VPNs | ⬜ TODO |
| _(none yet)_ | §8.8 — Securing Wireless LANs | ⬜ TODO |
| _(none yet)_ | §8.9 — Firewalls and Intrusion Detection | ⬜ TODO |

## Render

```bash
manim -pql ch08_security/network_security_threats.py NetworkSecurity
manim -pql ch08_security/tls_handshake.py TLSHandshake
```

## Notes

- `network_security_threats.py` covers three "bad guys" scenarios in one
  scene: a shared-medium sniffing attack (an eavesdropper copies traffic
  never addressed to it), IP source-address spoofing, and a botnet
  DoS/DDoS flood that drowns out legitimate traffic. Uses the shared
  `Attacker` icon and `network_packet()` helper (labeled src/dst/payload
  cells you can `Circumscribe()` individually).
- `tls_handshake.py` was written fresh for this repo (no earlier draft
  existed) — a simplified ClientHello → ServerHello+cert → key exchange
  flow, with a padlock that closes once both sides derive the session
  key, followed by encrypted application data. Includes a companion
  `TLSDowngradeWarning` scene for a plain-HTTP side-by-side comparison.

Import shared icons/helpers with:

```python
from shared.network_components import *
```

Add a row to the table above and link the script here as each concept
gets animated.
