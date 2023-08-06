from typing import List
from ._results import MatchingResult


class BaseMatcher:
    def __init__(self, image, template, convert_2_gray=True):
        self.image = image
        self.template = template
        assert self.image is not None, "Image should not be None"
        assert self.template is not None, "Image template should not be None"
        self.h_image, self.w_image = self.image.shape[:2]
        self.h_template, self.w_template = self.template.shape[:2]
        assert (
            self.h_image >= self.h_template and self.w_image >= self.w_template
        ), "Image template should be smaller than image source."
        self.convert_2_gray = convert_2_gray

    def find_best_result(self) -> MatchingResult:
        """
        TODO
        """

    def find_all_results(self) -> List[MatchingResult]:
        """
        TODO
        """
