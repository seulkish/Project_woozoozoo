# 라이브러리 import단
from flask import Blueprint, render_template, request, redirect, url_for, Flask
from werkzeug.utils import secure_filename
from pywzz.forms import PetInfo,PetImg
from pywzz.models import PetInfo,PetImg
import os
import io
from torchvision import transforms
import torch
from PIL import Image

#---------------------------------------
# AI모델 구동 위한 부분
model = torch.load('pywzz/model/model.pth',map_location='cpu')
#map_location -> cpu/gpu 어떤걸 쓸껀지 물어보는 것 -> 학습은 GPU로 해서 CPU만 있으면 map_location='cpu' 써야 함

model.eval()
def transform_image(img_file):
    transform_image = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    img = Image.open(img_file).convert('RGB')
    return transform_image(img).unsqueeze(0)

def model_run(img_file):
    class_model = ['구진/플라크','비듬/각질/상피성잔고리','태선화/과다색소침착','농포/여드름','미란/궤양','결절,종괴']
    img_tensor = transform_image(img_file)
    with torch.no_grad():
        outputs = model(img_tensor)
        _, preds = torch.max(outputs, 1)
    return class_model[preds]

#-------------------------------------
# 이미지 파일 처리 위한 부분
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allwed_file(filename):
    # .이 있나 없나 체크하는 것과 확장자 확인, 되면 1, 안되면 0
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
#----------------------------------------------------

# Flask 웹 구동부
bp = Blueprint('check', __name__, url_prefix='/check')

@bp.route('/')
def check():
    return render_template('check1.html')

@bp.route('/upload', methods = ['GET', 'POST'])
def upload():
    if request.method == 'GET':
        return render_template('check1.html')

    elif request.method == 'POST':
        f = request.files['data']
        # path='../save_img/'
        # os.mkdir(path)
        f.save(secure_filename(f.filename))
        return 'file upload successfully'

@bp.route('/upload/<filename>')
def upload_file():
    filename=PetImg(img=form.img.data)
    db.session.add(filename)
    db.session.commit()
    return redirect(url_for('check1_yw.html'))

@bp.route('/result')
def result():
    return redirect(url_for('model_run'))
