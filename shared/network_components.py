"""
network_components.py
======================
Reusable Manim component library for CCEN 356 (Computer Networks)
animations.

Import this module in any chapter script (TCP handshake, ARP, NAT, TLS,
DNS, congestion control, etc.) to reuse a consistent visual language
instead of rebuilding icons and colors from scratch every time.

    from shared.network_components import *

Icons included: Host, Server, Router, Switch, Firewall, Person
Sequence-diagram helpers: lifeline, message_arrow
Animation helpers: send_packet, connect, step_caption

NOTE: this file was reassembled from an earlier working session. Diff it
against any local copy you already have before relying on it — a few
icon classes (Cloud, Database, LoadBalancer, DNSServer, Lock) were
mentioned in that session's README but aren't reproduced below; add them
here as you need them so every chapter keeps pulling from one library.
"""

from manim import *

# ---------------------------------------------------------------------------
# STYLE SHEET — keep colors consistent across every chapter/topic
# ---------------------------------------------------------------------------
NODE_FILL = "#1E1E2E"
NODE_STROKE = "#CDD6F4"
LABEL_COLOR = "#CDD6F4"

REQUEST_COLOR = "#89B4FA"      # outbound request (SYN, GET, ...)
RESPONSE_COLOR = "#A6E3A1"     # response / ack
ERROR_COLOR = "#F38BA8"        # error, drop, RST
RETRANSMIT_COLOR = "#FAB387"   # retransmit / retry / timeout
SECURE_COLOR = "#CBA6F7"       # encrypted / TLS traffic


# ---------------------------------------------------------------------------
# BASE NODE
# ---------------------------------------------------------------------------
class NetworkNode(VGroup):
    """Base class for every network icon: an `icon` VGroup plus a text
    label placed underneath it. Subclasses build `icon` and call super()."""

    def __init__(self, label="", icon=None, label_size=22, **kwargs):
        super().__init__(**kwargs)
        self.icon = icon if icon is not None else VGroup()
        self.add(self.icon)
        if label:
            self.label_text = Text(label, font_size=label_size, color=LABEL_COLOR)
            self.label_text.next_to(self.icon, DOWN, buff=0.15)
            self.add(self.label_text)
        else:
            self.label_text = None


# ---------------------------------------------------------------------------
# ICONS
# ---------------------------------------------------------------------------
class Host(NetworkNode):
    """A desktop/client icon: monitor screen on a stand and base."""

    def __init__(self, label="Client", **kwargs):
        screen = RoundedRectangle(
            corner_radius=0.08, width=1.0, height=0.7,
            fill_color=NODE_FILL, fill_opacity=1, stroke_color=NODE_STROKE,
        )
        stand = Rectangle(
            width=0.25, height=0.15, fill_color=NODE_STROKE,
            fill_opacity=1, stroke_width=0,
        ).next_to(screen, DOWN, buff=0)
        base = Rectangle(
            width=0.5, height=0.06, fill_color=NODE_STROKE,
            fill_opacity=1, stroke_width=0,
        ).next_to(stand, DOWN, buff=0)
        icon = VGroup(screen, stand, base)
        super().__init__(label=label, icon=icon, **kwargs)


class Server(NetworkNode):
    """A rack server: stacked bars with a status LED on each."""

    def __init__(self, label="Server", bars=3, **kwargs):
        stack = VGroup()
        for i in range(bars):
            bar = RoundedRectangle(
                corner_radius=0.04, width=0.9, height=0.22,
                fill_color=NODE_FILL, fill_opacity=1, stroke_color=NODE_STROKE,
            )
            led = Dot(radius=0.04, color=RESPONSE_COLOR).move_to(
                bar.get_left() + RIGHT * 0.15
            )
            row = VGroup(bar, led)
            if i > 0:
                row.next_to(stack[-1], DOWN, buff=0.05)
            stack.add(row)
        super().__init__(label=label, icon=stack, **kwargs)


class Router(NetworkNode):
    """A router: a circle body with antenna-like connector lines."""

    def __init__(self, label="Router", **kwargs):
        body = Circle(radius=0.42, fill_color=NODE_FILL, fill_opacity=1, stroke_color=NODE_STROKE)
        arrows = VGroup(
            *[
                Line(ORIGIN, 0.25 * d, stroke_color=NODE_STROKE, stroke_width=3)
                .move_to(body.get_center() + 0.55 * d)
                for d in (UP, DOWN, LEFT, RIGHT)
            ]
        )
        icon = VGroup(body, arrows)
        super().__init__(label=label, icon=icon, **kwargs)


