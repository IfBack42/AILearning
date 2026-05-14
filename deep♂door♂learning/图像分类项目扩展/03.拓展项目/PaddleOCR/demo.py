import os
import time
from paddleocr import PaddleOCR

filepath = r"tests/test_files/254.jpg"

ocr_model = PaddleOCR(use_angle_cls=True, lang="ch", use_gpu=True, show_log=1,
                      det_db_box_thresh=0.1, use_dilation=True,
                      det_model_dir='weight/ch_PP-OCRv4_det_server_infer.tar',
                      cls_model_dir='weight/ch_ppocr_mobile_v2.0_cls_infer.tar',
                      rec_model_dir='weight/ch_PP-OCRv4_rec_server_infer.tar')

t1 = time.time()
for i in range(1):
    result = ocr_model.ocr(img=filepath, det=True, rec=True, cls=True)[0]
t2 = time.time()
print((t2 - t1) / 10)

for res_str in result:
    print(res_str)