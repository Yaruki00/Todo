import os
from elixir import *

dbdir = os.path.join(os.path.expanduser("~"), ".pyqtodo")
dbfile = os.path.join(dbdir, "tasks.sqlite")

class Task(Entity):
    using_options(tablename='tasks')
    text = Field(Unicode, required = True)
    date = Field(DateTime, default = None, required = False)
    done = Field(Boolean, default = False, required = True)
    tags = ManyToMany("Tag")

    def __repr__(self):
        return "Task: " + self.text

class Tag(Entity):
    using_options(tablename = 'tags')
    name = Field(Unicode, required = True)
    tasks = ManyToMany("Task")

    def __repr__(self):
        return "Tag: " + self.name

saveData = None

def initDB():
    if not os.path.isdir(dbdir):
        os.mkdir(dbdir)
    metadata.bind = "sqlite:///%s"%dbfile
    setup_all()
    if not os.path.exists(dbfile):
        create_all()

    global saveData
    import elixir
    if elixir.__version__ < "0.6":
        saveData = session.flush
    else:
        saveData = session.commit

def main():
    initDB()

    green = Tag(name = u"green")
    red = Tag(name = u"red")

    tarea1 = Task(text = u"Buy tomatos", tags = [red])
    tarea2 = Task(text = u"Buy chili", tags = [red])
    tarea3 = Task(text = u"Buy lettuce", tags = [green])
    tarea4 = Task(text = u"Buy strawberries", tags = [red, green])
    saveData()

    print "Green Tasks:"
    print green.tasks
    print
    print "Red Tasks:"
    print red.tasks
    print
    print "Task with l:"
    print [(t.id, t.text, t.done) for t in Task.query.filter(Task.text.like(ur'%l%')).all()]

if __name__ == "__main__":
    main()
