import os
from typing import Dict, Optional

import numpy as np
import PIL.Image

import manta_lab.util as manta_util
from manta_lab.dtypes import type_util
from manta_lab.dtypes._interface import BatchableMedia, MEDIA_TEMP_DIR


class ImageMask:
    pass


class Molecule:
    pass


class Object3D:
    pass


class Classes:
    pass


class BoundingBoxes2D:
    pass


class Image(BatchableMedia):
    """Datatype for logging images.

    Arguments:
        data_or_path: array, PIL
        #https://pillow.readthedocs.io/en/4.2.x/handbook/concepts.html#concept-modes.
        mode: (string) The PIL mode. "L", "RGB", "RGBA"...
        caption: (string) Label for display of image.

    Examples:
        ### Create a ml.Image from a numpy array
        ```python
        import numpy as np
        import manta_lab as ml

        ml.init()
        examples = []
        for i in range(3):
            image = np.random.randint(255, size=(28, 28, 3))
            image = ml.Image(image, caption=f"random field {i}")
            examples.append(image)
        ml.log({"examples": examples})
        ```

        ### Create a ml.Image from a PILImage
        ```python
        import numpy as np
        from PIL import Image
        import manta_lab as ml

        ml.init()
        examples = []
        for i in range(3):
            image = np.random.randint(255, size=(28, 28, 3), dtype=np.uint8)
            PIL.Image = Image.fromarray(image, mode="RGB")
            image = ml.Image(PIL.Image, caption=f"random field {i}")
            examples.append(image)
        ml.log({"examples": examples})
        ```

        ### Create a ml.Image from a Matplotlib
    """

    _log_type: str = "image"
    # from arguments
    _caption: Optional[str]
    _classes: Optional[Classes]
    _boxes: Optional[Dict[str, BoundingBoxes2D]]
    _masks: Optional[Dict[str, ImageMask]]
    # from __init__
    _image: Optional[PIL.Image.Image]
    _width: Optional[int]
    _height: Optional[int]
    # from _set_file
    _path = Optional[str]
    _is_tmp = Optional[str]
    _extension = Optional[str]
    _digest = Optional[str]
    _size = Optional[str]

    _artifact = Optional[str]

    def __init__(self, data_or_path, mode=None, caption=None, classes=None, boxes=None, masks=None) -> None:
        super().__init__()

        self._caption = None
        self._width = None
        self._height = None
        self._image = None
        self._classes = None
        self._boxes = None
        self._masks = None

        if isinstance(data_or_path, str):
            self._init_from_path(data_or_path)
        elif isinstance(data_or_path, Image):
            self._init_from_manta_image(data_or_path)
        else:
            self._init_from_data(data_or_path, mode)

        self._init_image_meta(caption, classes, boxes, masks)

    def _init_from_path(self, path):
        self._extention = os.path.splitext(path)[1][1:]
        self._image = PIL.Image.open(path)
        self._image.load()
        self._set_file(path, is_tmp=False, extension=self._extension)

    def _init_from_data(self, data, mode):
        # TODO: init from matplotlib, torch, TF
        if isinstance(data, PIL.Image.Image):
            self._image = data
        elif isinstance(data, np.ndarray):
            if data.ndim > 2:
                data = data.squeeze()
            data = type_util.numpy_to_uint8(data)
            mode = mode or type_util.guess_image_mode(data)
            self._image = PIL.Image.fromarray(data, mode=mode)
        else:
            raise NotImplementedError("init from matplotlib, torch, TF will be implemented later")

        tmp_path = os.path.join(MEDIA_TEMP_DIR.name, f"{manta_util.generate_id()}.png")
        self._image.save(tmp_path, transparency=None)
        self._set_file(tmp_path, is_tmp=True, extension=".png")

    def _init_from_manta_image(self, image):
        # exclude boxes or masks, only image-related data.
        self._caption = image._caption
        self._width = image._width
        self._height = image._height
        self._image = image._image
        self._classes = image._classes
        self._path = image._path
        self._is_tmp = image._is_tmp
        self._extension = image._extension
        self._digest = image._digest
        self._size = image._size
        self._artifact = image._artifact

    @type_util.free_image_ram
    def _init_image_meta(self, caption, classes, boxes, masks):
        # TODO: classes, boxes, masks
        if caption is not None:
            self._caption = caption

        self._width, self._height = self.image.size

    @classmethod
    def from_json(cls, json_obj, artifact):
        # TODO: Implement
        data_or_path = artifact.get_path(json_obj["path"]).download()
        classes = json_obj.get("classes")
        boxes = json_obj.get("boxes")
        masks = json_obj.get("masks")

        return cls(
            data_or_path,
            caption=json_obj.get("caption"),
            classes=classes,
            boxes=boxes,
            masks=masks,
        )

    def to_json(self) -> Dict:
        json_dict = super().to_json()
        json_dict["_type"] = Image._log_type
        json_dict["format"] = self.format

        if self._width is not None:
            json_dict["width"] = self._width
        if self._height is not None:
            json_dict["height"] = self._height
        if self._caption:
            json_dict["caption"] = self._caption

        # TODO: boxes and masks also

        return json_dict

    def bind_run(
        self,
        run,
    ) -> None:
        super().bind_run(run)
        # TODO: bind boxes and masks too

    def upload_file(self, key, step):
        super().upload_file(key, step)

        # TODO: optimize image and upload it too
        # optimized_img_path = type_util.optimize_image(self._image)
        # super().upload_file(key, step, optimized_img_path)

    @staticmethod
    def get_media_subdir():
        return os.path.join("media", "images")

    @staticmethod
    def seq_to_json(
        seq,
    ) -> dict:
        jsons = [obj.to_json() for obj in seq]

        media_dir = Image.get_media_subdir()
        for obj in jsons:
            expected = manta_util.to_server_slash_path(media_dir)
            if not obj["path"].startswith(expected):
                raise ValueError(
                    "Files in an array of Image's must be in the {} directory, not {}".format(
                        Image.get_media_subdir(), obj["path"]
                    )
                )

        width, height = seq[0].image.size  # type: ignore
        format = jsons[0]["format"]

        def size_equals_image(image: "Image") -> bool:
            img_width, img_height = image.image.size  # type: ignore
            return img_width == width and img_height == height  # type: ignore

        sizes_match = all(size_equals_image(img) for img in seq)
        if not sizes_match:
            print("Images sizes do not match. This will causes images to be display incorrectly in the UI.")

        json_dict = {
            "_type": "images",
            "width": width,
            "height": height,
            "format": format,
            "count": len(seq),
            "contents": jsons,
        }

        # TODO: Caption, Mask, box, classes ...
        return json_dict

    @staticmethod
    def all_captions():
        pass

    @staticmethod
    def all_masks():
        pass

    @staticmethod
    def all_boxes():
        pass

    @property
    def image(self) -> Optional[PIL.Image.Image]:
        if self._image is None:
            if self._path is not None:
                self._image = PIL.Image.open(self._path)
                self._image.load()
        return self._image

    @property
    def format(self):
        return self._extension


if __name__ == "__main__":
    from pprint import pprint

    import manta_lab as ml

    run = ml.init(project="test-image")
    path = "/Users/joowonkim/Downloads/my-manta.png"

    img = Image(path)
    img.bind_run()
    img.upload_file("image", 100)
    j = img.to_json()
