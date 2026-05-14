"""
你正在开发一个图书管理系统，需要编写 Python 代码来处理图书信息。

已知有一个图书列表 books，记录图书编号(book_id)和书名(book_name)，一个作者列表，记录作者名称(author)和图书编号(book_id)。
请使用函数嵌套调用的方式编写代码，实现以下功能：

创建一个函数 search_book_by_author(authors, author)，根据作者名称获取其编写的所有图书名
创建一个函数 get_book_info(books, book_id)，根据图书编号获取图书的名称。
在 search_book_by_author(authors, author) 函数内部，通过调用 get_book_info(books, book_id) 函数来获取每本图书的图书名。
在主程序中调用 search_book_by_author(authors, author) 函数，并输出符合要求的图书名称。
请编写上述要求的代码，并输出符合要求的图书名称。

authors = [
    {
        "book_id": 1,
        "author": "张三"
    },
    {
        "book_id": 2,
        "author": "李四"
    },
    {
        "book_id": 3,
        "author": "张三"
    },
    {
        "book_id": 4,
        "author": "王五"
    },

]
books = [
    {
        "book_id": 1,
        "book_name": "Python编程入门",
    },
    {
        "book_id": 2,
        "book_name": "Java从入门到精通",
    },
    {
        "book_id": 3,
        "book_name": "数据结构与算法",
    },
    {
        "book_id": 4,
        "book_name": "深入理解计算机系统",
    }
]
"""
authors = [
    {
        "book_id": 1,
        "author": "张三"
    },
    {
        "book_id": 2,
        "author": "李四"
    },
    {
        "book_id": 3,
        "author": "张三"
    },
    {
        "book_id": 4,
        "author": "王五"
    },

]
books = [
    {
        "book_id": 1,
        "book_name": "Python编程入门",
    },
    {
        "book_id": 2,
        "book_name": "Java从入门到精通",
    },
    {
        "book_id": 3,
        "book_name": "数据结构与算法",
    },
    {
        "book_id": 4,
        "book_name": "深入理解计算机系统",
    }
]

def search_book_by_author(authors, author):  # 输入作者名返回作者的书的信息 内部调用函数
    # 输入作者名后，得到作者的书籍id，再调用函数得到书记信息
    list_ = []
    for name in authors:
        if name["author"] == author:
            list_.append(get_book_info(books,name["book_id"]))
    return list_

def get_book_info(books, book_id): #输入书的id返回书的信息
    for book in books:
        if book['book_id'] == book_id:
            return book
    else:
        return "找求不到"
print(search_book_by_author(authors,input()))