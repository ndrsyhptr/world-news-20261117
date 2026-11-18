from pathlib import Path
from shutil import copyfile


def main():
    image = Path(__file__).resolve().parent / "assets" / "entry.png"
    output_dir = Path("/output")
    output_dir.mkdir(parents=True, exist_ok=True)
    # Copy the published artwork byte for byte, without an image codec.
    copyfile(image, output_dir / "entry.png")


if __name__ == "__main__":
    main()
