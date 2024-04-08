import numpy as np


def get_mask_from_color_mask(color_mask, cls_color_map, lead):
    color = cls_color_map[lead]
    cls_pixels = np.all(color_mask==color, axis=-1)

    height, width, _ = color_mask.shape
    bin_mask = np.zeros([height, width])
    bin_mask[cls_pixels] = 255
    bin_mask[~cls_pixels] = 0
    return bin_mask.astype(np.uint8)


if __name__ == '__main__':
    import cv2
    color_mask_path = '/home/fdias/Documents/gitlab/gen_data_cinc24/ecg-image-kit/codes/ecg-image-generator/colormask_example.png'
    color_mask = cv2.cvtColor(cv2.imread(color_mask_path), cv2.COLOR_BGR2RGB)
    from lead2color import lead2colorRGB as lead2color
    cls_color_map = lead2color
    
    
    im = get_mask_from_color_mask(color_mask, cls_color_map, 'fullI')
    cv2.imwrite('mask.png', im)
    # cv2.imshow('I', im)
    # cv2.waitKey(0)