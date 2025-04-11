from paddleocr import PaddleOCR
ocr = PaddleOCR(use_angle_cls=True, lang='ch')  # 'ch' for Chinese
result = ocr.ocr('path/to/your/image.jpg', cls=True)
print(result)