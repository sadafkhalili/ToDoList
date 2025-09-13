
from datetime import datetime

class TaskManager:
    def __init__(self, filename="tasks.txt"):
        self.filename = filename
        self.tasks = []
        self.load_tasks()
    
    def load_tasks(self):
        # بارگذاری وظایف از فایل متنی
        self.tasks = []
        try:
            with open(self.filename, 'r') as f:
                for line in f:
                    if line.strip():
                        task_data = line.strip().split('|')
                        if len(task_data) >= 6:
                            task = {
                                "id": int(task_data[0]),
                                "title": task_data[1],
                                "description": task_data[2],
                                "priority": int(task_data[3]),
                                "completed": task_data[4] == "True",
                                "created_at": task_data[5]
                            }
                            self.tasks.append(task)
        except FileNotFoundError:
            # اگر فایل وجود نداشته باشد، لیست tasks خالی باقی می‌ماند
            self.tasks = []
        except:
            self.tasks = []
    
    def save_tasks(self):
        # ذخیره وظایف در فایل متنی
        with open(self.filename, 'w') as f:
            for task in self.tasks:
                line = f"{task['id']}|{task['title']}|{task['description']}|{task['priority']}|{task['completed']}|{task['created_at']}\n"
                f.write(line)
    
    def add_task(self, title, description="", priority=1):
        # افزودن وظیفه جدید
        if not title.strip():
            return False
        
        new_task = {
            "id": len(self.tasks) + 1,
            "title": title.strip(),
            "description": description.strip(),
            "priority": priority,
            "completed": False,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        self.tasks.append(new_task)
        self.save_tasks()
        return True
    
    def complete_task(self, task_id):
        # علامت گذاری وظیفه به عنوان انجام شده
        for task in self.tasks:
            if task["id"] == task_id:
                task["completed"] = True
                self.save_tasks()
                return True
        return False
    
    def remove_task(self, task_id):
        # حذف وظیفه
        for i, task in enumerate(self.tasks):
            if task["id"] == task_id:
                del self.tasks[i]
                self.save_tasks()
                return True
        return False
    
    def get_tasks(self, show_completed=False):
        # دریافت لیست وظایف
        if show_completed:
            return self.tasks
        return [task for task in self.tasks if not task["completed"]]
    
    def search_tasks(self, keyword):
        # جستجو در وظایف
        keyword = keyword.lower()
        return [
            task for task in self.tasks 
            if keyword in task["title"].lower() or keyword in task["description"].lower()
        ]
    
    def clear_completed(self):
        # حذف تمامی وظایف انجام شده
        initial_count = len(self.tasks)
        self.tasks = [task for task in self.tasks if not task["completed"]]
        removed_count = initial_count - len(self.tasks)
        if removed_count > 0:
            self.save_tasks()
        return removed_count

def display_tasks(tasks):
    # نمایش وظایف در کنسول
    if not tasks:
        print("No tasks found.")
        return
    
    
    print("TASK LIST")
    
    
    for task in tasks:
        status = "DONE" if task["completed"] else "PENDING"
        priority_str = "!" * task["priority"]
        
        print(f"{task['id']:>2}. {status} - {task['title']} {priority_str}")
        if task["description"]:
            print(f"   Description: {task['description']}")
        print(f"   Created: {task['created_at']}")
        
def main():
    manager = TaskManager()
    
    while True:
        
        print("TASK MANAGER - MAIN MENU")
        print("="*40)
        print("1. View tasks")
        print("2. Add new task")
        print("3. Complete task")
        print("4. Delete task")
        print("5. Search tasks")
        print("6. Clear completed tasks")
        print("0. Exit")
        
        choice = input("\nEnter your choice: ").strip()
        
        if choice == "1":
            show_completed = input("Show completed tasks? (y/n): ").lower() == 'y'
            tasks = manager.get_tasks(show_completed)
            display_tasks(tasks)
            
        elif choice == "2":
            title = input("Task title: ")
            description = input("Description (optional): ")
            try:
                priority = int(input("Priority (1-5, default 1): ") or "1")
                priority = max(1, min(5, priority))
            except:
                priority = 1
                
            if manager.add_task(title, description, priority):
                print("Task added successfully.")
            else:
                print("Task title cannot be empty.")
                
        elif choice == "3":
            try:
                task_id = int(input("Enter task ID to complete: "))
                if manager.complete_task(task_id):
                    print("Task marked as completed.")
                else:
                    print("Task not found.")
            except:
                print("Please enter a valid number.")
                
        elif choice == "4":
            try:
                task_id = int(input("Enter task ID to delete: "))
                if manager.remove_task(task_id):
                    print("Task deleted successfully.")
                else:
                    print("Task not found.")
            except:
                print("Please enter a valid number.")
                
        elif choice == "5":
            keyword = input("Search keyword: ")
            results = manager.search_tasks(keyword)
            display_tasks(results)
            
        elif choice == "6":
            removed_count = manager.clear_completed()
            print(f"Removed {removed_count} completed tasks.")
            
        elif choice == "0":
            print("Goodbye!")
            break
            
        else:
            print("Invalid choice. Please enter a number between 0-6.")

if __name__ == "__main__":
    main()