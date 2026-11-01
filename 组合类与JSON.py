import json
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
    def to_dict(self):
         return {"title":self.title,"completed":self.completed}
class TodoList:
    def __init__(self):
        self.task_list = []
    def add_task(self,task_title):
        new_task = Task(task_title)
        self.task_list.append(new_task)
    def show(self):
        if len(self.task_list) == 0:
            print("无待做任务")
            return
        print ("待做任务：\n")
        for index,task in enumerate(self.task_list):
            print(f"{index+1}.",end=" ")
            task.show()
    def delete_task(self,index):
        if 0 <= index < len(self.task_list):
            del self.task_list[index]
            print("删除任务操作成功！")
        else:
            print("未查找到所输入序号！删除任务失败！")
    def save_to_json(self,filename):
        data =[]
        for task in self.task_list:
            data.append(task.to_dict())
        with open(filename,"w",encoding = "utf-8") as f:
            json.dump(data,f,ensure_ascii=False,indent=2)
        print("保存成功！")
    def load_from_json(self,filename):
        try:
            with open(filename,"r",encoding = "utf-8") as f:
                data = json.load(f)
            self.task_list = []
            for item in data:
                t = Task(item["title"])
                if item["completed"]:
                    t.mark_finish()
                self.task_list.append(t)
            print("文件读取成功！")
        except FileNotFoundError:
            print("无法查找到文件！无待做任务！")
todo = TodoList()
todo.load_from_json("todoList.json")
todo.add_task("玩儿原神")
todo.add_task("站中间，串两边")
todo.add_task("看哈利波特")
todo.show()
todo.task_list[0].mark_finish()
print("\n标记第一个任务完成后：")
todo.show()
todo.save_to_json("todoList.json")
input("输入回车，关闭弹窗")
