# from flask import Flask, render_template, request
# from markupsafe import Markup

# app = Flask(__name__)

# @app.route('/')
# def index():
#     return render_template('indexx.html',new_url=[Markup('<a href="#">hjgjhg</a>'),Markup("<a>hjgjhg2</a>"),Markup("<a>hjgjhg3</a>")])

# @app.route('/', methods=['POST'])
# def test():
#     # first_name = request.form['first_name']
#     # last_name = request.form['last_name']
#     # print(first_name, last_name)
#     # return ("okay")
#     result = request.form['jump_to_python']
#     print("CHOSEN ENGINE :", result)
#     return result

# if __name__ == '__main__':
#     app.run(debug=True)

# number_is =[1,2,3,4,5,6,7]
# for i in range(len(number_is)):
#     print("number : ",i)

# a=""
# LENGTH=10
# for i in range(LENGTH):
#     a+=str(i)
#     if i!=LENGTH-1:
#         a+=","
#     else:
#         continue
# print("----------------")
# print(a)
# print("----------------")

import cv2
import numpy as np

img = cv2.pyrDown(
    cv2.imread('People-Times-Square-New-York-City-May-8-1945.jpg',
               cv2.IMREAD_UNCHANGED))

ret, threshed_img = cv2.threshold(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), 127,
                                  255, cv2.THRESH_BINARY)

contours, hier = cv2.findContours(threshed_img, cv2.RETR_TREE,
                                  cv2.CHAIN_APPROX_SIMPLE)

for c in contours:
    x, y, w, h = cv2.boundingRect(c)
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

    rect = cv2.minAreaRect(c)
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    cv2.drawContours(img, [box], 0, (0, 0, 255))

    (x, y), radius = cv2.minEnclosingCircle(c)
    center = (int(x), int(y))
    radius = int(radius)
    img = cv2.circle(img, center, radius, (255, 0, 0), 2)

print(len(contours))
cv2.drawContours(img, contours, -1, (255, 255, 0), 1)

cv2.imshow("contours", img)

cv2.imshow("contours", img)


def cal_dist(p1, p2, distance_w, distance_h):
    pass


bottom_point = []

r = []
g = []
y = []
bxs = []
distances_mat = []
for i in range(len(distances_mat)):
    if distances_mat[i][2] == 0:
        if (distances_mat[i][0]
                not in r) and (distances_mat[i][0]
                               not in g) and (distances_mat[i][0] not in y):
            r.append(distances_mat[i][0])
        if (distances_mat[i][1]
                not in r) and (distances_mat[i][1]
                               not in g) and (distances_mat[i][1] not in y):
            r.append(distances_mat[i][0])
for i in range(len(distances_mat)):
    if distances_mat[i][2] == 1:
        if (distances_mat[i][0]
                not in r) and (distances_mat[i][0]
                               not in g) and (distances_mat[i][0] not in y):
            y.append(distances_mat[i][0])
        if (distances_mat[i][1]
                not in r) and (distances_mat[i][1]
                               not in g) and (distances_mat[i][1] not in y):
            y.append(distances_mat[i][1])
for i in range(len(distances_mat)):
    if distances_mat[i][2] == 2:
        if (distances_mat[i][0]
                not in r) and (distances_mat[i][0]
                               not in g) and (distances_mat[i][0] not in y):
            g.append(distances_mat[i][0])
        if (distances_mat[i][1]
                not in r) and (distances_mat[i][1]
                               not in g) and (distances_mat[i][1] not in y):
            g.append(distances_mat[i][1])
boxes1 = []
distance_w = []
distance_h = []
cal_dis=[]

for i in range(len(bottom_point)):
    for j in range(len(bottom_point)):
        if i != j:
            dist = cal_dis(bottom_point[i], bottom_point[j], distance_w,
                           distance_h)
            if dist <= 150:
                closeness = 0
                distances_mat.append(
                    [bottom_point[i], bottom_point[j], closeness])
                bxs.append([boxes1[i], boxes1[j], closeness])
            elif dist > 150 or dist <= 180:
                closeness = 1
                distances_mat.append(bottom_point[i], bottom_point[j],
                                     distance_w, distance_h)
            else:
                closeness = 2
                distances_mat.append(bottom_point[1], bottom_point[j],
                                     distance_w, distance_h)

while True:
    key = cv2.waitKey(1)
    if key == 27:
        break
cv2.destroyAllWindows()