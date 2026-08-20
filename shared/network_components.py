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


class Cloud(NetworkNode):
    """A cloud (for 'the internet' / cloud provider), built from overlapping circles."""

    def __init__(self, label="Internet", **kwargs):
        puffs = VGroup(
            Circle(radius=0.28).shift(LEFT * 0.35 + DOWN * 0.05),
            Circle(radius=0.34).shift(UP * 0.08),
            Circle(radius=0.28).shift(RIGHT * 0.35 + DOWN * 0.05),
            Circle(radius=0.22).shift(DOWN * 0.15),
        )
        icon = VGroup(*puffs).set_fill(NODE_FILL, opacity=1).set_stroke(NODE_STROKE)
        super().__init__(label=label, icon=icon, **kwargs)


class Database(NetworkNode):
    """A database: the classic cylinder shape."""

    def __init__(self, label="Database", **kwargs):
        top = Ellipse(width=0.9, height=0.25, fill_color=NODE_FILL, fill_opacity=1, stroke_color=NODE_STROKE)
        body = Rectangle(width=0.9, height=0.5, fill_color=NODE_FILL, fill_opacity=1, stroke_width=0)
        body.next_to(top, DOWN, buff=0).align_to(top, LEFT)
        bottom = Ellipse(width=0.9, height=0.25, fill_color=NODE_FILL, fill_opacity=1, stroke_color=NODE_STROKE)
        bottom.next_to(body, DOWN, buff=-0.125)
        side_l = Line(top.get_left(), bottom.get_left(), color=NODE_STROKE)
        side_r = Line(top.get_right(), bottom.get_right(), color=NODE_STROKE)
        icon = VGroup(body, bottom, side_l, side_r, top)
        super().__init__(label=label, icon=icon, **kwargs)


class LoadBalancer(NetworkNode):
    """A load balancer: a node with arrows fanning out to represent distribution."""

    def __init__(self, label="Load Balancer", **kwargs):
        body = RoundedRectangle(
            corner_radius=0.08, width=0.6, height=0.6,
            fill_color=NODE_FILL, fill_opacity=1, stroke_color=NODE_STROKE,
        )
        fan = VGroup(
            *[Arrow(body.get_right(), body.get_right() + 0.4 * d,
                     stroke_width=2, max_tip_length_to_length_ratio=0.35, color=NODE_STROKE)
              for d in (UR, RIGHT, DR)]
        )
        icon = VGroup(body, fan)
        super().__init__(label=label, icon=icon, **kwargs)


class DNSServer(NetworkNode):
    """A DNS server: a globe (circle with latitude/longitude lines)."""

    def __init__(self, label="DNS", **kwargs):
        globe = Circle(radius=0.35, fill_color=NODE_FILL, fill_opacity=1, stroke_color=NODE_STROKE)
        meridian = Ellipse(width=0.35, height=0.7, stroke_color=NODE_STROKE, fill_opacity=0).move_to(globe.get_center())
        equator = Line(globe.get_left(), globe.get_right(), stroke_color=NODE_STROKE)
        icon = VGroup(globe, meridian, equator)
        super().__init__(label=label, icon=icon, **kwargs)


class Lock(NetworkNode):
    """A padlock, for TLS / security / encryption topics. Set `locked=False`
    to draw it sprung open (e.g. to show a completed key exchange, or a
    compromised/insecure channel depending on context)."""

    def __init__(self, label="TLS", locked=True, **kwargs):
        body = RoundedRectangle(
            corner_radius=0.05, width=0.5, height=0.4,
            fill_color=SECURE_COLOR, fill_opacity=1, stroke_width=0,
        )
        shackle = Arc(radius=0.2, start_angle=0, angle=PI, stroke_color=NODE_STROKE, stroke_width=5)
        shackle.next_to(body, UP, buff=-0.05)
        if not locked:
            shackle.shift(UP * 0.1 + RIGHT * 0.05).rotate(-PI / 6)
        icon = VGroup(body, shackle)
        super().__init__(label=label, icon=icon, **kwargs)


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


class Attacker(NetworkNode):
    """A hooded attacker figure (error-red), for security-threat topics:
    packet sniffing, IP spoofing, DoS/DDoS, botnets, etc."""

    def __init__(self, label="", **kwargs):
        hood = Polygon(
            [-0.28, -0.05, 0], [0.28, -0.05, 0], [0, 0.32, 0],
            fill_color=ERROR_COLOR, fill_opacity=1, stroke_width=0,
        )
        face = Rectangle(width=0.2, height=0.1, fill_color=NODE_FILL,
                          fill_opacity=1, stroke_width=0).move_to([0, -0.08, 0])
        body = Polygon(
            [-0.34, -0.55, 0], [0.34, -0.55, 0], [0.22, -0.05, 0], [-0.22, -0.05, 0],
            fill_color=ERROR_COLOR, fill_opacity=0.85, stroke_width=0,
        )
        icon = VGroup(body, hood, face)
        super().__init__(label=label, icon=icon, **kwargs)


