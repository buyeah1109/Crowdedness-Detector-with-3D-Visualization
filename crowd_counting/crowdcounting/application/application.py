from crowdcounting import Router

class CrowdCounter():

    def __init__(
        self,
        _mcnnmodelpath = '../data/models/mcnn_shtechA_660.h5',
        _gpuID = -1
    ):
        self.mcnnmodelpath = _mcnnmodelpath
        self.gpu_id = _gpuID

    def count(self, image):
        model = Router(
            self.gpu_id,
            mcnn_model_path=self.mcnnmodelpath,
            cutoff_pose=20,
            cutoff_mcnn=50
        )
        result = model.score(image, return_image=False, img_dim=1750)
        pred = result["pred"]
        return pred




