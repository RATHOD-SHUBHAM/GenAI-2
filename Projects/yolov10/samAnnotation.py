import numpy as np
import torch
import matplotlib.pyplot as plt
import cv2
import os
from segment_anything import sam_model_registry, SamAutomaticMaskGenerator, SamPredictor

class SAM:
    def __init__(self):
        self.HOME = os.getcwd()

    def show_mask(self, mask, ax, random_color=False):
        if random_color:
            color = np.concatenate([np.random.random(3), np.array([0.6])], axis=0)
        else:
            color = np.array([30/255, 144/255, 255/255, 0.6])
        h, w = mask.shape[-2:]
        mask_image = mask.reshape(h, w, 1) * color.reshape(1, 1, -1)
        ax.imshow(mask_image)

    def show_points(self, coords, labels, ax, marker_size=375):
        pos_points = coords[labels==1]
        neg_points = coords[labels==0]
        ax.scatter(pos_points[:, 0], pos_points[:, 1], color='green', marker='*', s=marker_size, edgecolor='white', linewidth=1.25)
        ax.scatter(neg_points[:, 0], neg_points[:, 1], color='red', marker='*', s=marker_size, edgecolor='white', linewidth=1.25)

    def show_box(self, box, ax):
        x0, y0 = box[0], box[1]
        w, h = box[2] - box[0], box[3] - box[1]
        ax.add_patch(plt.Rectangle((x0, y0), w, h, edgecolor='green', facecolor=(0,0,0,0), lw=2))

    # Automatic mask generation
    def show_anns(self, anns):
        if len(anns) == 0:
            return
        sorted_anns = sorted(anns, key=(lambda x: x['area']), reverse=True)
        ax = plt.gca()
        ax.set_autoscale_on(False)

        img = np.ones((sorted_anns[0]['segmentation'].shape[0], sorted_anns[0]['segmentation'].shape[1], 4))
        img[:,:,3] = 0
        for ann in sorted_anns:
            m = ann['segmentation']
            color_mask = np.concatenate([np.random.random(3), [0.35]])
            img[m] = color_mask
        ax.imshow(img)


    def annotate(self, test_image, bbox):
        sam_checkpoint = f'{self.HOME}/sam_vit_h_4b8939.pth'
        model_type = "vit_h"

        device = "cpu"

        sam = sam_model_registry[model_type](checkpoint=sam_checkpoint)
        sam.to(device=device)

        predictor = SamPredictor(sam)
        mask_generator = SamAutomaticMaskGenerator(sam)

        self.test_image = test_image
        image = cv2.imread(self.test_image)
        predictor.set_image(image)

        tensor_box = torch.tensor(bbox.xyxy, device=predictor.device)

        transformed_boxes = predictor.transform.apply_boxes_torch(tensor_box, image.shape[:2])

        batch_masks, batch_scores, batch_logits = predictor.predict_torch(
            point_coords=None,
            point_labels=None,
            boxes=transformed_boxes,
            multimask_output=False,
        )

        plt.figure(figsize=(10, 10))
        plt.imshow(image)

        for mask in batch_masks:
            self.show_mask(mask.cpu().numpy(), plt.gca(), random_color=True)
        # for box in tensor_box:
        #     show_box(box.cpu().numpy(), plt.gca())

        plt.axis('off')
        plt.savefig('my_image.jpg')
        # plt.show()

        # Display the mask
        individual_masks = [mask.squeeze(0) for mask in batch_masks]


        for i, mask in enumerate(individual_masks):
            print(f"Mask {i}: {mask.shape}")
            self.show_mask(mask.cpu().numpy(), plt.gca(), random_color=True)

        plt.axis('off')
        plt.savefig('my_mask.jpg')
        # plt.show()



