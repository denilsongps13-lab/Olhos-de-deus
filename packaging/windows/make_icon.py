from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter


def main() -> None:
    output = Path("build/OlhosDeDeus.ico")
    output.parent.mkdir(parents=True, exist_ok=True)

    size = 512
    image = Image.new("RGBA", (size, size), (5, 13, 22, 255))
    glow = Image.new("RGBA", image.size, (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)
    glow_draw.ellipse((82, 138, 430, 374), outline=(44, 221, 255, 190), width=24)
    glow = glow.filter(ImageFilter.GaussianBlur(22))
    image.alpha_composite(glow)

    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((20, 20, 492, 492), radius=92, outline=(21, 80, 111, 255), width=7)
    draw.arc((80, 132, 432, 380), start=195, end=345, fill=(80, 232, 255, 255), width=18)
    draw.arc((80, 132, 432, 380), start=15, end=165, fill=(80, 232, 255, 255), width=18)
    draw.ellipse((168, 168, 344, 344), outline=(53, 165, 244, 255), width=16, fill=(7, 35, 58, 255))
    draw.ellipse((214, 214, 298, 298), fill=(62, 225, 255, 255))
    draw.ellipse((238, 238, 274, 274), fill=(235, 254, 255, 255))

    image.save(output, format="ICO", sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
    print(output)


if __name__ == "__main__":
    main()
