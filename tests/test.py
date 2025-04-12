import pickle
import multiprocessing

class SelfReferencingClass:
    def __init__(self, name, value=0):
        self.name = name  # 普通字段
        self.value = value  # 普通字段
        self.references = []  # 存储同类对象的list
    
    # 往list里面添加数据
    def add_reference(self, obj):
        if isinstance(obj, SelfReferencingClass):
            self.references.append(obj)
    
    def __repr__(self):
        ref_names = [ref.name for ref in self.references]
        return f"SelfReferencingClass(name='{self.name}', value={self.value}, references={ref_names})"

def child_process(conn):
    print("子进程启动，等待接收对象...")
    # 接收序列化数据
    serialized_data = conn.recv()
    print("子进程接收到序列化数据")
    
    # 反序列化对象
    obj = pickle.loads(serialized_data)
    print("子进程反序列化后的对象:", obj)
    
    # 验证引用关系
    if obj.references:
        print(f"子进程中 {obj.name} 引用的对象: {obj.references[0].name}")
    else:
        print("子进程中对象没有引用")
    
    conn.close()

def main():
    # 创建两个互相引用的对象
    obj1 = SelfReferencingClass("对象1", 100)
    obj2 = SelfReferencingClass("对象2", 200)
    
    obj1.add_reference(obj2)
    obj2.add_reference(obj1)
    
    print("原始对象:")
    print("obj1:", obj1)
    print("obj2:", obj2)
    
    # 创建进程通信管道
    parent_conn, child_conn = multiprocessing.Pipe()
    
    # 启动子进程
    p = multiprocessing.Process(target=child_process, args=(child_conn,))
    p.start()
    
    # 序列化其中一个对象
    print("父进程序列化 obj1...")
    serialized_obj = pickle.dumps(obj1)
    
    # 发送给子进程
    parent_conn.send(serialized_obj)
    print("父进程已发送序列化数据")
    
    # 等待子进程结束
    p.join()
    
    # 验证父进程中的对象是否仍然正常
    print("\n父进程验证原始对象:")
    print("obj1:", obj1)
    print("obj1引用的对象:", obj1.references[0] if obj1.references else "无")
    print("obj2:", obj2)
    print("obj2引用的对象:", obj2.references[0] if obj2.references else "无")

if __name__ == "__main__":
    main()