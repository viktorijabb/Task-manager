from datetime import date, datetime


def reg_user(ad, usernames):  # function to register user

    # if user  is not admin, display appropriate message and return to menu
    if ad is False:
        print("Only admins can use this menu option!")

    # if user is admin, allow to add a new user
    else:
        while True:
            new_username = input("Enter the username of the new user: ")
            new_password = input("Enter the password of a new user: ")
            # check if user has already been registered
            if new_username in usernames:
                print("This user already exists!")
                continue
            else:
                confirm_password = input("Re-enter the new user's password: ")
                # checks for password confirmation
                if new_password != confirm_password:

                    while True:
                        confirm_password = input("Re-enter the new user's password: ")

                        if new_password == confirm_password:
                            with open("user.txt", "a") as user_append:
                                user_append.write(f"\n{new_username}, {new_password}")
                                print("\nYou have successfully added a new user!\n")
                                return
                else:
                    with open("user.txt", "a") as user_append:
                        user_append.write(f"\n{new_username}, {new_password}")
                        print("\nYou have successfully added a new user!\n")
                        return


def add_task():  # function to add task

    a_username = input("Enter the username of the person you want to assign the task to: ")
    a_title = input("Enter title of task: ")
    a_description = input("Enter a task description: ")
    a_due_date = input("Enter the due date of the task (for example - 19/11/2023): ")
    a_date_today = today()
    a_task_completed = False # task marked as incomplete by default
    a_task_completed = "Yes" if a_task_completed else "No"

    # writes task to the task file
    with open("tasks.txt", "a") as file:
        file.write(
            f"\n{a_username}, "
            f"{a_title}, "
            f"{a_description}, "
            f"{a_due_date}, "
            f"{a_date_today}, "
            f"{a_task_completed}")
        print("You have successfully added a task! ")
        return


def view_all():  # function to view all tasks

    with open("tasks.txt", "r") as file:
        for line in file:
            item = line.split(", ")
            print(f'''
    Task:           {item[1]}
    Assigned to:    {item[0]}
    Date assigned:  {item[4]}
    Due date:       {item[3]}
    Task Complete?  {item[5]}
    Task description:
        {item[2]}\n''')


def view_mine(user):  # function to (1) view user's tasks (2) view specific task (3) mark as complete

    user_list = []

    with open("tasks.txt", "r") as file:  # view user's tasks
        for i, line in enumerate(file, 1):
            item = split_parts(line)
            user_list.append(item[0])
            if user == item[0]:
                print(f'''
{i}
Task:           {item[1]}
Assigned to:    {item[0]}
Date assigned:  {item[4]}
Due date:       {item[3]}
Task Complete?  {item[5]}
Task description:
        {item[2]}\n''')
            else:
                continue

        if user not in user_list:
            print("\nYou have no tasks assigned to you!\n")

    while True:  # look for specific task or return to main menu
        choice = input("Enter the code of a specific  task or \"-1\" to return to the main menu: ")
        if choice == "-1":
            return

        with open("tasks.txt", "r+") as file:
            for i, line in enumerate(file, 1):
                item = split_parts(line)

                if i != int(choice):
                    continue
                print(f'''
{i}
Task:           {item[1]}
Assigned to:    {item[0]}
Date assigned:  {item[4]}
Due date:       {item[3]}
Task Complete?  {item[5]}
Task description:
    {item[2]}\n''')
        # mark task as complete
        complete = input("Would you like to mark the task as complete?(Yes or No): ").lower()
        if complete == "yes":
            line.replace("No", "Yes")
            print("\nYou have marked the task as complete! ")
        # edit task
        else:
            edit = input("Would you like to edit the task?(Yes or No): ").lower()

            if edit == "yes" and item[5] == "No":
                change_user = input("Assign task to user: ")
                change_date = input("Change due date to (example - 19/11/2023): ")

                if change_user in usernames:
                    line.replace(item[0], change_user)
                    line.replace(item[3], change_date)
                else:
                    print("\nThis user does not exist!")


def stats(): # function to show statistics

    users, tasks = gen_reports()
    print(f'''
Total number of users:      {len(users)}
Total number of tasks:      {tasks}
    ''')


