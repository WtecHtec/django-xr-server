from paddleclas import PaddleClas
import paddle
paddle.utils.run_check()
infer_imgs='./minixr/ocr/test/demo.jpg'
clas = PaddleClas(model_name='InceptionV3', image_file = infer_imgs)
# clas = PaddleClas(model_file="./minixr/ocr/test/mainbody_v1.0_infer/inference.pdmodel")
result=clas.predict(infer_imgs)
print(result)