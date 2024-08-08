# color mask to grey mask
from PIL import Image
import numpy as np

def greyMask(file_root:str,filename:str):
    color_mask_path = file_root+filename
    # 컬러 마스크 이미지 열기
    color_mask = Image.open(color_mask_path).convert('RGBA')

    # NumPy 배열로 변환
    color_mask_array = np.array(color_mask)

    # 새로운 마스크 배열 생성 (흰색과 검은색)
    # 마스킹 부분은 흰색(255), 나머지는 검은색(0)
    new_mask_array = np.zeros((color_mask_array.shape[0], color_mask_array.shape[1]), dtype=np.uint8)

    # 알파 채널 가져오기
    alpha_channel = color_mask_array[:, :, 3]

    # 마스킹된 부분이 색상 정보가 있는지 확인
    for y in range(color_mask_array.shape[0]):
        for x in range(color_mask_array.shape[1]):
            if alpha_channel[y, x] > 0:  # 투명하지 않은 경우
                new_mask_array[y, x] = 255  # 흰색으로 설정

    # 새로운 마스크 이미지를 생성
    new_mask_image = Image.fromarray(new_mask_array, mode='L')  # 'L' 모드는 흑백 이미지 모드

    # 새로운 마스크 이미지 저장
    new_mask_image.save("./masks/"+filename)

# 컬러 마스크 이미지 경로
import os
condition = lambda x:(int(x.split(".")[0].split("_")[0]),int(x.split(".")[0].split("_")[1].split("mask")[1]))

masks = sorted([i for i in os.listdir("color_masks") if i !=".DS_Store"],key=condition)
for mask in masks:
    greyMask("./color_masks/",mask)
