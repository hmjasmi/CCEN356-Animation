# CCEN 356 — Computer Networks: Animation Library

Manim-based animations for **CCEN 356 (Computer Networks)** at Khalifa
University, built to accompany **Kurose & Ross, *Computer Networking: A
Top-Down Approach*** (8th ed.).

Animations are organized **one folder per textbook chapter**, so the
repo can grow alongside the course.

## Structure

```
shared/                          reusable icon + animation library
ch01_intro/                      Ch 1 — Computer Networks and the Internet
ch02_application_layer/          Ch 2 — Application Layer
ch03_transport_layer/            Ch 3 — Transport Layer
ch04_network_layer_data_plane/   Ch 4 — Network Layer: Data Plane
ch05_network_layer_control_plane/ Ch 5 — Network Layer: Control Plane
ch06_link_layer_lans/            Ch 6 — Link Layer and LANs
ch07_wireless_mobile/            Ch 7 — Wireless and Mobile Networks
ch08_security/                   Ch 8 — Security in Computer Networks
ch09_multimedia_networking/      Ch 9 — Multimedia Networking
```

Each chapter folder has its own `README.md` listing which textbook
sections are covered, which animations exist, and which are still TODO.

## Setup

```bash
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

You'll also need [FFmpeg](https://ffmpeg.org/) and a LaTeX distribution
installed system-wide if you plan to render math-heavy scenes (Manim
uses both). See the [Manim install guide](https://docs.manim.community/en/stable/installation.html)
for OS-specific steps.

## Rendering a scene

```bash
manim -pql ch01_intro/whats_a_protocol.py WhatsAProtocol
```

- `-p` previews the result after rendering
- `-ql` = quick/low quality (fast, for drafting)
- `-qh` = high quality (for the final export you'd post/embed)

Every chapter script imports from `shared/network_components.py`, so
run commands from the **repo root** (not from inside a chapter folder)
so the import resolves.

## Component library (`shared/network_components.py`)

One shared visual language used across every chapter:

- **Icons**: `Host`, `Server`, `Router`, `Switch`, `Firewall`, `Person`
- **Sequence-diagram helpers**: `lifeline`, `message_arrow` — for
  protocol-exchange topics drawn as a ladder diagram
- **Animation helpers**: `send_packet`, `connect`, `step_caption`
- **Color code** (consistent across all topics):

  | Color | Meaning |
  |---|---|
  | Blue (`REQUEST_COLOR`) | outbound request (SYN, GET, ...) |
  | Green (`RESPONSE_COLOR`) | response / ack |
  | Red (`ERROR_COLOR`) | error, drop, RST |
  | Orange (`RETRANSMIT_COLOR`) | retransmit / retry / timeout |
  | Purple (`SECURE_COLOR`) | encrypted / TLS traffic |

## Adding a new animation

1. Pick the textbook chapter/section the concept belongs to.
2. Storyboard the steps in plain language first (who sends what, in
   what order).
3. Write the scene in that chapter's folder, importing from
   `shared.network_components`.
4. Update that chapter's `README.md` — mark the section covered and
   link the new file.
5. Render, sanity-check, then commit.

```python
from shared.network_components import *

class ARPRequest(Scene):
    def construct(self):
        host = Host("Host A").to_edge(LEFT)
        router = Router("Gateway").to_edge(RIGHT)
        self.play(FadeIn(host), FadeIn(router))
        self.play(Create(connect(host, router)))
        self.play(*send_packet(host, router, "Who has 192.168.1.1?", color=REQUEST_COLOR))
        self.play(*send_packet(router, host, "MAC: AA:BB:...", color=RESPONSE_COLOR))
```

Most topic scripts stay under ~50 lines because the icons, colors, and
packet motion are already handled by the shared library.

## License

Course material for CCEN 356, Khalifa University. Add your preferred
license in `LICENSE` (MIT is a reasonable default for teaching code).
