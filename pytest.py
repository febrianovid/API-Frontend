plate_list = [{"plate": "abc123"}, {"plate": "def678"}]

# print(type(plate_list))

#1
print("1 : ", plate_list[0])

#2
car_plate_dict = {"plate": "zxy6060"}
print("2 : ", car_plate_dict["plate"])

#3
print("3 : ", plate_list[1]['plate'])

#4
for i in range(len(plate_list)):
    print(plate_list[i]['plate'])
    min = (36, 6)
    min[1]=7
    print(min[1]-1)
    # min[1]-=min[1] 
