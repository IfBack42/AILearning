products = {'大白菜', '胡萝卜', '西红柿', '山药'}

# 1、remove()：根据元素的值删除元素
# products.remove('水蜜桃')
# print(products)

# 2、discard()：功能与remove类似，但是如果元素不存在，discard不会报错
# products.discard('水蜜桃')
# print(products)

# 3、pop()：随机删除集合中的某个元素（无法确定）
del_data = products.pop()
print(del_data)