# ---------------------------------------------------------------------------
# LINKS / PACKETS
# ---------------------------------------------------------------------------
def connect(node_a, node_b, color=NODE_STROKE, stroke_width=2):
    """A static line between two nodes' nearest bounding-box edges —
    call once to lay down the topology before animating packets along it."""
    return Line(node_a.get_right(), node_b.get_left(),
                color=color, stroke_width=stroke_width, z_index=-1)


def make_packet(color=REQUEST_COLOR, shape="dot", label="", label_size=16):
    """Build a small mobject representing a packet/segment/frame, with an
    optional label centered on it. `shape` is 'dot', 'square', or
    'envelope' (a small rectangle with a folded-flap top, for email/
    message-style topics)."""
    if shape == "dot":
        body = Dot(radius=0.12, color=color)
    elif shape == "square":
        body = Square(side_length=0.22, fill_color=color, fill_opacity=1, stroke_width=0)
    elif shape == "envelope":
        rect = RoundedRectangle(corner_radius=0.03, width=0.32, height=0.22,
                                 fill_color=color, fill_opacity=1, stroke_color=WHITE, stroke_width=1)
        flap1 = Line(rect.get_corner(UL), rect.get_center(), stroke_color=WHITE, stroke_width=1)
        flap2 = Line(rect.get_corner(UR), rect.get_center(), stroke_color=WHITE, stroke_width=1)
        body = VGroup(rect, flap1, flap2)
    else:
        raise ValueError(f"Unknown packet shape: {shape}")

    if not label:
        return body
    tag = Text(label, font_size=label_size, color="#11111B").move_to(body.get_center())
    return VGroup(body, tag)


def send_packet(from_node, to_node, label="", color=REQUEST_COLOR, shape="dot",
                 run_time=1.0, label_size=16, fade_after=True):
    """Animate a small labeled packet traveling from one node to another.
    Returns a list of animations — call with self.play(*send_packet(...)).

        self.play(*send_packet(client, server, "SYN", color=REQUEST_COLOR))
        self.play(*send_packet(attacker, target, "", color=ERROR_COLOR, shape="square"))
    """
    group = make_packet(color=color, shape=shape, label=label, label_size=label_size)
    group.move_to(from_node.get_right())

    path = Line(from_node.get_right(), to_node.get_left())
    anims = [
        FadeIn(group, run_time=0.2),
        MoveAlongPath(group, path, run_time=run_time, rate_func=smooth),
    ]
    if fade_after:
        anims.append(FadeOut(group, run_time=0.2))
    return anims


def pipe(width, height, label, font_size=20, fill_color="#D9DCE3"):
    """A labeled 'capacity pipe' for throughput/bandwidth diagrams. Bar
    HEIGHT encodes relative link capacity — a taller pipe carries more
    bits/sec, matching the classic 'wide pipe vs. narrow pipe' bottleneck
    intuition (e.g. pipe(4, 0.35, 'Rs bits/sec') for a slow link next to
    pipe(4, 0.9, 'Rc bits/sec') for a fast one)."""
    body = RoundedRectangle(
        corner_radius=min(height, 0.3) / 2, width=width, height=height,
        fill_color=fill_color, fill_opacity=1, stroke_color=NODE_STROKE, stroke_width=1.5,
    )
    lbl = Text(label, font_size=font_size, color=BLACK)
    lbl.move_to(body)
    return VGroup(body, lbl)


def step_caption(text, y=None, font_size=24, color=LABEL_COLOR):
    """A short on-screen narration line for a single protocol step. If `y`
    is given, the caption is centered horizontally at that fixed vertical
    position (pass the same y across a scene's steps so captions don't
    jump around) — e.g. step_caption("...", y=caption_y). If omitted, the
    caption is created unpositioned at the origin; position it yourself
    with .next_to(...) / .to_edge(...)."""
    cap = Text(text, font_size=font_size, color=color)
    if y is not None:
        cap.move_to([0, y, 0])
    return cap


def _labeled_cell(text, width, height, fill_color, font_size):
    box = Rectangle(width=width, height=height, fill_color=fill_color,
                     fill_opacity=1, stroke_color=NODE_STROKE)
    text_color = BLACK if fill_color != NODE_FILL else LABEL_COLOR
    lbl = Text(text, font_size=font_size, color=text_color)
    lbl.move_to(box)
    return VGroup(box, lbl)


