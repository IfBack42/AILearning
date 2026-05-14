'''
手工输入一个文件名称，判断点号所在的位置（上传）
.jpg/.png/.gif
'''
filename = input('请输入要上传文件的名称：')
# 判断点号是否存在，如果存在，在哪个位置
# print(filename.find('.'))
if filename.find('.') > 0:
    print('合理图片')
else:
    print('您上传的图片有误，请重新上传')