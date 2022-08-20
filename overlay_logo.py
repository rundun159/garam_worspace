import cv2
import os
import json
import argparse

DEBUG_PAR = True

parser = argparse.ArgumentParser(description='overlay_logo')
parser.add_argument('--src_name', type=str)
parser.add_argument('--levites', type=bool, default = False)
args = parser.parse_args()

def overlay_img(background, overlay, start_point, dim, levites=False):
    if DEBUG_PAR: print(f"overlay shape : {overlay.shape}, dim : {dim}")
    for y in range(dim[0]):
        for x in range(dim[1]):
            overlay_color = overlay[y, x, :3]  # first three elements are color (RGB)
            overlay_alpha = overlay[y, x, 3] / 255  # 4th element is the alpha channel, convert from 0-255 to 0.0-1.0

            # get the color from the background image
            background_color = background[start_point[0] + y, start_point[1] + x]

            # combine the background color and the overlay color weighted by alpha
            if not levites:
                overlay_alpha *= 0.5
            else:
                overlay_alpha *= 0.7
            composite_color = background_color * (1 - overlay_alpha) + overlay_color * overlay_alpha

            # update the background image in place
            background[start_point[0] + y, start_point[1] + x] = composite_color
    return background

def ret_start_point(h, w, padding_rate, dim, flag, levites=False):
    min_len = min(h,w)
    padding_size = int(min_len * padding_rate)
    start_point = None

    levites_padding = 10

    if (flag == '1'):
        if levites:
            start_point = (padding_size + levites_padding, padding_size + levites_padding)
        else:
            start_point = (padding_size, padding_size)
        
    elif (flag == '2'):
        if levites:
            start_point = (padding_size + levites_padding, w - padding_size - dim[1] - levites_padding)            
        else:
            start_point = (padding_size, w - padding_size - dim[1])
    elif (flag == '3'):
        if levites:
            start_point = (h - padding_size - dim[0],padding_size + levites_padding)
        else:
            start_point = (h - padding_size - dim[0],padding_size)
    elif (flag == '4'):
        if levites:
            start_point = (h - padding_size - dim[0], w - padding_size - dim[1] - levites_padding)            
        else:
            start_point = (h - padding_size - dim[0], w - padding_size - dim[1])
    if DEBUG_PAR : print(f"start_point : {start_point}")
    return start_point

if __name__ == '__main__':
    print("It changed!")
    dir_name = f'..\\imgs\\{args.src_name}'
    new_dir_name = dir_name + '_logo'
    os.makedirs(new_dir_name, exist_ok=True)
    files = os.listdir(dir_name)
    n_json_list = [name for name in files if name.split('.')[-1] !='json']
    file_name_list = ['.'.join(file.split('.')[:-1]) for file in n_json_list]

    if args.levites:
        logo_path = '..\\imgs\\logo\\Levites_new.png'
        padding_rate = 0
        resize_rate = 0.4
    else:
        logo_path = '..\\imgs\\logo\\TLC-favicon-high-alpha-high-resolution.png'
        padding_rate = 0
        resize_rate = 0.1
    logo = cv2.imread(logo_path, cv2.IMREAD_UNCHANGED)
    logo_h, logo_w = logo.shape[:2]
    if DEBUG_PAR : print("Logo Shape : ", logo.shape)
    # for TLC
    # for Levites
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

                if DEBUG_PAR: print(f"Img Shape : {background.shape}, {file_name}")

                # for Levites
                if args.levites:
                    garam_w = 150
                    dim = (garam_w, int(garam_w * logo_w / logo_h))                
                # for TLC
                else:
                    garam_w = 100
                    dim = (garam_w, int(garam_w * logo_w / logo_h))
                    resize_rate_min = min(resize_rate * h / logo_h, resize_rate * w / logo_w)

                if DEBUG_PAR: print(f"dim : {dim}")

                start_point = ret_start_point(h,w,padding_rate,dim,flag, args.levites)
                overlay = cv2.resize(logo, (dim[1], dim[0]), interpolation = cv2.INTER_AREA)

                new_img = overlay_img(background, overlay, start_point, dim, args.levites)
                print(os.path.join(new_dir_name, f'{cnt}.png'))
                cv2.imwrite(os.path.join(new_dir_name, f'{cnt}.png'),new_img)
                cnt += 1

