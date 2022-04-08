import cv2
import os
import json

def overlay_img(background, overlay, start_point, dim):
    for y in range(dim[0]):
        for x in range(dim[1]):
            overlay_color = overlay[y, x, :3]  # first three elements are color (RGB)
            overlay_alpha = overlay[y, x, 3] / 255  # 4th element is the alpha channel, convert from 0-255 to 0.0-1.0

            # get the color from the background image
            background_color = background[start_point[0] + y, start_point[1] + x]

            # combine the background color and the overlay color weighted by alpha
            composite_color = background_color * (1 - overlay_alpha) + overlay_color * overlay_alpha

            # update the background image in place
            background[start_point[0] + y, start_point[1] + x] = composite_color
    return background

def ret_start_point(h, w, padding_rate, dim, flag):
    min_len = min(h,w)
    padding_size = int(min_len * padding_rate)
    start_point = None

    if (flag == '1'):
        start_point = (padding_size, padding_size)
    elif (flag == '2'):
        start_point = (padding_size, w - padding_size - dim[1])
    elif (flag == '3'):
        start_point = (h - padding_size - dim[0],padding_size)
    elif (flag == '4'):
        start_point = (h - padding_size - dim[0], w - padding_size - dim[1])

    return start_point

if __name__ == '__main__':
    dir_name = '..\\imgs\\data_annotated'
    new_dir_name = dir_name + '_logo'
    os.makedirs(new_dir_name)
    files = os.listdir(dir_name)
    n_json_list = [name for name in files if name.split('.')[-1] !='json']
    file_name_list = ['.'.join(file.split('.')[:-1]) for file in n_json_list]

    logo_path = '..\\imgs\\logo\\TLC-favicon.png'
    logo = cv2.imread(logo_path, cv2.IMREAD_UNCHANGED)
    logo_h, logo_w = logo.shape[:2]

    padding_rate = 0.03
    resize_rate = 0.1
    cnt = 0 

    for full_name, file_name in zip(n_json_list, file_name_list):
        json_path = os.path.join(dir_name,file_name)+'.json'
        if(os.path.isfile(json_path)):

            with open(os.path.join(json_path), 'r') as fcc_file:
                json_obj = json.load(fcc_file)
            flag = None
            for key, item in json_obj['flags'].items():
                if(item): flag = key

            if(flag):
                img_path = os.path.join(dir_name, full_name)
                background = cv2.imread(img_path)
                h,w = background.shape[:2]

                # dim = (int(resize_rate * h / logo_h), int(resize_rate * w / logo_w))
                resize_rate_min = min(resize_rate * h / logo_h, resize_rate * w / logo_w)
                dim = (int(logo_h * resize_rate_min), int(logo_w * resize_rate_min))
                start_point = ret_start_point(h,w,padding_rate,dim,flag)
                overlay = cv2.resize(logo, dim, interpolation = cv2.INTER_AREA)
                new_img = overlay_img(background, overlay, start_point, dim)
                print(os.path.join(new_dir_name, f'{cnt}.png'))
                cv2.imwrite(os.path.join(new_dir_name, f'{cnt}.png'),new_img)
                cnt += 1

