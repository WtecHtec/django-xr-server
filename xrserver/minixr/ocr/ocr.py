import os
from pathlib import Path

import cv2
import imutils
from django.conf import settings
# BASE_DIR = Path(__file__).resolve().parent.parent
# print(settings)
g_matreil_path =  './media/media'

class OCR():
  def get_target_block(self, train_path):
    result = ''
    rect = ''
    code = False
    max_area = -99999
    t_img = cv2.imread(train_path)

    # cv2.imshow("Input", t_img)
    # cv2.waitKey(0)

    gray_img = cv2.cvtColor(t_img.copy(), cv2.COLOR_BGR2GRAY)
    
		# 模板阈值（蒙层	）
    _, gray_img = cv2.threshold(gray_img, 100, 80, cv2.THRESH_BINARY_INV)
    cv2.imshow("Input", gray_img)
    cv2.waitKey(0)

    canny_img = cv2.Canny(gray_img.copy(),120,155)
    rectKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (4, 3))
    canny_img = cv2.morphologyEx(canny_img.copy(), cv2.MORPH_CLOSE, rectKernel)
    canny_img = cv2.morphologyEx(canny_img.copy(), cv2.MORPH_CLOSE, rectKernel)

    # cv2.imshow("Input", canny_img)
    # cv2.waitKey(0)

    cnts_img = cv2.findContours(canny_img.copy(), cv2.RETR_EXTERNAL,
		 cv2.CHAIN_APPROX_NONE)
    cnts = imutils.grab_contours(cnts_img)

    show_img = t_img.copy()
    cv2.drawContours(show_img, cnts, -1, (0,0,255), 3)
    cv2.imshow("Input", show_img)
    cv2.waitKey(0)

    for c in cnts:
      # 获取特征
      cnt_area = cv2.contourArea(c)
      if max_area < cnt_area and cnt_area > 500:
        max_area = cnt_area
        rect = cv2.boundingRect(c)
        (x, y, w, h) = cv2.boundingRect(c)
        # result = cv2.rectangle(t_img.copy(), (x, y), (x + w ,y + h),(0,0,0),-1)
        result = gray_img[y:y+h, x:x+w]
        code = True
    return code, result, rect

  def matchMedia(self, train_path = ''):
    files= os.listdir(g_matreil_path) #得到文件夹下的所有文件名称
    if train_path == '' or train_path == None :
      return ''
    code,t_result, t_rect = self.get_target_block(train_path)
    if code == False:
      return ''
    x, y, w, h = t_rect
    print(x, y, w, h)

    # t_result = cv2.imread(train_path)
    # t_result = cv2.cvtColor(t_result.copy(), cv2.COLOR_BGR2GRAY)

    cv2.imshow("Input-show", t_result)
    cv2.waitKey(0)

    max_score = -999
    media_result = ''
    for tfile in files: #遍历文件夹
       tmp_path = g_matreil_path + "/" +tfile
       if not os.path.isdir(tmp_path):
        if tfile.endswith('.jpeg') or tfile.endswith('.png') or tfile.endswith('.jpg'):
          t_img = cv2.imread(tmp_path)
          gray_img = cv2.cvtColor(t_img.copy(), cv2.COLOR_BGR2GRAY)
          [h, w] = t_result.shape
          print(w, h)
          gray_img =  cv2.resize(gray_img, (w, h))
          result = cv2.matchTemplate(t_result, gray_img, cv2.TM_CCOEFF_NORMED)
          (_, score, _, _) = cv2.minMaxLoc(result)
          print(score)
          if max_score < score and score > 0.95: 
              max_score = score
              media_result = tfile

          # code, result, rect = self.get_target_block(tmp_path)
          # if code == True:
          #   temp_img = imutils.resize(result, width=w, height=h)
          #   cv2.imshow("Input", temp_img)
          #   cv2.waitKey(0)
          #   # temp_img =  cv2.resize(result,(w, h))
          #   result = cv2.matchTemplate(temp_img, t_result, cv2.TM_CCOEFF_NORMED)
          #   (_, score, _, _) = cv2.minMaxLoc(result)
          #   print(score)
          #   if max_score < score and score > 0.95: 
          #      max_score = score
          #      media_result = tmp_path

    print(media_result, max_score)
    return media_result

ocr = OCR()
ocr.matchMedia('./media/ocr/demo.jpg')