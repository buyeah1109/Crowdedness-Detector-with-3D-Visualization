import os
import numpy as np
import cv2
from tf_pose.estimator import TfPoseEstimator
from tf_pose.networks import get_graph_path, model_wh
import tensorflow as tf

DEFAULT_RADIUS = 1000

class CrowdednessDetector():
    
    def __init__(
        self,
        _area,
        _radius = DEFAULT_RADIUS,
    ):
        self.radius = _radius
        self.area  = _area
        self.centroids_x = []
        self.centroids_y = []
        self.count = -1
    
    # return count of people, 
    # density map 
    # with given image and radius/social distance
    def count_density_map(self, _input_img):
        _radius = self.radius
        config = tf.ConfigProto()
        config.gpu_options.allow_growth = True
        config.allow_soft_placement = True
        model = "cmu"
        resize = "656x368"
        w, h = model_wh(resize)

        model = init_model(-1, model, w, h, config)
        img = create_openpose_image(_input_img, 1750)
        humans = score_openpose(model, img, w, h)
        image_h, image_w = img.shape[:2]
        cnt = 0
        coor_x = []
        coor_y = []
        for human in humans:
            if 0 not in human.body_parts.keys():
                continue
            cnt = cnt + 1
            body_part = human.body_parts[0]
            center = (int(body_part.x * image_w + 0.5), int(body_part.y * image_h + 0.5))
            coor_x.append(center[0])
            coor_y.append(center[1])
        self.save_centroids(coor_x, coor_y)
        black_img = np.zeros([image_h, image_w, 3], np.uint8)
        density_img = np.copy(black_img)
        for i in range(len(coor_x)):
            cv2.circle(density_img, (coor_x[i],coor_y[i]), radius=_radius, color=(255,255,255), thickness=-1)
        self.count = cnt
        return cnt, density_img

    def get_crowdedness(self, density_img, n):
        area = self.area
        h, w = density_img.shape[:2]
        cnt = 0
        # for r in range(h):
        #     for c in range(w):
        #         b, g, r = density_img[r][c][:]
        #         if b/3 + g/3 + r/3 == 0:
        #             cnt = cnt + 1
        # cnt = h * w - cnt
        sum3 = np.sum(density_img)
        cnt = sum3 / (3*255)
        den = n / area
        clus = w * h / cnt
        cr = den * clus
        return cr

    def save_centroids(self, coor_x, coor_y):
        self.centroids_x = coor_x
        self.centroids_y = coor_y


def init_model(gpu_id, model, w, h, config):
    """Initialize model.
    
    Args:
        gpu_id: GPU ID. 
    
    Returns:
        A TensorFlow model object.
    """

    # if w == 0 or h == 0:
    #     w, h = 432, 368

    if gpu_id == -1: # pragma: no cover
        os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
        e = TfPoseEstimator(get_graph_path(model), target_size=(w, h), tf_config=config)
    else:
        with tf.device("/device:GPU:{}".format(gpu_id)):
            e = TfPoseEstimator(
                get_graph_path(model), target_size=(w, h), tf_config=config
            )
    return e
    
def score_openpose(e, image, w, h):
    """Score an image using OpenPose model.
    
    Args:
        e: OpenPose model.
        image: Image in CV2 format.
    
    Returns:
        Nubmer of people in image.
    """
    resize_out_ratio = 4.0
    humans = e.inference(
    image, resize_to_default=(w > 0 and h > 0), upsample_size=resize_out_ratio
    )
    return humans

def imresizeMaxDim(img, maxDim, boUpscale=False, interpolation=cv2.INTER_CUBIC):
    """Resize image.
    
    Args:
        img: Image in CV2 format. 
        maxDim: Maximum dimension. 
        boUpscale (optional): Defaults to False. 
        interpolation (optional): Defaults to cv2.INTER_CUBIC. 
    
    Returns:
        Resized image and scale.
    """
    scale = 1.0 * maxDim / max(img.shape[:2])
    if scale < 1 or boUpscale:
        img = cv2.resize(img, (0, 0), fx=scale, fy=scale, interpolation=interpolation)
    else:
        scale = 1.0
    return img, scale
    
def create_openpose_image(filebytes, img_dim):
    """Create image from file bytes.
    
    Args:
        filebytes: Image in stream.
        img_dim: Max dimension of image.
    
    Returns:
        Image in CV2 format. 
    """
    # file_bytes = np.asarray(bytearray(BytesIO(filebytes).read()), dtype=np.uint8)
    file_bytes = np.fromstring(filebytes, np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    img, _ = imresizeMaxDim(img, img_dim)
    return img






