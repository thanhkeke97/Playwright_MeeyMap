"""
YOLO + Template Matching engine.
Converted from core/YOLOTemplateSearch.py (Robot Framework version).
Standalone Python module - no Robot dependency.
"""
from __future__ import annotations

import json
import os
import random
from decimal import Decimal, ROUND_DOWN
from pathlib import Path

import cv2
import numpy as np
import torch
from ultralytics import YOLO


class YOLOTemplateSearch:
    CV_THREADS = 1
    TORCH_THREADS = 1
    NUM_SCALES = 9
    SCALE_MIN = 0.6
    SCALE_MAX = 1.4

    def __init__(
        self,
        model_path: str = "yolo11n.pt",
        seed: int = 42,
        thresh_hold_path: str = "config/thresh_hold.json",
    ):
        self._set_deterministic(seed)
        self._configure_runtime_threads()
        self.seed = seed
        self.model = YOLO(model_path)
        self._thresh_hold_path = thresh_hold_path
        print(f"Loaded YOLO model: {model_path} (deterministic seed={seed})")

    # ── Public API ──────────────────────────────────────────────────────────

    def compare_full_screenshots(
        self,
        first_image_path: str,
        second_image_path: str,
        template_threshold: float = 0.9,
        min_template_threshold: float = 0.8,
        max_results: int = 1,
    ) -> list[list[int]]:
        """So sánh 2 screenshot toàn màn hình."""
        first_image = cv2.imread(first_image_path)
        second_image = cv2.imread(second_image_path)

        if first_image is None or second_image is None:
            print("❌ Không thể load ảnh để so sánh full screenshot!")
            return []

        if first_image.shape != second_image.shape:
            print("⚠️ Hai screenshot khác kích thước.")
            return []

        actual_min = 0.1 if float(min_template_threshold) == 0 else min_template_threshold
        potential = self._template_match_multi_scale(
            first_image, second_image, actual_min, "FULL_SCREENSHOT_COMPARE"
        )
        filtered = self._run_adaptive_threshold(
            potential, template_threshold, actual_min, max_results
        )
        return self._build_return_payload(filtered)

    def find_small_image_in_large(
        self,
        large_image_path: str,
        small_template_path: str,
        target_class: str | None = None,
        template_threshold: float = 0.9,
        yolo_confidence: float = 0.3,
        max_results: int = 50,
        min_template_threshold: float = 0.1,
    ) -> list[list[int]]:
        """Tìm ảnh nhỏ trong ảnh lớn sử dụng YOLO + Template Matching."""
        is_calibration = float(min_template_threshold) == 0
        actual_min = 0.1 if is_calibration else min_template_threshold

        large_image = cv2.imread(large_image_path)
        template = cv2.imread(small_template_path)

        if large_image is None or template is None:
            print("❌ Không thể load ảnh!")
            return []

        print(f"Ảnh lớn : {large_image.shape}")
        print(f"Template: {template.shape}")

        potential_matches: list[dict] = []

        # YOLO detect
        print("\n🔍 YOLO đang detect objects...")
        self._set_deterministic(self.seed)
        results = self.model(large_image_path, conf=float(yolo_confidence), workers=0, verbose=False)

        candidate_regions: list[dict] = []
        for result in results:
            boxes = result.boxes
            if boxes is None:
                continue
            for box in boxes:
                class_id = int(box.cls[0].cpu().numpy())
                class_name = self.model.names[class_id]
                confidence = float(box.conf[0].cpu().numpy())

                if target_class and class_name.lower() != target_class.lower():
                    continue

                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy().astype(int)
                margin = 20
                x1 = max(0, x1 - margin)
                y1 = max(0, y1 - margin)
                x2 = min(large_image.shape[1], x2 + margin)
                y2 = min(large_image.shape[0], y2 + margin)

                roi = large_image[y1:y2, x1:x2]
                if roi.size == 0:
                    continue

                candidate_regions.append({
                    "roi": roi,
                    "bbox": (x1, y1, x2, y2),
                    "yolo_confidence": confidence,
                    "class": class_name,
                    "region_id": len(candidate_regions),
                })

        print(f"✅ YOLO tìm thấy {len(candidate_regions)} candidate regions")

        # Template matching
        potential_matches.extend(
            self._template_match_multi_scale(large_image, template, actual_min, "FULL_IMAGE")
        )
        for region in candidate_regions:
            roi_matches = self._template_match_multi_scale(
                region["roi"], template, actual_min,
                f"YOLO_{region['class']}", region["bbox"],
            )
            potential_matches.extend(roi_matches)

        filtered = self._run_adaptive_threshold(
            potential_matches, template_threshold, actual_min, max_results
        )
        return self._build_return_payload(filtered)

    # ── Private helpers ─────────────────────────────────────────────────────

    @staticmethod
    def _set_deterministic(seed: int = 42):
        random.seed(seed)
        np.random.seed(seed)
        torch.manual_seed(seed)
        if torch.cuda.is_available():
            torch.cuda.manual_seed(seed)
            torch.cuda.manual_seed_all(seed)
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False

    def _configure_runtime_threads(self):
        cv2.setNumThreads(self.CV_THREADS)
        torch.set_num_threads(self.TORCH_THREADS)
        try:
            torch.set_num_interop_threads(self.TORCH_THREADS)
        except RuntimeError:
            pass

    @staticmethod
    def _to_decimal(value) -> Decimal:
        if isinstance(value, Decimal):
            return value
        return Decimal(str(value))

    def _run_adaptive_threshold(self, potential_matches, template_threshold,
                                actual_min_threshold, max_results):
        STEP = Decimal("0.05")
        current_thresh = self._to_decimal(template_threshold)
        min_thresh = self._to_decimal(actual_min_threshold)
        max_thresh = Decimal("1.00")

        filtered_matches: list[dict] = []
        best_multiple_matches: list[dict] = []
        tried: set[Decimal] = set()

        while True:
            if current_thresh in tried:
                break
            tried.add(current_thresh)

            thresh_float = float(current_thresh)
            matches = [m for m in potential_matches if m["confidence"] >= thresh_float]
            filtered_matches = self._filter_and_rank_matches(matches, max_results)
            num = len(filtered_matches)

            print(f"📊 Thử threshold {current_thresh} -> {num} kết quả")

            if num == 1:
                break
            if num > 1:
                best_multiple_matches = filtered_matches
                if current_thresh >= max_thresh:
                    break
                current_thresh = min(max_thresh, current_thresh + STEP)
                continue
            if current_thresh <= min_thresh:
                break
            current_thresh = max(min_thresh, current_thresh - STEP)

        if not filtered_matches and best_multiple_matches:
            filtered_matches = best_multiple_matches

        return filtered_matches

    def _build_return_payload(self, filtered_matches: list[dict]) -> list[list[int]]:
        all_centers = [list(m["center"]) for m in filtered_matches]
        for i, m in enumerate(filtered_matches):
            x1, y1, x2, y2 = m["bbox"]
            print(f"\n🎯 MATCH #{i + 1}:")
            print(f"   📍 Vị trí : ({x1}, {y1}) -> ({x2}, {y2})")
            print(f"   🎯 Tâm    : {m['center']}")
            print(f"   📊 Confidence: {m['confidence']:.4f}")
            print(f"   📏 Scale  : {m['scale']:.4f}")
            print(f"   📂 Source : {m['source']}")
        print(f"\n📍 Danh sách tọa độ: {all_centers}")
        return all_centers

    def _template_match_multi_scale(self, search_image, template, threshold,
                                    source_name, offset=(0, 0)):
        if search_image.size == 0:
            return []

        search_gray = cv2.cvtColor(search_image, cv2.COLOR_BGR2GRAY)
        template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

        h_t, w_t = template_gray.shape[:2]
        h_s, w_s = search_gray.shape[:2]

        scales = np.linspace(self.SCALE_MIN, self.SCALE_MAX, self.NUM_SCALES)
        matches: list[dict] = []

        for scale in scales:
            new_w = round(w_t * scale)
            new_h = round(h_t * scale)
            if new_w >= w_s or new_h >= h_s or new_w < 5 or new_h < 5:
                continue

            resized = cv2.resize(template_gray, (new_w, new_h), interpolation=cv2.INTER_AREA)
            result = cv2.matchTemplate(search_gray, resized, cv2.TM_CCOEFF_NORMED)
            locations = np.where(result >= float(threshold))

            for pt in zip(*locations[::-1]):
                x, y = int(pt[0]), int(pt[1])
                confidence = float(result[y, x])
                cx = x + new_w // 2 + int(offset[0])
                cy = y + new_h // 2 + int(offset[1])
                matches.append({
                    "center": (cx, cy),
                    "bbox": (
                        x + int(offset[0]),
                        y + int(offset[1]),
                        x + new_w + int(offset[0]),
                        y + new_h + int(offset[1]),
                    ),
                    "confidence": confidence,
                    "scale": scale,
                    "source": source_name,
                })

        return matches

    @staticmethod
    def _filter_and_rank_matches(matches: list[dict], max_results: int) -> list[dict]:
        if not matches:
            return []
        matches.sort(key=lambda m: m["confidence"], reverse=True)

        filtered: list[dict] = []
        for m in matches:
            is_dup = False
            for existing in filtered:
                dx = abs(m["center"][0] - existing["center"][0])
                dy = abs(m["center"][1] - existing["center"][1])
                if dx < 30 and dy < 30:
                    is_dup = True
                    break
            if not is_dup:
                filtered.append(m)
            if len(filtered) >= max_results:
                break

        return filtered
