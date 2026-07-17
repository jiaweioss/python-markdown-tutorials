"""Chapter 02 demo: create Python's four common containers."""

scores = [86, 92, 78]
participant = ("P001", 19)
skills = {"Python", "文件", "Python"}
student = {"name": "小明", "age": 19}

empty_list = []
empty_tuple = ()
empty_set = set()
empty_dict = {}
one_item_tuple = ("Python",)

print("列表：", scores)
print("元组：", participant)
print("集合（重复项被去除）：", skills)
print("字典：", student)
print("空容器：", empty_list, empty_tuple, empty_set, empty_dict)
print("单元素元组：", one_item_tuple)
