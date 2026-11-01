class Task:
    def __init__(self, title):
        self.title = title
        self.completed = False
    def mark_finish(self):
        self.completed = True
    def mark_canceled(self):
        self.completed = False
    def show(self):
        if self.completed:
            status = "已完成"
        else:
            status = "未完成"
        print(f"任务：{self.title}，完成状况：{status}")
t1 = Task("玩儿原神")
t2 = Task("站中间，串两边")
t3 = Task("看哈利波特")
print("未修改")
t1.show()
t2.show()
t3.show()
t1.mark_finish()
print ("\n修改t1后")
t1.show()
t2.show()
t3.show()
t1.mark_canceled()
print("\n撤销修改")
t1.show()
t2.show()
t3.show()
input("输入回车，关掉窗口")