class Switch(NetworkNode):
    """A network switch: a rectangle with a row of port squares."""

    def __init__(self, label="Switch", ports=5, **kwargs):
        body = RoundedRectangle(
            corner_radius=0.06, width=1.1, height=0.4,
            fill_color=NODE_FILL, fill_opacity=1, stroke_color=NODE_STROKE,
        )
        dots = VGroup(
            *[Square(side_length=0.08, fill_color=NODE_STROKE, fill_opacity=1, stroke_width=0)
              for _ in range(ports)]
        ).arrange(RIGHT, buff=0.08).move_to(body.get_center())
        icon = VGroup(body, dots)
        super().__init__(label=label, icon=icon, **kwargs)


class Firewall(NetworkNode):
    """A firewall: a brick-wall pattern rectangle."""

    def __init__(self, label="Firewall", rows=3, cols=3, **kwargs):
        brick_w, brick_h = 0.32, 0.18
        wall = VGroup()
        for r in range(rows):
            offset = brick_w / 2 if r % 2 else 0
            for c in range(cols):
                brick = Rectangle(
                    width=brick_w - 0.02, height=brick_h - 0.02,
                    fill_color=ERROR_COLOR, fill_opacity=0.85, stroke_color=NODE_STROKE,
                    stroke_width=1,
                ).move_to([c * brick_w + offset, r * brick_h, 0])
                wall.add(brick)
        wall.move_to(ORIGIN)
        super().__init__(label=label, icon=wall, **kwargs)


class Person(NetworkNode):
    """A person icon, for human-protocol examples (round head + simple body)."""

    def __init__(self, label="", skin_color="#F4C299", **kwargs):
        head = Circle(radius=0.22, fill_color=skin_color, fill_opacity=1, stroke_color=NODE_STROKE)
        body = Polygon(
            [-0.32, -0.5, 0], [0.32, -0.5, 0], [0.2, -0.02, 0], [-0.2, -0.02, 0],
            fill_color=NODE_STROKE, fill_opacity=1, stroke_width=0,
        )
        body.next_to(head, DOWN, buff=0.02)
        icon = VGroup(body, head)
        super().__init__(label=label, icon=icon, **kwargs)


# ---------------------------------------------------------------------------
# LINKS / PACKETS
# ---------------------------------------------------------------------------
def connect(node_a, node_b, color=NODE_STROKE, stroke_width=2):
    """A static line representing a physical/logical link between two nodes."""
    return Line(node_a.icon.get_center(), node_b.icon.get_center(),
                color=color, stroke_width=stroke_width, z_index=-1)


def send_packet(from_node, to_node, label="", color=REQUEST_COLOR, run_time=1.0, label_size=20):
    """Animate a small labeled packet traveling from one node to another.
    Returns a list of animations — call with self.play(*send_packet(...))."""
    packet = RoundedRectangle(
        corner_radius=0.05, width=0.9, height=0.35,
        fill_color=color, fill_opacity=1, stroke_width=0,
    ).move_to(from_node.icon.get_center())
    tag = Text(label, font_size=label_size, color="#11111B").move_to(packet.get_center())
    group = VGroup(packet, tag)

    path = Line(from_node.icon.get_center(), to_node.icon.get_center())
    return [
        FadeIn(group, run_time=0.2),
        MoveAlongPath(group, path, run_time=run_time, rate_func=smooth),
        FadeOut(group, run_time=0.2),
    ]


def step_caption(text, font_size=24, color=LABEL_COLOR):
    """A short on-screen narration line for a single protocol step."""
    return Text(text, font_size=font_size, color=color)


# ---------------------------------------------------------------------------
# SEQUENCE / LADDER DIAGRAM HELPERS
# (for protocol-exchange topics: human vs. computer protocol, handshakes
# drawn as a message sequence rather than a moving packet, etc.)
# ---------------------------------------------------------------------------
def lifeline(node, length=4.0, color=NODE_STROKE):
    """A dashed vertical line dropping from a node's icon, representing that
    participant's timeline in a sequence/ladder diagram."""
    start = node.icon.get_bottom()
    end = start + DOWN * length
    return DashedLine(start, end, color=color, stroke_width=1.5, dash_length=0.1)


def message_arrow(x_start, x_end, y, label="", color=REQUEST_COLOR, label_size=20):
    """A single labeled, persistent arrow in a sequence/ladder diagram
    (unlike send_packet, this doesn't move or fade — it stays on screen as
    a record of 'this message was sent at this point in time')."""
    arrow = Arrow([x_start, y, 0], [x_end, y, 0], buff=0, stroke_width=3,
                  color=color, max_tip_length_to_length_ratio=0.15)
    lbl = Text(label, font_size=label_size, color=LABEL_COLOR)
    lbl.next_to(arrow, UP, buff=0.08)
    return VGroup(arrow, lbl)
