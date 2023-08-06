import cv2


class ImageCompare:
    def __init__(self, image_source, image_ref, convert_2_gray=True):
        self.image_source = image_source
        self.image_ref = image_ref
        assert self.image_source is not None, "Image source should not be None"
        assert self.image_ref is not None, "Image reference should not be None"
        self.h_image_source, self.w_image_source = self.image_source.shape[:2]
        self.h_image_ref, self.w_image_ref = self.image_ref.shape[:2]
        self.convert_2_gray = convert_2_gray

    def get_similarity(self) -> float:
        image_source, image_ref = self.image_source.copy(), self.image_ref.copy()
        same_size_ref = cv2.resize(
            image_ref, image_source.shape[:2][::-1], interpolation=cv2.INTER_NEAREST
        )
        if self.convert_2_gray:
            same_size_ref = cv2.cvtColor(same_size_ref, cv2.COLOR_BGR2GRAY)
            image_source = cv2.cvtColor(image_source, cv2.COLOR_BGR2GRAY)
        res = cv2.matchTemplate(image_source, same_size_ref, cv2.TM_CCOEFF_NORMED)
        _, confidence, _, _ = cv2.minMaxLoc(res)
        return confidence
