import json
class Task:
    def __init__(self, title):
        self.title = title
        self.completed = False
    def mark_finish(self):
        self.completed = True
    def change_title(self, new_title):
        self.title = new_title
    def to_dict(self):
        return {"title": self.title, "completed": self.completed}
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
            status = "已完成"if task.completed else "待完成"
            print(f"{index+1}.{task.title}:{status}")
        print("\n")
    def mark_task_finish(self,index):
        if 0 <= index < len(self.task_list):
            self.task_list[index].mark_finish()
            print("成功标记任务！")
        else:
            print("序号不存在！")
    def delete_task(self,index):
        if 0 <= index < len(self.task_list):
            del self.task_list[index]
            print("删除任务操作成功！")
        else:
            print("未查找到所输入序号！该序号不存在！删除任务失败！")
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
            print("历史数据读取成功！")
        except FileNotFoundError:
            print("无历史数据文件！新建清单")
def show_menu():
    print("代办任务如下：")
    print("1.新任务")
    print("2.全部任务")
    print("3.标记任务完成")
    print("4.删除任务")
    print("5.退出菜单")
    print("\n")
if __name__ == "__main__":
    todo = TodoList()
    FILE_NAME = "todoList.json"
    todo.load_from_json(FILE_NAME)
    while True:
        show_menu()
        choice = input("请输入你需要的功能编号：")
        if choice == "1":
            title = input("输入任务内容：")
            todo.add_task(title)
            print("添加任务成功！")
        elif choice == "2":
            todo.show()
        elif choice == "3":
            todo.show()
            num = int(input("输入要标记完成的任务序号："))
            todo.mark_task_finish(num - 1)
        elif choice == "4":
            todo.show()
            num = int(input("输入要删除的任务序号："))
            todo.delete_task(num - 1)
        elif choice == "5":
            todo.save_to_json(FILE_NAME)
            print("数据已保存，菜单退出！")
            break
        else:
            print("输入无效，请重新输入！")