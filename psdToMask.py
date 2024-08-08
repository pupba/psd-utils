# psd file to color-masks
from psd_tools import PSDImage
import numpy as np
from PIL import Image

def psdToMask(psd_root:str,filename:str):
    # PSD 파일 열기
    psd = PSDImage.open(psd_root+filename)

    # 원본 크기 가져오기
    original_width, original_height = psd.size

    # 레이어별로 이미지 저장
    for index, layer in enumerate(psd):
        # 레이어를 numpy 배열로 변환
        layer_image = layer.composite()

        if layer_image is not None:
            # 이미지를 RGBA로 변환하고 uint8 형식으로 변환
            layer_image = np.array(layer_image.convert('RGBA'))

            # 알파 채널을 활용하여 마스킹
            alpha_channel = layer_image[:, :, 3]  # 알파 채널
            mask = (alpha_channel > 0)  # 투명하지 않은 부분의 마스크

            # 원본 크기 유지
            masked_image = np.zeros((original_height, original_width, 4), dtype=np.uint8)  # 빈 이미지 생성

            # 레이어의 위치
            top, left = layer.top, layer.left

            # 마스크가 있는 부분만 복사
            for y in range(layer_image.shape[0]):
                for x in range(layer_image.shape[1]):
                    if mask[y, x]:  # 마스크가 있는 경우
                        masked_image[top + y, left + x] = layer_image[y, x]  # RGBA 채널 복사

            # 파일 이름 설정
            layer_filename = f'{filename.split(".")[0]}_mask{index}.png'

            # PIL을 사용하여 RGBA 이미지를 저장
            Image.fromarray(masked_image).save(f"./color_masks/{layer_filename}")
            print(f'Saved {layer_filename} with size: {masked_image.shape[1]}x{masked_image.shape[0]}')

if __name__ == "__main__":
    # PSD 파일 경로
    import os
    psds = sorted([i for i in os.listdir('psds') if i!=".DS_Store"],key=lambda x:int(x.split(".")[0]))
    # psds = [str(i+1).zfill(3)+".psd" for i in range(5)]
    for psd in psds:
        psdToMask("psds/",psd)
