#!/usr/bin/python
#coding=utf8

import test_pb2
  
testinfo = test_pb2.testinfo()  
testinfo.devtype = 100  
testinfo.devid = 2  
testinfo.unitid = 3  
testinfo.chlid = 4  
testinfo.testid = 250
testinfo.stepdata = b'abd'

print("#"*50)
print(testinfo, testinfo.devtype)  # 打印 protobuf 结构的内容
out = testinfo.SerializeToString()  
print("#"*50)
print(out)  # 打印 Protobuf 序列字符串
  
  
decode = test_pb2.testinfo()  
decode.ParseFromString(out)  
print("#"*50)
print(decode) # 打印 解析Protobuf后的内容














# https://github.com/google/protobuf/releases



# 解压到protobuf-2.6.0
# cd protobuf-2.6.0\python
# python setup.py build
# python setup.py install

# 下载protoc
# 解压到C:\protoc
# 设置环境变量
# setx PATH "%PATH%;C:\protoc\bin"
# echo %path%
# protoc --version
# 编写test.proto
# protoc --python_out=./ test.proto
# 生成test_pb2.py文件
# 安装protobuf python模块

