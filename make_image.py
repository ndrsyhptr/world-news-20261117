"""Render the original editorial artwork. Pillow is a build dependency only."""

from functools import lru_cache
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

SIZE = 1024
SCALE = 2
PAPER = '#f6f2e9'
WHITE = '#fffdf7'
INK = '#172d32'
TEAL = '#12635e'
RUST = '#a33d2a'
MINT = '#a9e2cb'
GOLD = '#f1bd6c'
LINE = '#cfc9bb'
SERIF = 'DejaVuSerif-Bold.ttf'
CONDENSED_SERIF = 'DejaVuSerifCondensed-Bold.ttf'
SANS = 'LiberationSans-Bold.ttf'
REGULAR = 'LiberationSans-Regular.ttf'

TILES = (
    ('BAHRAIN', ('Bahrain intercepts', 'Iranian drones'), 'U.S. radar was the stated target.', 'radar', RUST),
    ('MANILA, PHILIPPINES', ('Quad leaders meet', 'in Manila'), 'Talks cover critical mineral supplies.', 'minerals', TEAL),
    ('SHENZHEN, CHINA', ('Canada and China', 'expand tariff relief'), 'Pork, seafood, steel and aluminum.', 'trade', TEAL),
    ('ANTALYA, TÜRKİYE', ('COP31 negotiators', 'seek climate deal'), 'The UN summit enters its final week.', 'climate', RUST),
    ('MAPUTO, MOZAMBIQUE', ('Opposition leader Mondlane goes on trial',), 'Charges stem from protests after the disputed 2024 election.', 'court', TEAL),
)


@lru_cache(maxsize=None)
def font(family, size):
    return ImageFont.truetype(family, size * SCALE)


def scaled(values):
    return tuple(round(v * SCALE) for v in values)


class Poster:
    def __init__(self):
        self.image = Image.new('RGB', (SIZE * SCALE, SIZE * SCALE), PAPER)
        self.draw = ImageDraw.Draw(self.image)

    def rect(self, box, fill):
        self.draw.rectangle(scaled(box), fill=fill)

    def ellipse(self, box, fill=None, stroke=None, width=2):
        self.draw.ellipse(scaled(box), fill=fill, outline=stroke, width=width * SCALE)

    def path(self, points, color, width=3):
        self.draw.line([scaled(p) for p in points], fill=color, width=width * SCALE, joint='curve')

    def polygon(self, points, color):
        self.draw.polygon([scaled(p) for p in points], fill=color)

    def text(self, xy, words, family, size, color, right, bottom):
        style = font(family, size)
        x, y = scaled(xy)
        l, t, r, b = self.draw.textbbox((0, 0), words, font=style)
        if x + r - l > right * SCALE or y + b - t > bottom * SCALE:
            raise ValueError(f'Text exceeds its layout box: {words}')
        self.draw.text((x - l, y - t), words, font=style, fill=color)

    def bridge(self):
        self.ellipse((649, 194, 946, 491), fill='#214047')
        self.ellipse((663, 208, 932, 477), stroke='#49706e')
        self.ellipse((817, 237, 881, 301), fill=GOLD)
        for y, start, end in ((404, 666, 928), (425, 682, 912), (446, 706, 888)):
            self.path(((start, y), (end, y)), '#49706e', 2)
        for x in (705, 758, 860, 901):
            self.rect((x, 349, x + 9, 406), MINT)
        self.draw.arc(scaled((689, 275, 823, 398)), 185, 322, fill=MINT, width=7 * SCALE)
        self.draw.arc(scaled((827, 291, 924, 402)), 213, 357, fill=MINT, width=7 * SCALE)
        self.polygon(((668, 342), (799, 342), (788, 355), (668, 355)), WHITE)
        self.polygon(((837, 353), (927, 342), (927, 355), (828, 369)), WHITE)
        self.polygon(((803, 375), (822, 382), (821, 390), (800, 384)), GOLD)

    def icon(self, x, y, kind, accent):
        self.ellipse((x, y, x + 54, y + 54), fill=accent)

        def stroke(*points):
            self.path([(x + a, y + b) for a, b in points], WHITE)

        def ring(a, b, radius):
            self.ellipse((x + a - radius, y + b - radius, x + a + radius, y + b + radius), stroke=WHITE)

        if kind == 'radar':
            ring(27, 27, 15)
            ring(27, 27, 8)
            stroke((27, 27), (40, 16))
        elif kind == 'minerals':
            stroke((14, 23), (22, 13), (34, 13), (41, 23), (27, 42), (14, 23), (41, 23))
            stroke((22, 13), (27, 42), (34, 13))
        elif kind == 'trade':
            stroke((13, 20), (40, 20), (34, 14))
            stroke((41, 34), (14, 34), (20, 40))
        elif kind == 'climate':
            ring(27, 27, 15)
            self.ellipse((x + 20, y + 12, x + 34, y + 42), stroke=WHITE)
            stroke((13, 27), (41, 27))
        elif kind == 'court':
            stroke((12, 23), (27, 13), (42, 23), (12, 23))
            for a in (18, 27, 36):
                stroke((a, 26), (a, 37))
            stroke((12, 41), (42, 41))

    def masthead(self):
        self.rect((36, 27, 988, 31), INK)
        self.text((36, 44), 'WORLD NEWS', SERIF, 71, INK, 935, 109)
        self.text((39, 111), 'TUESDAY 17 NOVEMBER 2026', SANS, 32, TEAL, 988, 143)
        self.rect((930, 54, 988, 61), RUST)
        self.rect((949, 67, 988, 74), RUST)

    def lead(self):
        self.rect((36, 154, 988, 549), INK)
        self.rect((65, 198, 105, 203), GOLD)
        self.text((65, 215), 'OCCUPIED CRIMEA', SANS, 26, MINT, 629, 249)
        for y, words in zip((272, 346), ('Ukraine damages', 'Kerch Bridge')):
            self.text((61, y), words, CONDENSED_SERIF, 66, WHITE, 645, y + 70)
        self.text((65, 455), 'A key link from occupied Crimea to Russia.', REGULAR, 29, WHITE, 633, 489)
        self.bridge()

    def tile(self, x, y, width, height, item):
        location, headlines, detail, kind, accent = item
        self.rect((x, y, x + width, y + height), WHITE)
        self.rect((x, y, x + width, y + 2), LINE)
        self.rect((x, y, x + 5, y + height), accent)
        self.icon(x + width - 70, y + 11, kind, accent)
        self.text((x + 18, y + 13), location, SANS, 24, accent, x + width - 78, y + 41)
        for i, text in enumerate(headlines):
            self.text((x + 17, y + 44 + 38 * i), text, SANS, 42, INK, x + width - 15, y + height - 24)
        self.text((x + 18, y + height - 28), detail, REGULAR, 24, INK, x + width - 13, y + height - 3)

    def render(self):
        self.masthead()
        self.lead()
        for i, item in enumerate(TILES[:4]):
            self.tile(36 + (i % 2) * 485, 564 + (i // 2) * 159, 467, 148, item)
        self.tile(36, 882, 952, 111, TILES[4])
        return self.image.resize((SIZE, SIZE), Image.Resampling.LANCZOS)


def main():
    output = Path(__file__).resolve().parent / 'assets' / 'entry.png'
    output.parent.mkdir(exist_ok=True)
    Poster().render().save(output, format='PNG', optimize=True)


if __name__ == '__main__':
    main()
