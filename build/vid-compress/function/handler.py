import json
import os
import uuid
from PIL import Image  
import PIL  
import requests
# from django.http import HttpResponse
# from django.http import FileResponse
import shutil

from minio import Minio
import ffmpeg

def handle(st):
    """
    For the moment, we are going with json input to be as below
    ```
    {
        file_name: "file name"
    }
    ```
    """
    req = json.loads(st)
    print(req)

    mc = Minio(os.environ['minio_hostname'],
                  access_key=os.environ['minio_access_key'],
                  secret_key=os.environ['minio_secret_key'],
                  secure=False)

    source_bucket = os.environ['source_bucket']
    dest_bucket = os.environ['dest_bucket']

    file_name = req['file_name']
    my_uuid = gen_uuid()

    file_path = f"/tmp/{my_uuid}_{file_name}"
    mc.fget_object(source_bucket, file_name, f"/tmp/{my_uuid}_{file_name}")
    # file_path = f"/tmp/{file_name}"

    (
        ffmpeg
        .input(file_path)
        # .hflip()
        .filter('fps', fps=5, round='up')
        .filter('scale', w=720, h=720)
        .output(f"/tmp/{my_uuid}_compressed_{file_name}")
        .run()
    )



    # foo = Image.open(f"/tmp/{my_uuid}_{file_name}")  # My image is a 200x374 jpeg that is 102kb large 
    # foo.size  # (200, 374)
 
    # # downsize the image with an ANTIALIAS filter (gives the highest quality)
    # foo = foo.resize((160,300),Image.ANTIALIAS)
 
    # # foo.save('image_scaled.jpg', quality=95)  # The saved downsized image size is 24.8kb
    # return foo.save('image_scaled_opt.jpg', optimize=True, quality=95) 
    # f = open("image_scaled_opt.jpg", "wb")
    # f.write(pic)
    # f.close()
    # return f
    mc.fput_object(dest_bucket, file_name, f"/tmp/{my_uuid }_compressed_{file_name}")
    
    # New lines
    # # The saved downsized image size is 22.9kb
    # path1 = f"/tmp/{my_uuid }_compressed_{file_name}"
    f = Image.open(f"/tmp/{my_uuid }_compressed_{file_name}")  
    # fin = f.write("datacompressed.jpg")
    f.save("datacompressed.jpg")
    # f.close()
    with open(f'/tmp/{my_uuid }_compressed_{file_name}','rb') as rf:
        with open('./datacompressed.jpg','wb') as wf:
            for line in rf: 
                wf.write(line)
            # shutil.copyfileobj(rf.write().decode('utf-8'), wf)
            return print('Image sucessfully Downloaded: ',file_name)

        # return HttpResponse(fi.read(), content_type="image/jpg")
       
   

    # img = open('./datacompressed.jpg','rb')      HttpResponse(status=200)
    # response =  FileResponse(img)
    # return response
    # res = requests.post(url = 'http://localhost:8080/function/vid-compress/home/app/datacompressed.jpg', data =data, headers={'Content-Type':'image/jpeg'})
    # return res
    # pic = picture.save("datacompressed.jpg") 
    # f=open(f"/tmp/{my_uuid}_compressed_{file_name}", "wb")
    # path = f"/tmp/{my_uuid}_compressed_{file_name}"
    # with open("required.jpg", "wb") as imf:
    #    return imf.write(path)
    # f.write()
    # f.close()

    # with open('./datacompressed.jpg','wb') as f:
    #     shutil.copyfileobj(fi.read(), f)
    # print('Image sucessfully Downloaded: ',file_name)

    # return HttpResponse(status=200)
    #  return fin
    # return f"/tmp/{my_uuid}_compressed_{file_name}"
    # return res
def gen_uuid():
    return str(uuid.uuid4().hex)
