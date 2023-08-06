import cv2
import numpy as np
from typing import Union, List
from ._base_matcher import BaseMatcher
from ._results import MatchingResult


class FeatureMatcher(BaseMatcher):
    def find_all_results(self) -> List[MatchingResult]:
        result = self.find_best_result()
        return [result] if result is not None else []

    def find_best_result(self) -> Union[MatchingResult, None]:
        # Initiate SIFT detector
        sift = cv2.SIFT_create()
        # find the key points and descriptors with SIFT
        if self.convert_2_gray:
            _template = cv2.cvtColor(self.template, cv2.COLOR_BGR2GRAY)
            _image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        else:
            _template = self.template
            _image = self.image
        kp_image, desc_image = sift.detectAndCompute(_image, None)
        kp_template, desc_template = sift.detectAndCompute(_template, None)
        # BFMatcher with default params
        bf = cv2.BFMatcher()
        matches = bf.knnMatch(desc_template, desc_image, k=2)
        # Apply ratio test
        match_pts = []

        def _get_good_matches(r):
            _good_pts = []
            for m, n in matches:
                if m.distance < r * n.distance:
                    _good_pts.append(m)
            return _good_pts

        ratio = 0.4
        while ratio < 0.75:
            match_pts = _get_good_matches(ratio)
            if len(match_pts) > 0:
                break
            else:
                ratio = ratio + 0.001

        h, w = self.h_template, self.w_template
        if len(match_pts) >= 4:
            # Draw a polygon around the recognized object
            src_pts = np.float32(
                [kp_template[m.queryIdx].pt for m in match_pts]
            ).reshape(-1, 1, 2)
            dst_pts = np.float32([kp_image[m.trainIdx].pt for m in match_pts]).reshape(
                -1, 1, 2
            )
            # Get the transformation matrix
            M, _ = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
            # Find the perspective transformation to get the corresponding points
            pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(
                -1, 1, 2
            )
            dst = cv2.perspectiveTransform(pts, M)
            points = np.int32(dst).tolist()
            center_x = int(sum([p[0][0] for p in points]) / len(points))
            center_y = int(sum([p[0][1] for p in points]) / len(points))
            max_x = int(max([p[0][0] for p in points]))
            min_x = int(min([p[0][0] for p in points]))
            max_y = int(max([p[0][1] for p in points]))
            min_y = int(min([p[0][1] for p in points]))
            return MatchingResult(
                center=(center_x, center_y), rect=((min_x, max_y), (max_x, min_y))
            )
        elif len(match_pts) > 0:
            points = [kp_image[m.trainIdx].pt for m in match_pts]
            center_x = int(sum([x for x, y in points]) / len(points))
            center_y = int(sum([y for x, y in points]) / len(points))
            return MatchingResult(
                center=(center_x, center_y),
                rect=(
                    (int(center_x - w / 2), int(center_y + h / 2)),
                    (int(center_x + w / 2), int(center_y - h / 2)),
                ),
            )
        else:
            return None