def gen_reports(): # function to generate reports

    task_count = 0
    complete_tasks = 0
    incomplete_tasks = 0
    overdue_tasks = 0

    with open("tasks.txt", "r+") as tasks:

        for task in tasks:
            user, title, description, date, due_date, completed = task.strip("\n").split(", ")
            task_count += 1

            # sorts if tasks are completed or incomplete
            if completed == "No":
                incomplete_tasks += 1
            else:
                complete_tasks += 1

            # checks if tasks are overdue
            date_object1 = datetime.strptime(today(), "%d/%m/%Y")
            date_object2 = datetime.strptime(due_date, "%d/%m/%Y")
            if date_object1 > date_object2 and completed == "No":
                overdue_tasks += 1

    # generates task report
    with open("task_overview.txt", "w+") as task_overview:
        task_overview.write(f'''
Tasks generated:    {task_count}
Completed tasks:    {complete_tasks}
Incomplete tasks:   {incomplete_tasks}
Overdue tasks:      {overdue_tasks}
{(incomplete_tasks * 100) / task_count}% of tasks are incomplete
{(overdue_tasks * 100) / task_count}% of tasks are overdue
                ''')


    with open("tasks.txt", "r+") as tasks, open("user.txt", "r+") as users:
        user_list = users.readlines()
        task_list = tasks.readlines()

        for user in user_list:
            username, password = split_parts(user)
            user_task_count = 0
            user_complete_tasks = 0
            user_incomplete_tasks = 0
            user_overdue_tasks = 0

            for task in task_list:
                t_username, title, description, date, due_date, completed = task.strip("\n").split(", ")
                if username == t_username:
                    user_task_count += 1

                    # sorts if tasks are completed or incomplete
                    if completed == "No":
                        user_incomplete_tasks += 1
                    else:
                        user_complete_tasks += 1

                    # checks if tasks are overdue
                    date_object1 = datetime.strptime(today(), "%d/%m/%Y")
                    date_object2 = datetime.strptime(due_date, "%d/%m/%Y")
                    if date_object1 > date_object2 and completed == "No":
                        user_overdue_tasks += 1

            # generates user report
            with open("user_overview.txt", "a") as user_overview:
                user_overview.write(f'''
User:               {username}
Tasks assigned to user:    {user_task_count}
{get_percent(user_task_count, task_count)} % of tasks are assigned to this user
{get_percent(user_complete_tasks,user_task_count)} % of tasks are completed
{get_percent(user_incomplete_tasks,user_task_count)} % of tasks are incomplete
{get_percent(user_overdue_tasks, user_task_count)} % of tasks are overdue
                            ''')
    return user_list, task_count


def today(): # function fetches today's date
    today = date.today()
    return today.strftime("%d/%m/%Y")


def split_parts(line_in_file):  # splits line by comma
    return line_in_file.split(", ")


def get_percent(sample, all_samples):  # calculate % and exception handling for division by zero
    try:
        return (sample * 100) / all_samples
    except ZeroDivisionError:
        return 0


# --- login section ---


usernames = []
passwords = []

with open("user.txt", "r") as username_password:
    for line in username_password:
        line = line.strip("\n").split(", ")
        usernames.append(line[0])
        passwords.append(line[1])

# ---input/user validation---

usr_inp_username = input("Enter your username: ")
usr_inp_password = input("Enter your password: ")

while True:
    if usr_inp_username in usernames:
        if usr_inp_password in passwords:
            print("\nYou have successfully logged in!\n")
            break
        else:
            usr_inp_password = input("Enter a valid password: ")
            continue
    else:
        usr_inp_username = input("Enter a valid username: ")
        continue


# ---checking if user is admin---
admin = usr_inp_username == "admin"
# ---MENU---
# presenting the menu to the user
while True:

    print('''Select one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my task''')

    # if user is admin, show an additional menu option
    if admin:
        print("s - Statistics")
        print("gr - Generate reports")
    print("e - Exit")

    # user selects menu option
    menu = input(": ").lower()

    # ---OPTION r---
    if menu == 'r':
        reg_user(admin, usernames)

    # ---OPTION a---
    elif menu == 'a':
        add_task()

    # ---OPTION va---
    elif menu == 'va':
        view_all()

    # ---OPTION vm---
    elif menu == 'vm':
        view_mine(usr_inp_username)

    # --- OPTION s---
    elif menu == 's' and admin:
        stats()

    # --- OPTION gr---
    elif menu == 'gr' and admin:
        gen_reports()

    # ---OPTION e---
    elif menu == 'e':
        print('Goodbye!!!')
        exit()

    else:  # if invalid option entered, ask to enter again
        print("You have made a wrong choice, Please Try again")
        continue
