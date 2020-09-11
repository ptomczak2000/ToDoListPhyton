from datetime import datetime, timedelta
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///todo.db')
Base = declarative_base()


class Task(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True, unique=True)
    task = Column(String, default=' o results a')
    deadline = Column(Date, default=datetime.today().date().strftime('%-d %b'))

    def __repr__(self):
        return self.string_field


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


def add_tasks():
    new_row = Task(task=None, deadline=None)
    print("Enter task")
    new_row.task = input()
    print("Enter deadline")
    new_row.deadline = datetime.strptime(input(), '%Y-%m-%d')
    session.add(new_row)
    session.commit()


def delete_tasks():
    rows = session.query(Task).order_by(Task.deadline).all()
    ID = 1
    print("")
    if session.query(Task).order_by(Task.deadline).first() is None:
        print("Nothing to delete")
    else:
        print("Choose the number of the task you want to delete:")
        for task in rows:
            print("{}. {}. {}".format(ID, task.task, task.deadline.strftime('%-d %b')))
            ID += 1
        row_to_delete = rows[int(input()) - 1]
        session.delete(row_to_delete)
        print("The task has been deleted!")
    print("")
    session.commit()


def display_today_tasks():
    today = str(datetime.today().strftime('%-d %b'))
    tasks = session.query(Task).filter(Task.deadline == datetime.today().date()).all()
    print(f'Today {today}:')
    id = 1
    if session.query(Task).filter(Task.deadline == datetime.today().date()).first() is None:
        print("Nothing to do!")
    else:
        for task in tasks:
            print(f'{id}. {task.task}')
            id += 1


def display_missed_tasks():
    rows = session.query(Task).filter(Task.deadline < datetime.today().date()).all()
    ID = 1
    print("")
    print("Missed tasks:")
    if session.query(Task).filter(Task.deadline < datetime.today().date()).first() is None:
        print("Nothing is missed!")
    else:
        for task in rows:
            print("{}. {}. {}".format(ID, task.task, task.deadline.strftime('%-d %b')))
            ID += 1
    print("")


def display_weeks_tasks():
    today = datetime.today().date()
    for i in range(0, 7):
        i_day = today + timedelta(days=i)
        i_rows = session.query(Task.id, Task.task, Task.deadline).filter(Task.deadline == i_day).order_by(
            Task.deadline).all()
        print(f'{i_day.strftime("%A")} {i_day.day} {i_day.strftime("%b")}')
        if len(i_rows) == 0:
            print("Nothing to do!")
        else:
            count = 1
            for j in i_rows:
                print(f'{count}. {j.task}')
                count += 1
        print()


def display_all_day_tasks(date):
    tasks = session.query(Task).filter(Task.deadline == date).all()
    ID = 1
    print("{}:".format(date.strftime('%A %d %b')))
    if session.query(Task).filter(Task.deadline == date).first() is None:
        print("Nothing to do!")
    else:
        for task in tasks:
            print("{}. {}".format(ID, task.task))
            ID += 1


def display_all_tasks():
    tasks = session.query(Task).order_by(Task.deadline).all()
    ID = 1
    for task in tasks:
        if session.query(Task).first() is None:
            print("Nothing to do!")
        else:
            print("{}. {}. {}".format(ID, task.task, task.deadline.strftime('%-d %b')))
        ID += 1


def menu():
    print("""1) Today's tasks
2) Week's tasks
3) All tasks
4) Missed tasks
5) Add task
6) Delete task
0) Exit""")
    return int(input())


if __name__ == '__main__':
    loop = 1
    choice = 0
    while loop == 1:
        choice = menu()
        if choice == 1:
            display_today_tasks()
        elif choice == 2:
            display_weeks_tasks()
        elif choice == 3:
            display_all_tasks()
        elif choice == 4:
            display_missed_tasks()
        elif choice == 5:
            add_tasks()
        elif choice == 6:
            delete_tasks()
        else:
            loop = 0
            print("Bye!")
