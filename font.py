def split_hangul(syllable):
    i = ord(syllable) - 0xac00
    i, trail = divmod(i, 28)
    lead, vowel = divmod(i, 21)
    return lead, vowel, trail

def map_vowel(i):
    first = 'ㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ'
    second = 'ㅏㅐㅑㅒㅓㅔㅕㅖㅗㅛㅜㅠㅡㅣ'
    return second.index(first[i])

def map_trail(i):
    first = 'ㄱㄲㄳㄴㄵㄶㄷㄹㄺㄻㄼㄽㄾㄿㅀㅁㅂㅄㅅㅆㅇㅈㅊㅋㅌㅍㅎ'
    second = 'ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ'
    return second.index(first[i])

def hangul_to_glyph(hangul):
    result = []
    for syllable in hangul:
        lead, vowel, trail = split_hangul(syllable)
        result.append(lead)
        result.append(map_vowel(vowel) + 19)
        if trail != 0:
            result.append(map_trail(trail - 1))
    return result

def read_font(filename, size, num_glyphs):
    with open(filename) as f:
        content = f.read()
    glyph_size = size * size * 2 + 1
    file_size = glyph_size * num_glyphs - 1
    assert len(content) == file_size
    result = []
    for c in range(num_glyphs):
        glyph = []
        for y in range(size):
            row = []
            for x in range(size):
                i = c * glyph_size + y * size * 2 + x * 2
                row.append(content[i] != '.')
            glyph.append(row)
        result.append(glyph)
    return result

def print_font(font, size, glyphs):
    for c in glyphs:
        for y in range(size):
            for x in range(size):
                on = font[c][y][x]
                dot = 'o' if on else '.'
                print(dot, end='')
            print()
        print()

def draw_font(font, size, multiplier, glyphs):
    point = size * multiplier
    spacing = size
    margin = size
    glyph_width = point + spacing
    num_glyphs = len(glyphs)
    width = glyph_width * num_glyphs - spacing + margin * 2
    height = point + margin * 2
    from PIL import Image, ImageDraw
    image = Image.new('1', (width, height), 1)
    draw = ImageDraw.Draw(image)
    for i, c in enumerate(glyphs):
        for y in range(size):
            for x in range(size):
                on = font[c][y][x]
                x1 = glyph_width * i + x * multiplier + margin
                y1 = y * multiplier + margin
                x2 = x1 + multiplier
                y2 = y1 + multiplier
                p1 = x1, y1
                p2 = x2, y2
                color = 0 if on else 1
                draw.rectangle((p1, p2), fill=color)
    return image

if __name__ == '__main__':
    import sys
    filename = sys.argv[1]
    size = int(sys.argv[2])
    multiplier = int(sys.argv[3])
    num_glyphs = int(sys.argv[4])
    font = read_font(filename, size, num_glyphs)
    glyphs = range(num_glyphs)
    image = draw_font(font, size, multiplier, glyphs)
    image.save(filename + '.png')
