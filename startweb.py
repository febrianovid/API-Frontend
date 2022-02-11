from os import name
from re import X
# from typing import final
from flask import *
import requests
# from requests.api import post
import numpy as np
import base64
import cgi
from markupsafe import Markup
import cv2
# from werkzeug.utils import append_slash_redirect

app = Flask(__name__)

list_of_endpoint = []
markup_list = []


def post_image(img, urllink):
    """Posting image"""
    files = {'image': img}
    response = requests.post(url=urllink, files=files)
    return response


flist = list()


@app.route('/', methods=['POST', 'GET'])
def success():
    global list_of_endpoint
    global markup_list

    ## MODULE1 : Check URL Gateway for available API
    response = requests.get(url='http://172.17.0.142:10001/check')
    any_other_result = response.json()
    print("list was", any_other_result)
    print("was : ", len(any_other_result))
    list_of_endpoint = []
    markup_list = []

    for i in range(len(any_other_result)):
        endpoint_list = any_other_result[i]['endpoint']
        endpoint_status = any_other_result[i]['response_code']
        if endpoint_status == 200:
            list_of_endpoint.append(endpoint_list)
    print("list now : ", list_of_endpoint)
    print("now : ", len(list_of_endpoint))

    for active_endpoint in list_of_endpoint:
        markup_list.append(
            Markup(
                '<a href="#testimonial" name="{}" onclick="setValue(this.name)">{}</a>'
                .format(active_endpoint, active_endpoint)))
    ## END OF MODULE1

    ## MODULE2 : Choosing type of API
    if request.method == 'POST':

        result = request.form['jump_to_python']
        print("what i got:", result)

        if result == 'object':
            urllink = 'http://172.17.0.216:8080/gfl'
        elif result == 'gender':
            urllink = 'http://172.17.11.34:2000/app'
        elif result == 'color':
            urllink = 'http://172.17.11.34:4000/app'
        else:
            urllink = 'http://172.17.0.142:10001/tasks/{}'.format(result)

    ## MODULE3 : Resquest uploaded Image
        data = dict()
        f = request.files['fileimg']
        print("Image when first requested Type : ", type(f))
        image_io = f.read()

        ## MODULE4 : Change Image type and send it to API Backend
        print("Image IO Type : ", type(image_io))
        nparr = np.fromstring(image_io, np.uint8)
        img_base = base64.b64encode(nparr)
        print("Image base Type : ", type(img_base))
        # Change image type so it can be shown on hmtl page
        # image should be a string type because bytes can't
        img_base64 = img_base.decode('ascii')
        print("Image base 64 Type : ", type(img_base64))
        data["data"] = img_base64
        flist.append(data)
        # Sending Image to the API BACKEND (Function post_image)
        response = post_image(image_io, urllink)
        result = response.json()
        ## MODULE5 : Receiving result of Image Detection
        print("ACTUAL RESULTS : ", result)

        # Retrieving data from the result

        task_type = result['task']
        label_is = result['label']
        result_details = result['results']

        # Checking If result isn't empty (Detecting successful)

        if len(result_details) == 0:
            return render_template(
                "index.html",
                anchor_id="contact",
                result="Unidentified Object for this Engine",
                img_base64=img_base64,
                new_endpoint=markup_list)
        else:
            pass

        print("TASK : ", task_type)
        print("RESULTS :", result_details)
        image_with_boundingbox = cv2.imdecode(np.fromstring(nparr, np.uint8),
                                              cv2.IMREAD_COLOR)
        IMG_HEIGHT, IMG_WIDTH, _ = image_with_boundingbox.shape

        # DETERMINING IF IT DETECTION-CLASSIFICATION or DETECTION or CLASSIFFICATION

        # IF IT DETECTION-CLASSIFICATION or DETECTION
        if task_type == 'detection-classification' or task_type == 'detection':
            total_object = 0
            for i in range(len(result_details)):
                try:
                    print(result_details[i]['bbox'])
                except:
                    continue
                # DRAWING BOUNDING BOX
                bounding_box = result_details[i]['bbox']
                print(f"BOUNDING BOX{[i]} : ", bounding_box)
                xy_min = (bounding_box[0], bounding_box[1])
                xy_max = (bounding_box[2], bounding_box[3])
                box = 2
                color = (0, 0, 255)
                image_with_boundingbox = cv2.rectangle(image_with_boundingbox,
                                                       xy_min, xy_max, color,
                                                       box)
                total_object += 1
                if 'class' in result_details[i]:
                    task_type == 'detection-classification'
                    print("LABEL IS : ", label_is)
                    final_result = (f"Task : {task_type.title()} , ")
                    age_gender = ""

                    for i, class_result in enumerate(
                            result_details[i]['class']):
                        print(f"RESULT OF CLASS{[i]} : {class_result}")
                        print(f"FROM LABEL{[i]} {label_is[i]}")
                        age_gender += f"{class_result} "
                    final_result += f"Total Object : {total_object} Detected !"
                    cv2.putText(image_with_boundingbox, f'{age_gender}',
                                (xy_min[0], xy_min[1] - 7),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                min(IMG_HEIGHT, IMG_WIDTH) / 1000, (0, 0, 0),
                                1)

                else:
                    final_result = (
                        f"Task : {task_type.title()} , API Type : {request.form['jump_to_python'].title()} ,  Total : {total_object} Object Detected ! "
                    )
            # RETURN OF IMAGE TYPE THAT CHANGED ALREADY
            return_value, encoded_jpg_img_bbox = cv2.imencode(
                ".jpg", image_with_boundingbox)
            imgnow = base64.b64encode(encoded_jpg_img_bbox)
            img_base64 = imgnow.decode('ascii')

        # IF IT CLASSIFICATION
        else:

            for i in range(len(result_details)):
                if result_details[i]['class'] != 0:
                    confidence_is = (result_details[i]['confidence'])
                    continue
                else:
                    continue

            final_result = (f"Task : {task_type.title()} ")
            class_result = result_details[0]['class']

            for i, class_result in enumerate(class_result):
                final_result += " , "
                final_result += f"{label_is[i].title()} : {class_result.title()} with confidence = {confidence_is[i]} "

        code = response.status_code

        ## MODULE6 : Checking Conection Status Code and Return All Progress Result
        if code == 200:
            if len(result) == 0:
                print('Posting Status : ', (response.status_code))
                return render_template("index.html",
                                       anchor_id="contact",
                                       result="Unidentified Object",
                                       img_base64=img_base64,
                                       new_endpoint=markup_list)
            print('Posting Status : ', (response.status_code))
            return render_template("index.html",
                                   anchor_id="contact",
                                   result=final_result,
                                   img_base64=img_base64,
                                   new_endpoint=markup_list)
        elif code == 300 or 400 or 500:
            print('Posting Status : ', (response.status_code))
            return render_template("index.html",
                                   anchor_id="contact",
                                   result="Unidentified Object",
                                   img_base64=img_base64,
                                   new_endpoint=markup_list)
    # Affiliate with MODULE1 (Rendering HTML Page with list of available Endpoint)
    if request.method == 'GET':
        return render_template("index.html",
                               anchor_id="",
                               new_endpoint=markup_list)


# Running FlaskApp
if __name__ == '__main__':
    app.run(debug=True)