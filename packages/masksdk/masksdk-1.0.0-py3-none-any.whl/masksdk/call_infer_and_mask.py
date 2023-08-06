import enum
import logging
import time
from typing import List

import requests
from PIL import Image

from masksdk.mask import blurring, pixelating, blackening

logger = logging.getLogger('masksdk')
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


class ModelName(enum.Enum):
    FACE_AI = 'face_ai'
    PLATE_AI = 'plate_ai'


class MaskName(enum.IntEnum):
    BULR = 1
    PIXEL = 2
    BLACK = 3


def _infer_one_image(infer_host, img_rb, model_name):
    try:
        files = {"input_data": img_rb}
        uri = '{}/models/{}/predict'.format(infer_host, model_name)
        start_time = time.time()
        resp = requests.post(url=uri, files=files, timeout=10)
        if resp.status_code == requests.codes["ok"] and len(resp.content) > 0:
            logger.debug("infer with resp_len {} total time: {:.4f}s".format(len(resp.content), time.time() - start_time))
            return resp.json()
        else:
            logger.warning('failed to get mask with error={}'.format(resp.content))
        return {}
    except Exception as error:
        logger.error('error to get mask output_image_path={}, error={}'.format(1, str(error)))
        return {}


def _parse_infer_response_box(response):
    boxes = []
    for bbox in response['data']['bounding-boxes']:
        box = dict()
        coord = bbox['coordinates']
        score = bbox.get('confidence', -1)
        class_name = bbox['ObjectClassName']
        box['score'] = score
        box['class_name'] = class_name
        box['x_min'] = coord['left']
        box['y_min'] = coord['top']
        box['x_max'] = coord['right']
        box['y_max'] = coord['bottom']
        boxes.append(box)
    return boxes


def mask_one_image(infer_host, image_file, model_names: List[ModelName], mask_name: MaskName, degree: float):
    """mask an image with specific parameters

    :param infer_host: infer server address [ip:port]
    :param image_file: the absolute image file
    :param model_names: use which mode to infer
    :param mask_name: use which mask technology to mask
    :param degree: the mask degree, 1 is most
    :return: image with mask
    """

    # open image in binary
    img_rb = open(image_file, 'rb')

    # infer
    bboxes = []
    for one_model_name in model_names:
        if one_model_name not in [ModelName.FACE_AI, ModelName.PLATE_AI]:
            raise NotImplementedError('not support this model={}'.format(one_model_name))
        infer_resp = _infer_one_image(infer_host, img_rb, one_model_name.value)
        if infer_resp.get('data'):
            one_boxes = _parse_infer_response_box(infer_resp)
            bboxes += one_boxes
        img_rb.seek(0)  # go back to the start of the img

    # select mask tech
    img = Image.open(img_rb)
    if mask_name == MaskName.BULR:
        func = blurring
    elif mask_name == MaskName.PIXEL:
        func = pixelating
    elif mask_name == MaskName.BLACK:
        func = blackening
    else:
        raise NotImplementedError('not support this mask tech={}'.format(mask_name))

    # mask
    mask_img = func(img, bboxes, degree)
    return mask_img
