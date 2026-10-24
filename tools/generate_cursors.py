#!/usr/bin/env python3
"""
Generate the AuraCursor XCursor theme in pure Python (no xcursorgen needed).

Draws a blue-glass arrow, I-beam, hand, move, not-allowed and an animated
"watch" spinner, writing real XCursor binary files.
Run: python3 tools/generate_cursors.py
"""
import math
import os
import struct

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                    "rootfs", "usr", "share", "icons", "AuraCursor", "cursors")
SIZE = 32          # pixel canvas
NOMINAL = 24       # nominal size advertised in the file

NAVY = (10, 26, 58, 255)
WHITE = (255, 255, 255, 255)
BLUE = (47, 127, 224, 255)
CYAN = (86, 199, 242, 255)


class Canvas:
    def __init__(self, w=SIZE, h=SIZE):
        self.w, self.h = w, h
        self.px = [(0, 0, 0, 0)] * (w * h)

    def set(self, x, y, color):
        if 0 <= x < self.w and 0 <= y < self.h:
            self.px[y * self.w + x] = color

    def polygon(self, pts, color):
        minx = int(min(p[0] for p in pts)); maxx = int(max(p[0] for p in pts))
        miny = int(min(p[1] for p in pts)); maxy = int(max(p[1] for p in pts))
        for y in range(miny, maxy + 1):
            for x in range(minx, maxx + 1):
                if self._inside(x + 0.5, y + 0.5, pts):
                    self.set(x, y, color)

    @staticmethod
    def _inside(x, y, pts):
        inside, n, j = False, len(pts), len(pts) - 1
        for i in range(n):
            xi, yi = pts[i]; xj, yj = pts[j]
            if ((yi > y) != (yj > y)) and \
               (x < (xj - xi) * (y - yi) / (yj - yi) + xi):
                inside = not inside
            j = i
        return inside

    def circle(self, cx, cy, r, color, ring=None):
        for y in range(self.h):
            for x in range(self.w):
                d = math.hypot(x - cx, y - cy)
                if ring is None and d <= r:
                    self.set(x, y, color)
                elif ring is not None and abs(d - r) <= ring:
                    self.set(x, y, color)

    def line(self, x1, y1, x2, y2, color, width=1.6):
        steps = int(max(abs(x2 - x1), abs(y2 - y1)) * 2) + 1
        for i in range(steps + 1):
            t = i / steps
            x, y = x1 + (x2 - x1) * t, y1 + (y2 - y1) * t
            for dy in range(-int(width), int(width) + 1):
                for dx in range(-int(width), int(width) + 1):
                    if math.hypot(dx, dy) <= width:
                        self.set(int(x + dx), int(y + dy), color)


def arrow(scale=1.0, fill=WHITE, outline=NAVY):
    c = Canvas()
    pts = [(6, 3), (6, 25), (12, 20), (15.5, 28), (19, 26.4), (15.8, 18.6),
           (23.5, 18.6)]
    big = [(x - 0.9, y - 0.9) for x, y in pts]
    c.polygon([(x + (0.9 if x > 12 else -0.9), y + (0.9 if y > 14 else -0.9))
               for x, y in pts], outline)
    c.polygon(pts, fill)
    # blue tip shine
    for i in range(5):
        c.set(7, 5 + i, BLUE if i < 2 else CYAN)
    return c


def ibeam():
    c = Canvas()
    for x in range(9, 24):
        c.polygon([(x, 5), (x + 1, 5), (x + 1, 7), (x, 7)], NAVY)
        c.polygon([(x, 25), (x + 1, 25), (x + 1, 27), (x, 27)], NAVY)
    c.line(16, 6, 16, 26, NAVY, 1.4)
    c.line(16, 6, 16, 26, WHITE, 0.5)
    return c


def hand():
    c = Canvas()
    # simplified pointing hand: rounded rect palm + index finger
    c.polygon([(13, 30), (13, 14), (15, 4), (18, 4), (19, 13), (21, 8),
               (24, 9), (24, 14), (26, 11), (28.5, 13), (27, 24),
               (24, 30)], NAVY)
    c.polygon([(14.2, 29), (14.2, 14.5), (16, 5.6), (17.6, 5.6), (18.2, 13.4),
               (21.5, 9.6), (23.2, 10.4), (23.2, 15.5), (25, 12.8),
               (26.9, 14.1), (25.7, 23.4), (23.4, 29)], WHITE)
    return c


def move():
    c = Canvas()
    cx, cy = 16, 16
    for dx, dy in ((0, -1), (0, 1), (-1, 0), (1, 0)):
        c.line(cx, cy, cx + dx * 11, cy + dy * 11, NAVY, 2.2)
        tip = [(cx + dx * 14, cy + dy * 14),
               (cx + dx * 8 - dy * 4, cy + dy * 8 - dx * 4),
               (cx + dx * 8 + dy * 4, cy + dy * 8 + dx * 4)]
        c.polygon(tip, NAVY)
        c.line(cx, cy, cx + dx * 11, cy + dy * 11, WHITE, 0.8)
    return c


