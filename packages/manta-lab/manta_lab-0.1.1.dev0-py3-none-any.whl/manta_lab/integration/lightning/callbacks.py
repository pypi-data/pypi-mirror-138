from functools import partial

import pytorch_lightning as pl
import torch

import manta_lab as ml


# TODO: only for image input & image output for now. will be changed to general use
class MantaImageCallback(pl.Callback):
    """Logs the input and output images of a module.

    Images are stacked into a mosaic, with output on the top
    and input on the bottom."""

    def __init__(
        self,
        train_samples=None,
        validation_samples=None,
        test_samples=None,
        max_samples=32,
    ):
        super().__init__()
        self._imgs = {
            "on_train_end": None,
            "on_validation_end": None,
            "on_test_end": None,
        }
        self.max_samples = max_samples

        if train_samples:
            self._connect_hook("on_train_end", train_samples)
        if validation_samples:
            self._connect_hook("on_validation_end", validation_samples)
        if test_samples:
            self._connect_hook("on_test_end", test_samples)

    def prune_max_image_samples(self, samples, random=False):
        if random:
            pass  # TODO: random sampling
        return samples[: self.max_samples]

    def _connect_hook(self, func_name, samples):
        self._imgs[func_name] = self.prune_max_image_samples(samples)

        log_images = partial(self._log_images, func_name=func_name)
        self.__setattr__(func_name, log_images)

    def _log_images(self, trainer, pl_module, func_name):
        inputs = self._imgs[func_name].to(device=pl_module.device)
        outs = pl_module(inputs)

        images = torch.cat([inputs, outs], dim=-2)
        caption = "Input & Output"
        trainer.logger.log(
            {
                "val/examples": [ml.Image(img, caption=caption) for img in images],
                "global_step": trainer.global_step,
            }
        )
