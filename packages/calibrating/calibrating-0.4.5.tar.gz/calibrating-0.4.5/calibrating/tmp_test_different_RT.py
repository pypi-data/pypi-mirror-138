#!/usr/bin/env python3

import boxx
from calibrating import *
from calibrating import Cam
import calibrating

if __name__ == "__main__":
    from boxx import *

    checkboard = 0
    # checkboard = 1
    if checkboard:
        caml, camr, camd = Cam.get_test_cams()
    else:
        root = "/home/dl/ai_asrs/big_file_for_ai_asrs/jinyu/2108.aruco标定2/5scan"
        feature_lib = ArucoFeatureLib()
        caml = Cam(
            glob(os.path.join(root, "*", "0_color.jpg")),
            feature_lib,
            name="caml",
            enable_cache=True,
        )
        camr = Cam(
            glob(os.path.join(root, "*", "0_stereo.jpg")),
            feature_lib,
            name="camr",
            enable_cache=True,
        )
        camd = Cam(
            glob(os.path.join(root, "*", "mk_color.png")),
            feature_lib,
            name="camd",
            enable_cache=True,
        )

    print(Cam.load(camd.dump()))

    stereo = Stereo(caml, camr)

    T_camd_in_caml = caml.get_T_cam2_in_self(camd)

    T = caml.get_T_cam2_in_self(camr)
    T = camr.get_T_cam2_in_self(caml)
    stereo2 = Stereo.load(stereo.dump(return_dict=1))
    stereo2.T, stereo2.t = T[:3, :3], T[:3, 3:]
    stereo2.cam2.K, stereo2.cam2.D = camr.K, camr.D
    stereo2._get_undistort_rectify_map()

    # init_by_K_Rt(self, K1, D1, K2, D2, xy, R, T):
    visn = 1
    Cam.vis_stereo(caml, camr, stereo2, visn)
    Cam.vis_stereo(caml, camr, stereo, visn)

if 0:
    key = caml.valid_keys_intersection(camd)[0]
    imgl = imread(caml[key]["path"])
    color_path_d = camd[key]["path"]
    depthd = imread(color_path_d.replace("color.", "depth.").replace(".jpg", ".png"))
    depthd = np.float32(depthd / 1000)

    depthl = caml.project_cam2_depth(camd, depthd, T_camd_in_caml)

    caml.vis_project_align(imgl, depthl)
