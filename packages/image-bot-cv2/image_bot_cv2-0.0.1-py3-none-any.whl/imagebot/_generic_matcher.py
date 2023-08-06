from typing import List, Union
from ._template_matcher import TemplateMatcher
from ._feature_matcher import FeatureMatcher
from ._results import MatchingResult


class GenericMatcher(TemplateMatcher):
    def find_all_results(self) -> List[MatchingResult]:
        results = super().find_all_results()
        if not results:
            feature_matcher = FeatureMatcher(
                self.image, self.template, self.convert_2_gray
            )
            return feature_matcher.find_all_results()
        else:
            return results

    def find_best_result(self) -> Union[MatchingResult, None]:
        result = super().find_best_result()
        if result is None:
            feature_matcher = FeatureMatcher(
                self.image, self.template, self.convert_2_gray
            )
            return feature_matcher.find_best_result()
        else:
            return result