def network_packet(src, dst, payload=None, src_color=NODE_STROKE, dst_color=NODE_STROKE,
                    cell_width=0.9, payload_width=1.2, height=0.4, font_size=16):
    """Build a small 'packet' visual with labeled src/dst header cells and
    an optional payload cell — for security topics (sniffing, spoofing)
    where a header field needs to be pointed at and highlighted on its
    own. Returns a VGroup with `.src_cell`, `.dst_cell`, and (if `payload`
    is given) `.payload_cell` attributes, e.g.:

        packet = network_packet("B", "A", payload="pwd:••••")
        self.play(Circumscribe(packet.payload_cell, color=ERROR_COLOR))
    """
    src_cell = _labeled_cell(f"src:{src}", cell_width, height, src_color, font_size)
    dst_cell = _labeled_cell(f"dst:{dst}", cell_width, height, dst_color, font_size)
    packet = VGroup(src_cell, dst_cell)
    payload_cell = None
    if payload is not None:
        payload_cell = _labeled_cell(payload, payload_width, height, NODE_FILL, font_size)
        packet.add(payload_cell)
    packet.arrange(RIGHT, buff=0.03)
    packet.src_cell = src_cell
    packet.dst_cell = dst_cell
    packet.payload_cell = payload_cell
    return packet


# ---------------------------------------------------------------------------
# ENCAPSULATION / LAYERING HELPERS
# (for §1.5 — Protocol Layers and Their Service Models)
# ---------------------------------------------------------------------------
LAYER_NAMES = ["Application", "Transport", "Network", "Link", "Physical"]

HT_COLOR = REQUEST_COLOR    # transport-layer header (H_t)
HN_COLOR = RESPONSE_COLOR   # network-layer header (H_n)
HL_COLOR = RETRANSMIT_COLOR  # link-layer header (H_l)


def layer_stack(names=None, width=1.8, row_height=0.5, font_size=18):
    """A vertical stack of labeled layer boxes (Application at top down to
    Physical at bottom). Indexable: stack[0] is Application ... stack[4]
    is Physical — use stack[i].get_center()[1] to read a row's y-coordinate
    for placing packets alongside it."""
    names = names or LAYER_NAMES
    rows = VGroup()
    for name in names:
        box = RoundedRectangle(corner_radius=0.05, width=width, height=row_height,
                                fill_color=NODE_FILL, fill_opacity=1, stroke_color=NODE_STROKE)
        lbl = Text(name, font_size=font_size, color=LABEL_COLOR)
        lbl.move_to(box)
        row = VGroup(box, lbl)
        if len(rows) > 0:
            row.next_to(rows[-1], DOWN, buff=0.08)
        rows.add(row)
    return rows


def header_box(tag, color, width=0.4, height=0.4, font_size=18):
    """A small colored header block (e.g. H_t, H_n, H_l) for composing an
    encapsulated packet via build_packet(). `tag` is the subscript letter
    ('t', 'n', 'l', ...); the box is labeled 'H<tag>'."""
    box = Rectangle(width=width, height=height, fill_color=color, fill_opacity=1,
                     stroke_width=1, stroke_color=NODE_STROKE)
    lbl = Text(f"H{tag}", font_size=font_size, color=BLACK)
    lbl.move_to(box)
    return VGroup(box, lbl)


def message_box(label="M", width=1.2, height=0.4, font_size=18, fill_color="#D9DCE3"):
    """The application-layer message block — the payload that headers get
    wrapped around during encapsulation."""
    box = Rectangle(width=width, height=height, fill_color=fill_color, fill_opacity=1,
                     stroke_width=1, stroke_color=NODE_STROKE)
    lbl = Text(label, font_size=font_size, color=BLACK)
    lbl.move_to(box)
    return VGroup(box, lbl)


def build_packet(*boxes):
    """Arrange header/message boxes left-to-right into one packet VGroup.
    Pass headers outermost-first, e.g.:

        build_packet(header_box("l", HL_COLOR), header_box("n", HN_COLOR),
                      header_box("t", HT_COLOR), message_box())

    for a link-layer frame carrying H_l | H_n | H_t | M.
    """
    return VGroup(*boxes).arrange(RIGHT, buff=0.02)


def place_packet(packet, y, right_x):
    """Position a packet VGroup so its right edge sits at x = right_x and
    its vertical center is at y. Keeps the message block visually anchored
    while headers grow/shrink to its left across encapsulation stages."""
    packet.move_to([right_x, y, 0])
    packet.shift(RIGHT * (right_x - packet.get_right()[0]))
    return packet


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
