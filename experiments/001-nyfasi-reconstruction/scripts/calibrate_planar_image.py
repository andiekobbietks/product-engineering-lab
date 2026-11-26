"""Rectify a planar product view using a measured rectangular scale target."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import cv2
import numpy as np

def rectify(image_path, config, output_path):
    width_mm, height_mm = float(config["target_width_mm"]), float(config["target_height_mm"])
    corners = np.asarray(config["image_corners_px"], dtype=np.float32)
    if corners.shape != (4, 2) or width_mm <= 0 or height_mm <= 0:
        raise ValueError("Expected four 2D corners and positive target dimensions")
    scale = float(config.get("pixels_per_mm", 10.0))
    width_px, height_px = round(width_mm * scale), round(height_mm * scale)
    destination = np.asarray([[0, 0], [width_px-1, 0], [width_px-1, height_px-1], [0, height_px-1]], dtype=np.float32)
    homography = cv2.getPerspectiveTransform(corners, destination)
    image = cv2.imread(str(image_path), cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError(f"Cannot read image: {image_path}")
    rectified = cv2.warpPerspective(image, homography, (width_px, height_px))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if not cv2.imwrite(str(output_path), rectified):
        raise RuntimeError(f"Could not write rectified image: {output_path}")
    return {
        "schema_version": "1.0.0", "source_image": image_path.name,
        "target_size_mm": [width_mm, height_mm], "rectified_size_px": [width_px, height_px],
        "scale_px_per_mm": scale, "homography": homography.tolist(),
        "warning": "Valid only for points on the same plane as the calibration target.",
    }

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("image", type=Path)
    parser.add_argument("calibration_json", type=Path)
    parser.add_argument("--output", type=Path, default=Path("rectified.png"))
    args = parser.parse_args()
    result = rectify(args.image, json.loads(args.calibration_json.read_text()), args.output)
    args.output.with_suffix(".calibration.json").write_text(json.dumps(result, indent=2) + "\n")
    print(f"Rectified planar view written to {args.output}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
