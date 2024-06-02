from abc import ABC, abstractmethod

import cv2
import numpy as np

from app.settings import settings


class BaseConverter(ABC):

    @abstractmethod
    def convert(self, file_bytes: bytes, compress: bool) -> bytes:
        pass

    @abstractmethod
    def get_extension(self) -> str:
        pass


class ImageWebpConverter(BaseConverter):

    def convert(self, file_bytes: bytes, compress: bool) -> bytes:
        file_as_np = np.frombuffer(file_bytes, dtype=np.uint8)
        file_image = cv2.imdecode(file_as_np, flags=1)
        compression_size = settings.compression_size if compress else 100
        return cv2.imencode(self.get_extension(), file_image, [int(cv2.IMWRITE_WEBP_QUALITY), compression_size])[
            1
        ].tobytes()

    def get_extension(self) -> str:
        return ".webp"


class ImageJpgConverter(BaseConverter):

    def convert(self, file_bytes: bytes, compress: bool) -> bytes:
        file_as_np = np.frombuffer(file_bytes, dtype=np.uint8)
        file_image = cv2.imdecode(file_as_np, flags=1)
        compression_size = settings.compression_size if compress else 100
        return cv2.imencode(self.get_extension(), file_image, [int(cv2.IMWRITE_JPEG_QUALITY), compression_size])[
            1
        ].tobytes()

    def get_extension(self) -> str:
        return ".jpg"


class ImagePngConverter(BaseConverter):

    def convert(self, file_bytes: bytes, compress: bool) -> bytes:
        file_as_np = np.frombuffer(file_bytes, dtype=np.uint8)
        file_image = cv2.imdecode(file_as_np, flags=1)
        compression_size = settings.compression_size if compress else 100
        return cv2.imencode(self.get_extension(), file_image, [int(cv2.IMWRITE_PNG_COMPRESSION), compression_size])[
            1
        ].tobytes()

    def get_extension(self) -> str:
        return ".png"
