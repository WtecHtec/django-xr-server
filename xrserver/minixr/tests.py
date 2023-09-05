# from django.test import TestCase

# Create your tests here.
from proto import user_pb2
#! /usr/bin/env python

user = user_pb2.User()

user.name = 'Bill'
user.age = 30

#序列化
serializeToString = user.SerializeToString()
print(serializeToString,type(serializeToString))


user.ParseFromString(b'\x02\x04Bill\x08\x1e')
# user.ParseFromString(b'\n\x04Bill\x10\x1e')
print(user)

# for person in address_book.people:
#   print("p_id{},p_name{},p_email{},p_money{},p_workstatu{}"
#         .format(person.id,person.name,person.email,person.money,person.work_status))

#   for phone_number in person.phones:
#     print(phone_number.number,phone_number.type)


#   for key in person.maps.mapfield:
#     print(key,person.maps.mapfield[key])


# from proto import addbooks_pb2

# address_book = addbooks_pb2.AddressBook()
# person = address_book.people.add()

# person.id = 1
# person.name = "safly"
# person.email = "safly@qq.com"
# person.money = 1000.11
# person.work_status = True

# phone_number = person.phones.add()
# phone_number.number = "123456"
# phone_number.type = addbooks_pb2.MOBILE

# maps = person.maps
# maps.mapfield[1] = 1
# maps.mapfield[2] = 2

# #序列化
# serializeToString = address_book.SerializeToString()
# print(serializeToString,type(serializeToString))



# address_book.ParseFromString(serializeToString)

# for person in address_book.people:
#   print("p_id{},p_name{},p_email{},p_money{},p_workstatu{}"
#         .format(person.id,person.name,person.email,person.money,person.work_status))

#   for phone_number in person.phones:
#     print(phone_number.number,phone_number.type)


#   for key in person.maps.mapfield:
#     print(key,person.maps.mapfield[key])




print('test')