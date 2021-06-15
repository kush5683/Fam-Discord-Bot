import asyncio
import discord
import os
from discord.ext import commands
from pprint import pprint
import json
from enum import Enum
from datetime import datetime
import re
import threading


def getTimeStamp():
    return datetime.now().strftime('%Y-%m-%d-%H-%M-%S')


def getDateTime():
    return datetime.now()


class TaskCommands(commands.Cog):
    class taskStatus(Enum):
        ACTIVE = 0
        CANCEL = 1
        COMPLETE = 2

    class timeUnit(Enum):
        unit = 0
        SECONDS = 1
        MINUTES = 60
        HOURS = 3600
        DAYS = 86400

        def __mul__(self, other):
            return self.value * int(other)

    class Task():
        # Task(encoded, value, timeUnit[unit.upper()], name, ctx)
        def __init__(self, encoding, value=None, unit=None, name=None, ctx=None):
            self.value, self.unit, self.name, self.timestamp, self.authorName, self.guild, self.channel = encoding.split(
                ":")
            if self.unit.upper() == "SECOND":
                self.unit = "seconds"
            elif self.unit.upper() == "MINUTE":
                self.unit = "minutes"
            elif self.unit.upper() == "HOUR":
                self.unit = "hours"
            self.unit = TaskCommands.timeUnit[self.unit]
            self.time = self.unit * self.value
            self.encoding = encoding
            self.timestamp = [int(num) for num in self.timestamp.split("-")]
            self.origin = datetime(self.timestamp[0], self.timestamp[1], self.timestamp[2],
                                   self.timestamp[3], self.timestamp[4], self.timestamp[5])
            self.status = TaskCommands.taskStatus.ACTIVE
            self.__attr = {
                "Value": self.value,
                "Unit": self.unit,
                "Name": self.name,
                "Author": self.authorName,
                "Time": self.time,
                "Status": self.status,
                "Encoding": self.encoding
            }

        def getTask(self):
            return self.__attr

        def getTime(self):
            now = getDateTime()
            timepassed = now-self.origin
            self.time = self.time-timepassed.total_seconds()
            return self.time

        def fromName(self, name):
            for t in self.tasksGlobal:
                if t.name == name:
                    return t

        def changeStatus(self, status):
            self.__attr.update({"Status": status})
            self.status = status

    class memberAttribute():
        def __init__(self, member):
            self.member = member
            self.__attr = {
                "Name": member.name,
                "Nickname": member.nick,
                "Roles": [role.name for role in member.roles if role.name != "@everyone"],
                "Active tasks": [],
                "Completed tasks": [],
            }

        def getAttributes(self):
            return self.__attr

        def toJSON(self):
            with open(f"../profiles/{self.member.name}.json", "w") as outfile:
                json.dump(self.__attr, outfile)

        def moveTask(self, taskname):
            pass

    def __init__(self, client):
        self.dir = os.getcwd()
        os.chdir("..")
        os.chdir("profiles")
        self.profileDir = os.getcwd()
        os.chdir(self.dir)
        self.client = client
        self.tasksGlobal = []
        self.loadTaskThreads()
        print("Task commands loaded")

    def checkRole(self, ctx, desiredRole):
        ans = False
        for role in ctx.author.roles:
            if str(role) == desiredRole:
                ans = True
        return ans

    def moveTask(self, task):

        guild = None
        for g in self.client.guilds:
            if int(g.id) == int(task.guild):
                guild = g

        channel = None
        for c in guild.channels:
            if int(c.id) == int(task.channel):
                channel = c

        author = None
        for member in guild.members:
            if int(member.id) == int(task.authorName):
                author = member
        os.chdir(self.profileDir)
        with open(f"{author.name}.json", "r+") as file:
            data = json.load(file)
            encoded = f'{task.encoding}'
            pprint(data)
            active = data["Active tasks"]
            completed = data["Completed tasks"]
            active.remove(encoded)
            completed.append(encoded)
            data["Completed tasks"] = completed
            data["Active tasks"] = active
            pprint(data)
            file.seek(0)
            file.write('')
            json.dump(data, file)
            file.truncate()
            task.changeStatus(TaskCommands.taskStatus.COMPLETE)
            self.tasksGlobal.remove(task)
            os.chdir(self.dir)
            return

    async def completeTask(self, task, message=True):
        if message:
            originTime = task.origin
            sleep = True
            now = getDateTime()
            timepassed = now-originTime
            if timepassed.total_seconds() > task.time:
                sleep = False
            if sleep:
                task.time = task.time-timepassed.total_seconds()
                print(f'Task added waiting {task.time} seconds')
                await asyncio.sleep(task.time)
            await self.sendTaskMention(task)
        self.moveTask(task)
        print(f"Done with {task.name}")

    def waitOnTask(self, task, loop):
        asyncio.run_coroutine_threadsafe(self.completeTask(task), loop)

    def createLoop(self, task):
        # waitOnTask(task)
        _thread = threading.Thread(
            target=self.waitOnTask, args=(task, asyncio.get_event_loop()))
        _thread.start()

    async def sendTaskMention(self, task):
        guild = None
        for g in self.client.guilds:
            if int(g.id) == int(task.guild):
                guild = g

        channel = None
        for c in guild.channels:
            if int(c.id) == int(task.channel):
                channel = c

        author = None
        for member in guild.members:
            if int(member.id) == int(task.authorName):
                author = member

        await channel.send(f'Hello {author.mention}, the time on your task "{task.name}" is up')
        print("Mentioned")
        return

    @commands.command()
    async def generate(self, ctx):
        if ctx.message.author.id != 336296609694351361:
            await ctx.send("You cannot do this")
            return
        else:
            # non bot members
            members = [
                member for member in ctx.guild.members if member.bot == False]
            attrs = []
            for member in members:
                attrs.append(TaskCommands.memberAttribute(member))

            for attr in attrs:
                # pprint(attr.getAttributes())
                await ctx.send(f'Generating file for {attr.getAttributes()["Name"]}')
                attr.toJSON()
            await ctx.send("All files created")

    @commands.command()
    async def cleanup(self, ctx):
        if ctx.message.author.id != 336296609694351361:
            await ctx.send("You cannot do this")
            return
        else:
            os.system("rm *.json")
            await self.generate(ctx)

    @commands.command()
    async def addtask(self, ctx, value=None, unit=None, name=None):

        if isinstance(int(value), int) == False or int(value) < 1 or int(value) == None:
            await ctx.send("First argument must be a positive integer")
        try:
            if unit.upper() == "SECOND":
                unit = "seconds"
            elif unit.upper() == "MINUTE":
                unit = "minutes"
            elif unit.upper() == "HOUR":
                unit = "hours"
            elif unit.upper() == "DAY":
                unit = "days"

            # python 3.10
            # match unit.upper():
            #     case "SECONDS":
            #         pass
            #     case "MINUTES":
            #         pass
            #     case "HOURS":
            #         pass
            #     case "DAYS":
            #         pass
            #     case "SECOND":
            #         unit = "seconds"
            #     case "MINUTE":
            #         unit = "minutes"
            #     case "HOUR":
            #         unit = "hours"
            #     case _:
            print(TaskCommands.timeUnit[unit.upper()])  # TODO: fix
        except KeyError:
            await ctx.send(f"Please use {[tu for tu in TaskCommands.timeUnit]} as second argument")

        if name == None:
            await ctx.send("Please name this task")
        # value:unit:name:datetime:authorName:guildID:channelID
        encoded = f"{value}:{TaskCommands.timeUnit[unit.upper()].name}:{name}:{getTimeStamp()}:{ctx.message.author.id}:{ctx.guild.id}:{ctx.channel.id}"
        t = TaskCommands.Task(
            encoded, value, TaskCommands.timeUnit[unit.upper()], name, ctx)
        self.tasksGlobal.append(t)
        os.chdir(self.profileDir)
        with open(f"{ctx.message.author.name}.json", "r+") as file:
            data = json.load(file)
            encode = f'{value}:'
            pprint(data)
            new_active = data["Active tasks"]
            new_active.append(encoded)
            data["Active tasks"] = new_active
            pprint(data)
            file.seek(0)
            file.write('')
            json.dump(data, file)
            file.truncate()
            await ctx.message.reply(f"A task has been created with name: {name}. You will receive a notification when the time comes.")
            os.chdir(self.dir)
            self.createLoop(t)


    def findTask(self, actives, completed, name):
        if name != None:
            for task in actives:
                for attr in task.split(":"):
                    if re.search(name, attr):
                        return (attr, "active", task)

            for task in completed:
                for attr in task.split(":"):
                    if re.search(name, attr):
                        return (attr, "completed", task)

        return (name, "not found")

    @commands.command()
    async def canceltask(self, ctx, name):
        os.chdir(self.profileDir)
        filename = f'{ctx.author.name}.json'
        with open(filename, "r+") as file:
            data = json.load(file)
            actives = data["Active tasks"]
            complete = data["Completed tasks"]
            result = self.findTask(actives, complete, name)
        if result[1] == "not found":
            await ctx.message.reply(f'No task with name "{name}" was found')
        elif result[1] == "completed":
            await ctx.message.reply(f'The task with name "{name}" has already been completed')
        elif result[1] == "active":
            await ctx.message.reply(f'Task found.')
            name = result[2].split(":")[2]
            dummy = TaskCommands.Task(
                f"1:unit:name:{getTimeStamp()}:authorName:guildID:channelID")
            t = dummy.fromName(name)
            await self.completeTask(t, False)
            await ctx.message.reply(f'Task cancelled.')
            os.chdir(dir)

    def buildStatus(self, status):
        if status[1].upper() == "ACTIVE":
            color = discord.Colour.green()
        else:
            color = discord.Colour.blue()
        embed = discord.Embed(
            color=color,
            title=status[0]
        )

        dummy = TaskCommands.Task(
            f"1:unit:name:{getTimeStamp()}:authorName:guildID:channelID")
        try:
            time = dummy.fromName(status[0]).getTime()
            if time < 0:
                time = 0
        except:
            time = 0
        embed.add_field(name='STATUS', value=status[1].upper(), inline=False)
        embed.add_field(name='TIME LEFT',
                        value=f'{int(time)} seconds', inline=False)
        return embed

    @commands.command()
    async def taskstatus(self, ctx, name=None, all=False):
        os.chdir(self.profileDir)
        filename = f'{ctx.author.name}.json'
        with open(filename, "r+") as file:
            data = json.load(file)
            actives = data["Active tasks"]
            complete = data["Completed tasks"]
            result = self.findTask(actives, complete, name)
            if result[1] == "not found":
                await ctx.send(f"Your tasks are:")
                await ctx.send(f'ACTIVE: {[name.split(":")[2] for name in [code for code in actives]]}')
                await ctx.send(f'COMPLETED: {[name.split(":")[2] for name in [code for code in complete]]}')
            else:
                await ctx.send(embed=self.buildStatus(result))
            os.chdir(self.dir)

    @commands.command()
    async def info(self, ctx):
        try:
            user = ctx.message.mentions[0]
        except IndexError:
            user = ctx.message.author
        os.chdir(self.profileDir)
        filenames = [entry for entry in os.listdir()
                     if re.search(".json", entry)]
        for filename in filenames:
            if filename == f'{user.name}.json':
                with open(filename, "r+") as file:
                    data = json.load(file)
                    embed = discord.Embed(
                        color=discord.Colour.purple(),
                        title='Report'
                    )
                    embed.add_field(
                        name='Name', value=data['Name'], inline=False)
                    embed.add_field(
                        name='Alias', value=data['Nickname'], inline=False)
                    embed.add_field(name='Affiliations',
                                    value=data['Roles'], inline=False)
                    if not data["Active tasks"]:
                        active_value = "[Nothing]"
                    else:
                        active_value = data["Active tasks"]
                    embed.add_field(name='Current jobs',
                                    value=active_value, inline=False)

                    if not data["Completed tasks"]:
                        complete_value = "[Nothing]"
                    else:
                        complete_value = data["Completed tasks"]
                    embed.add_field(name='Finished jobs',
                                    value=complete_value, inline=False)
                    await ctx.send(embed=embed)
                    os.chdir(self.dir)
                    return
        await ctx.send(f"{user.nick} not in system")

    def loadTasks(self, tasks):
        for task in tasks:
            t = TaskCommands.Task(task)
            self.tasksGlobal.append(t)
            # print(t.name)
            self.createLoop(t)

    def loadTaskThreads(self):
        threads = []
        os.chdir(self.profileDir)
        filenames = [entry for entry in os.listdir()
                     if re.search(".json", entry)]
        for filename in filenames:
            with open(filename, "r+") as file:
                data = json.load(file)
                actives = data["Active tasks"]
                t = threading.Thread(self.loadTasks(actives))
                threads.append(t)
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        os.chdir(self.dir)


def setup(client):
    client.add_cog(TaskCommands(client))


if __name__ == '__main__':
    os.system('py main.py')
