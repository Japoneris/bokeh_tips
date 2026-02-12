import argparse
import json
from pathlib import Path

from src.models import CVData
from src.chart import build_chart
from src.output import save_standalone_html, save_components


def main():
    parser = argparse.ArgumentParser(description="Generate CV timeline visualizations")
    parser.add_argument(
        "--config",
        default="config/cv_data.json",
        help="Path to JSON config file (default: config/cv_data.json)",
    )
    parser.add_argument(
        "--orientation",
        choices=["horizontal", "vertical"],
        default=None,
        help="Generate only one orientation (default: both)",
    )
    parser.add_argument(
        "--embed",
        action="store_true",
        help="Also produce script/div component files for blog embedding",
    )
    parser.add_argument(
        "--tap",
        action="store_true",
        help="Enable tap-to-navigate (click a bar to open its URL anchor)",
    )
    parser.add_argument(
        "--output-dir",
        default="output",
        help="Output directory (default: output/)",
    )
    args = parser.parse_args()

    config_path = Path(args.config)
    with open(config_path) as f:
        raw = json.load(f)

    data = CVData(**raw)
    output_dir = Path(args.output_dir)

    orientations = (
        [args.orientation] if args.orientation else ["horizontal", "vertical"]
    )

    for orient in orientations:
        plot = build_chart(data, orientation=orient, enable_tap=args.tap)
        html_path = output_dir / f"cv_{orient}.html"
        save_standalone_html(plot, html_path)
        print(f"Saved {html_path}")

        if args.embed:
            prefix = output_dir / f"CV_{orient}"
            save_components(plot, prefix)
            print(f"Saved {prefix}_script.txt and {prefix}_div.txt")


if __name__ == "__main__":
    main()
