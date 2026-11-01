import json
class Note:
    def __init__(self,name,item,price,paid):
        self.name = name
        self.item = item
        self.price= price
        self.paid = paid
    def to__dict(self):
        return {"name":self.name,"item":self.item,"price":self.price,}
    def turn_record(d):
        return Note(d["name"],d["item"],d["price"],d["paid"])