def not_allowed():
    c = Canvas()
    c.circle(16, 16, 11, NAVY, ring=2.6)
    c.circle(16, 16, 11, WHITE, ring=1.2)
    c.line(8, 8, 24, 24, NAVY, 2.2)
    c.line(8, 8, 24, 24, (227, 93, 106, 255), 1.1)
    return c


def watch_frame(phase):
    c = Canvas()
    a0 = math.radians(phase * 45)
    for y in range(SIZE):
        for x in range(SIZE):
            d = math.hypot(x - 16, y - 16)
            if abs(d - 10) <= 3:
                ang = math.atan2(y - 16, x - 16)
                rel = (a0 - ang) % (2 * math.pi)
                if rel < 4.2:  # trailing arc fades out
                    alpha = int(255 * max(0.15, 1 - rel / 4.2))
                    c.set(x, y, (56, 150, 235, alpha))
    return c


def write_xcursor(path, frames, xhot, yhot, delay=0):
    """frames: list[Canvas]; writes an (animated) XCursor file."""
    n = len(frames)
    header_size = 16
    toc_size = 12 * n
    chunks = []
    pos = header_size + toc_size
    for fr in frames:
        img = struct.pack("<IIIIIIIII", 36, 0xfffd0002, NOMINAL, 1,
                          fr.w, fr.h, xhot, yhot, delay)
        raw = b"".join(struct.pack("BBBB", b, g, r, a)
                       for (r, g, b, a) in fr.px)
        chunks.append((pos, img + raw))
        pos += len(img) + len(raw)
    out = struct.pack("<IIII", 0x72756358, header_size, 0x00010000, n)
    for pos_i, _ in chunks:
        out += struct.pack("<III", 0xfffd0002, NOMINAL, pos_i)
    for _, blob in chunks:
        out += blob
    with open(path, "wb") as fh:
        fh.write(out)


ALIASES = {
    "default": "left_ptr", "top_left_arrow": "left_ptr", "arrow": "left_ptr",
    "hand2": "pointer", "hand1": "pointer", "pointing_hand": "pointer",
    "xterm": "text", "ibeam": "text",
    "left_ptr_watch": "watch", "wait": "watch", "progress": "watch",
    "fleur": "move", "grabbing": "move", "grab": "move",
    "crosshair": "move", "cross": "move",
    "forbidden": "not-allowed", "circle": "not-allowed",
    "sb_h_double_arrow": "move", "sb_v_double_arrow": "move",
    "ew-resize": "move", "ns-resize": "move",
    "nwse-resize": "move", "nesw-resize": "move",
    "col-resize": "move", "row-resize": "move",
    "help": "left_ptr", "question_arrow": "left_ptr",
    "copy": "left_ptr", "alias": "left_ptr", "link": "left_ptr",
    "dnd-ask": "left_ptr", "dnd-copy": "left_ptr", "dnd-link": "left_ptr",
    "dnd-move": "move", "dnd-none": "not-allowed",
    "context-menu": "left_ptr", "cell": "move", "vertical-text": "text",
    "zoom-in": "left_ptr", "zoom-out": "left_ptr", "all-scroll": "move",
}

INDEX = """[Icon Theme]
Name=AuraCursor
Comment=AURA OS blue-glass cursor theme
Inherits=hicolor
"""


def main():
    os.makedirs(BASE, exist_ok=True)
    write_xcursor(os.path.join(BASE, "left_ptr"), [arrow()], 6, 3)
    write_xcursor(os.path.join(BASE, "pointer"), [hand()], 15, 4)
    write_xcursor(os.path.join(BASE, "text"), [ibeam()], 16, 16)
    write_xcursor(os.path.join(BASE, "move"), [move()], 16, 16)
    write_xcursor(os.path.join(BASE, "not-allowed"), [not_allowed()], 16, 16)
    write_xcursor(os.path.join(BASE, "watch"),
                  [watch_frame(i) for i in range(8)], 16, 16, delay=90)
    for alias, target in ALIASES.items():
        p = os.path.join(BASE, alias)
        if os.path.islink(p) or os.path.exists(p):
            os.remove(p)
        os.symlink(target, p)
    theme_root = os.path.dirname(BASE)
    with open(os.path.join(theme_root, "index.theme"), "w", encoding="utf-8") as fh:
        fh.write(INDEX)
    print("AuraCursor theme generated:", len(os.listdir(BASE)), "cursors")


if __name__ == "__main__":
    main()
