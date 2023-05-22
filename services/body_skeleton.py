
import numpy as np
import torch, cv2,time, math, base64, io, json
from PIL import Image
from services.skeleton.models.with_mobilenet import PoseEstimationWithMobileNet
from services.skeleton.modules.keypoints import extract_keypoints, group_keypoints
from services.skeleton.modules.load_state import load_state
from services.skeleton.modules.pose import Pose
from services.skeleton.val import normalize, pad_width
from config import settings

class BodySkeleton(object):
    def __init__(self):
        self.limbSeq = [[2, 3], [2, 6], [3, 4], [4, 5], [6, 7], [7, 8], [2, 9], [9, 10], [10, 11], [2, 12], 
                        [12, 13], [13, 14], [2, 1], [1, 15], [15, 17], [1, 16], [16, 18], [3, 17], [6, 18]]
        self.colors = [[255, 0, 0], [255, 85, 0], [255, 170, 0], [255, 255, 0], [170, 255, 0], [85, 255, 0],
                    [0, 255, 0], [0, 255, 85], [0, 255, 170], [0, 255, 255], [0, 170, 255], [0, 85, 255],
                    [0, 0, 255], [85, 0, 255], [170, 0, 255], [255, 0, 255], [255, 0, 170], [255, 0, 85]]
        self.COCO_BODY_PARTS = ['nose', 'neck', 'r_sho', 'r_elb', 'r_wri', 'l_sho', 'l_elb', 'l_wri', 'r_hip', 
                                'r_knee', 'r_ank', 'l_hip', 'l_knee', 'l_ank','r_eye', 'l_eye','r_ear', 'l_ear']
        self.net = PoseEstimationWithMobileNet()
        checkpoint = torch.load(settings.BODY_SKELETON_MODEL.CHECK_POINT, map_location='cpu')
        load_state(self.net, checkpoint)
        self.net = self.net.eval()
        print("Body Skeleton built")
        
    def infer_fast(self, net, img, net_input_height_size, stride, upsample_ratio, cpu,
                pad_value=(0, 0, 0), img_mean=(128, 128, 128), img_scale=1/256):
        height, width, _ = img.shape
        scale = net_input_height_size / height

        scaled_img = cv2.resize(img, (0, 0), fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)
        scaled_img = normalize(scaled_img, img_mean, img_scale)
        min_dims = [net_input_height_size, max(scaled_img.shape[1], net_input_height_size)]
        padded_img, pad = pad_width(scaled_img, stride, pad_value, min_dims)

        tensor_img = torch.from_numpy(padded_img).permute(2, 0, 1).unsqueeze(0).float()
        if not cpu:
            tensor_img = tensor_img.cuda()

        stages_output = self.net(tensor_img)

        stage2_heatmaps = stages_output[-2]
        heatmaps = np.transpose(stage2_heatmaps.squeeze().cpu().data.numpy(), (1, 2, 0))
        heatmaps = cv2.resize(heatmaps, (0, 0), fx=upsample_ratio, fy=upsample_ratio, interpolation=cv2.INTER_CUBIC)

        stage2_pafs = stages_output[-1]
        pafs = np.transpose(stage2_pafs.squeeze().cpu().data.numpy(), (1, 2, 0))
        pafs = cv2.resize(pafs, (0, 0), fx=upsample_ratio, fy=upsample_ratio, interpolation=cv2.INTER_CUBIC)

        return heatmaps, pafs, scale, pad

    def draw(self, input_image, pose_entries, all_keypoints, resize_fac=1):
        canvas = input_image.copy()

        for i in all_keypoints:
            a = i[0] * resize_fac
            b = i[1] * resize_fac
            cv2.circle(canvas, (int(a), int(b)), 2, [255, 255, 255],thickness=-1)
        stickwidth = 4

        for i in range(17):
            for s in pose_entries:
                index = s[np.array(self.limbSeq[i]) - 1]
                if -1 in index:
                    continue
                cur_canvas = canvas.copy()
                y = all_keypoints[index.astype(int), 0]
                x = all_keypoints[index.astype(int), 1]
                m_x = np.mean(x)
                m_y = np.mean(y)
                length = ((x[0] - x[1]) ** 2 + (y[0] - y[1]) ** 2) ** 0.5
                angle = math.degrees(math.atan2(x[0] - x[1], y[0] - y[1]))
                polygon = cv2.ellipse2Poly((int(m_y * resize_fac), int(m_x * resize_fac)),
                                        (int(length * resize_fac / 2), stickwidth), int(angle), 0, 360, 1)
                cv2.fillConvexPoly(cur_canvas, polygon, self.colors[i])
                canvas = cv2.addWeighted(canvas, 0.4, cur_canvas, 0.6, 0)

        return canvas

    def inference(self, img, height_size = 256):
        img = Image.open(io.BytesIO(img))
        img = np.array(img)
        stride = 8
        upsample_ratio = 4
        num_keypoints = 18
        orig_img = img.copy()
        heatmaps, pafs, scale, pad = self.infer_fast(self.net, img, height_size, stride, upsample_ratio, cpu='cpu')

        total_keypoints_num = 0
        all_keypoints_by_type = []
        for kpt_idx in range(num_keypoints):
            total_keypoints_num += extract_keypoints(heatmaps[:, :, kpt_idx], all_keypoints_by_type, total_keypoints_num)

        pose_entries, all_keypoints = group_keypoints(all_keypoints_by_type, pafs, demo=True)
        for kpt_id in range(all_keypoints.shape[0]):
            all_keypoints[kpt_id, 0] = (all_keypoints[kpt_id, 0] * stride / upsample_ratio - pad[1]) / scale
            all_keypoints[kpt_id, 1] = (all_keypoints[kpt_id, 1] * stride / upsample_ratio - pad[0]) / scale
        
        res = self.draw(img, pose_entries, all_keypoints)
        #cv2.imwrite('res.jpg', res)
        img = Image.fromarray(res)

        rawBytes = io.BytesIO()
        img.save(rawBytes, "PNG")
        rawBytes.seek(0)  
        base64Image = base64.b64encode(rawBytes.read())

        current_poses = []
        for n in range(len(pose_entries)):
            if len(pose_entries[n]) == 0:
                continue
            pose_keypoints = np.ones((num_keypoints, 2), dtype=np.int32) * -1
            for kpt_id in range(num_keypoints):
                if pose_entries[n][kpt_id] != -1.0:  # keypoint was found
                    pose_keypoints[kpt_id, 0] = int(all_keypoints[int(pose_entries[n][kpt_id]), 0])
                    pose_keypoints[kpt_id, 1] = int(all_keypoints[int(pose_entries[n][kpt_id]), 1])
            
            current_poses.append(dict(zip(self.COCO_BODY_PARTS, pose_keypoints.tolist())))

        return base64Image, current_poses
   
   





