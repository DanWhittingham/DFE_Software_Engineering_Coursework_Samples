'''
Demonstration of loops and file handling with functions and dictionaries
Allow users to log in, manage users and view or assign tasks
Additional privileges for the admin user
'''


#==== importing libraries ==========
import datetime
import os

#==== Login functions =======
# get_creds - read the available credentials
def get_creds(cred_file):
    # Obtain credentials, store as dictionary (key = user, value = password)
    cred_dict = {}
    with open(cred_file, "r") as creds:
        for line in creds:
            curr_cred = line.split(", ")    # Standard delimeter
            # Skip any strange lines:
            if len(curr_cred) != 2:
                continue
            # Sanitise the user string in case of manual edits to source file
            user = curr_cred[0].strip().lower()          
            # Skip any duplicate users:
            if user in cred_dict:
                print(f"\nWarning: duplicate user {user}, kept first one")
                continue
            # Otherwise, go ahead to add the credentials
            # Username is key and password is value
            cred_dict[user] = curr_cred[1].strip()

    # Make sure we have some users      
    if len(cred_dict) == 0:
        print("\nNo valid users exist, exiting")
        exit()
    return cred_dict


# get_tasks - read the available tasks
def get_tasks(task_file):
    all_tasks = []
    with open(task_file, "r") as tasks:
        for line in tasks:
            curr_task = line.strip().split(", ")  # Standard task delimiter
            if len(curr_task) != 6:
                continue    # Skip any bad tasks; must have six entries
            #TODO: Turn the elements into sensible datatypes
            all_tasks.append(curr_task) 
    return all_tasks


# user_login - log a user in and return the active user
def user_login(credentials):
    while True:
        input_user = input("\nPlease enter your username: ")
        input_user = input_user.strip().lower()
        input_pass = input("\nPlease enter your password: ")
        input_pass = input_pass.strip()

        # Now see if user inputs are valid credentials
        if credentials.get(input_user) == input_pass:
            break  # Allow the valid user to proceed to the menu
        else:
            print("\nNot recognised")  # User or password not found
    return input_user
        

#==== Main menu action functions ======
# reg_user - for registering a user
def reg_user(credentials, cred_file, active_user, **args):

    if active_user != "admin":
        print("\nThis selection is reserved for administrators.")
        return
        
    # Obtain username, make sure it's available, valid & non-empty:
    while True:
        new_user = input("\nPlease enter a new username with no , or \: ")
        new_user = new_user.strip().lower()
        if new_user == "":
            print("\nUsername must not be empty.")

        elif "\\" in new_user or "," in new_user:
            print("\nUsername may not contain , or \, please try again")

        elif new_user in credentials:
            print("\nUsername already registered. Returning to menu, try login or use a different name.")
            break
        
        else:
            print("\nUsername available.")
            # We have a valid username; obtain, check & confirm password:
            while True:
                print("\nPasswords are case sensitive with no , or \\")
                new_pass = input("\nEnter the new user's password: ")
                new_pass = new_pass.strip()

                if new_pass == "":
                    print("\nPassword must not be empty.")

                elif "\\" in new_pass or "," in new_pass:
                    print("\nPassword can't contain , or \, try again")

                elif new_pass == input("\nConfirm password: ").strip():
                    # We now have new user's credentials so register them:
                    with open(cred_file, "a") as cred:
                        cred.write(f"\n{new_user}, {new_pass}")
                        print(f"\nNew user {new_user} registered.")
                    # Add the new user to the in-use store of credentials
                    credentials[new_user] = new_pass
                    break
                else:
                    print("\nPasswords did not match, try again.")
            break


# add_task - for adding a task to the task file
def add_task(credentials, task_list, task_file, **args):
## Tasks are: [user, title, details, date added, due date, status]
    new_task = [""]*6
    new_task[0] = input("\nEnter the username to assign a task to: ")
    new_task[0] = new_task[0].strip().lower()
    if new_task[0] in credentials:
        # We will only take the rest of the task if the user exists
        new_task[1] = input("\nEnter the task title with no , or \\: ")
        new_task[1] = new_task[1].strip().replace(",", "").replace(
            "\\", "")
        new_task[2] = input("\nEnter the task details with no , or \\: ")
        new_task[2] = new_task[2].strip().replace(",", "").replace(
            "\\", "")
        date_today = datetime.date.today()
        new_task[3] = date_today.strftime("%d %b %Y")
        new_task[4] = obtain_date()
        new_task[5] = "No"

        # We have the entire task, so write to the file on a new line
        new_task_string = ", ".join(new_task)
        task_list.append(new_task)
        with open(task_file, "a") as all_tasks:
            all_tasks.write("\n" + new_task_string)
        print("Task successfully added as follows:")
        display_valid_task(new_task, len(task_list)-1)


    else:
        print("\nInvalid user, returning to menu; try registering them.")
       

# view_all - for displaying all tasks
def view_all(task_list, **args):
    i = 0
    # Obtain tasks and display in turn
    for task in task_list:
        display_valid_task(task, i)
        i += 1
    print(f"\nNumber of tasks found: {len(task_list)}")


# view_mine - for displaying and editing user's tasks
def view_mine(active_user, credentials, task_list, task_file, **args):
    # Obtain tasks and display in turn
    n_user_tasks = 0
    i = 0
    for task in task_list:
        if task[0] == active_user:
            # Only display tasks for the current user
            n_user_tasks += 1
            display_valid_task(task, i)
        i +=1
    print(f"\nNumber of tasks assigned to you: {n_user_tasks}")
    task_edited = False
    while n_user_tasks > 0:
        task_id = int(input(
            "\nEnter the ID of the task you wish to edit, or -1 to finish: "
        ))
        if task_id == -1:  ## Finished editing tasks
            break
        elif task_list[task_id][0] == active_user:  # Only edit own tasks
            task_to_edit = task_list[task_id]
            while True:
                print(f'''\nEditing task {task_id}. The following actions are available:
f - Finish editing this task
d - Task due date
o - Task owner
s - Task status
''')
                task_choice = input("Please enter your selection: ").strip().lower()
                if task_choice == "f":  # Finished editing this task
                    print("\nThe task is now defined as follows:")
                    display_valid_task(task_to_edit, task_id)
                    break
                
                task_action = task_actions.get(task_choice)  # Get the function for the user choice

                if task_action == None:
                    print("\nUnrecognised selection, please try again")

                else:  # Process the user action, and record whether any edits were made
                    task_edited = task_action(
                        task_to_edit = task_to_edit,
                        task_edited = task_edited,
                        credentials = credentials,
                        active_user = active_user
                        )

        else:
            print("\nThat is not your task. Choose another or contact admin.")

    # If any tasks were altered, we must update task_file.txt
    if task_edited:
        with open(task_file, "w") as all_tasks:
            all_tasks.write("")
        with open(task_file, "a") as all_tasks:
            for task in task_list:
                all_tasks.write("\n" + ", ".join(task))


# display_stats - show statistics, by printing from text file
def display_stats(credentials, task_list, active_user, **args):
    if active_user != "admin":  # restrict to admin
        print("\nThis selection is reserved for administrators.")
        return

    files_present = os.path.isfile("task_overview.txt") and os.path.isfile("user_overview.txt")

    # If either file is missing, generate them
    if files_present == False:
        generate_reports(credentials, task_list, active_user)
    
    # See if user wishes to refresh the files before displaying
    else:
        print("\nEnter 'y' to refresh the stats, or anything else to continue")
        refresh = input("Refresh? ").strip().lower()
        if refresh == "y":
            generate_reports(credentials, task_list, active_user)
    
    # Display task_overview
    with open("task_overview.txt", "r") as task_overview:
        for line in task_overview:
            print(line.strip())

    # Display user_overview
    with open("user_overview.txt", "r") as user_overview:
        for line in user_overview:
            print(line.strip())


# generate_reports - create the report files task_overview and user_overview
def generate_reports(credentials, task_list, active_user, **args):
    if active_user != "admin":  # restrict to admin
        print("\nThis selection is reserved for administrators.")
        return

    # Data for task_overview
    ## Total number of tasks
    n_tasks = len(task_list)
    n_complete = 0
    n_overdue = 0  # overdue: incomplete AND due date has passed

    # Store the users who we find have tasks
    user_task_data = {}

    # Count complete tasks, count overdue tasks (which are incomplete tasks)
    for task in task_list:
        task_user = task[0]
        if task_user not in user_task_data:  # First task found for this user
            user_task_data[task_user] = [1, 0, 0]  # Total assigned, total complete, total overdue
        else:
            user_task_data[task_user][0] += 1  # Add a task to this user's task data

        # Check if task is complete
        if task[5] == "Yes":
            n_complete += 1
            user_task_data[task_user][1] += 1  # Number of complete tasks for the user

        # Check if task is overdue (i.e. due date is in the past)
        elif datetime.datetime.strptime(task[4], "%d %b %Y").date() < datetime.date.today():
            n_overdue += 1
            user_task_data[task_user][2] += 1  # Number of overdue tasks for the user

    n_incomplete = n_tasks - n_complete

    # Create the task_overview.txt report file
    with open ("task_overview.txt", "w") as task_overview:
        task_overview.write(f'''{"="*70}
Total task count:       {n_tasks}
Total tasks completed:  {n_complete}
Total tasks incomplete: {n_incomplete}
Total tasks overdue:    {n_overdue}
% tasks incomplete:     {(100 * n_incomplete / n_tasks):.2f}
% tasks overdue:        {(100 * n_overdue / n_tasks):.2f}
{"="*70}''')

    # Create the user_overview.txt report file
    with open ("user_overview.txt", "w") as user_overview:
        for user in credentials:
            if user in user_task_data:  # Case for user who had some tasks assigned
                user_task_count = user_task_data[user][0]
                user_task_complete = user_task_data[user][1]
                user_task_overdue = user_task_data[user][2]
                user_overview.write(f'''{"="*70}
User:                   {user}
User task count:        {user_task_count}
% owned of all tasks:   {(100 * user_task_count / n_tasks):.2f}
% own tasks complete:   {(100 * user_task_complete / user_task_count):.2f}
% own tasks incomplete: {(100 * (user_task_count - user_task_complete) / user_task_count):.2f}
% own tasks overdue:    {(100 * user_task_overdue / user_task_count):.2f}
{"="*70}
''')

            else:  # Case for users who had no tasks assigned
                user_overview.write(f'''{"="*70}
User:                   {user}
User task count:        {user_task_count}
% owned of all tasks:   0
% own tasks complete:   100
% own tasks incomplete: 0
% own tasks overdue:    0
{"="*70}
''')


# ==== Task editing actions ====   
# Edit task due date                 
def edit_due_date(task_to_edit, task_edited, **args):
    if task_to_edit[5] != "No":
        print("\nCan't edit completed task. Choose status to reopen it")
        return task_edited

    new_date = obtain_date()
    if new_date == task_to_edit[4]:
        print("\nThat is the existing due date.")  # Nothing changed

    else:
        task_edited = True
        task_to_edit[4] = new_date
    return task_edited

# Edit task owner
def edit_owner(task_to_edit, task_edited, credentials, active_user):
    if task_to_edit[5] != "No":
        print("\nCan't edit completed task. Choose status to reopen it")
        return task_edited

    new_owner = input("\nEnter the new task owner: ")
    new_owner = new_owner.strip().lower()
    if new_owner == task_to_edit[0]:
        print("\nThat is the existing owner.")  # Nothing changed
    elif new_owner in credentials:
        task_edited = True
        task_to_edit[0] = new_owner
        if new_owner != active_user:
            n_user_tasks -= 1
    else:
        print("\nUnrecognised owner")
    return task_edited

# Edit task status
def edit_status(task_to_edit, task_edited, **args):
    status = input("\nIs the task complete? (Y/N): ")
    status = status.strip()
    status = status[0].lower()
    if status == "y":
        if task_to_edit[5] != "Yes":
            task_edited = True
            task_to_edit[5] = "Yes"
            print("\nCompletion set to 'Yes'.")
        else:
            print("\nStatus unchanged.")  # Nothing changed
    elif status == "n":
        if task_to_edit[5] != "No":
            task_edited = True
            task_to_edit[5] = "No"
            print("\nCompletion set to 'No'.")
        else:
            print("\nStatus unchanged.")
    else:
        print("\nUnrecognised status")
    return task_edited

# ==== Other utilities
# display_valid_task: requires a task, as a list of length 6
def display_valid_task(task, id):
    print(f'''
{"="*70}
Task ID:            {id}
Task:               {task[1]}
Assigned to:        {task[0]}
Date assigned:      {task[3]}
Due date:           {task[4]}
Task complete?      {task[5]}
Task description:
    {task[2]}
{"="*70}''')

# obtain and validate input date
def obtain_date():
    while True:
        try:
            date_string = input("\nPlease enter due date in format DD Mmm YYYY: ")
            received_date = datetime.datetime.strptime(date_string, "%d %b %Y").date()
            return received_date.strftime("%d %b %Y")
        except ValueError:
            print("\nIncorrect date format.")


main_actions = {
    "a" : add_task,
    "va" : view_all,
    "vm" : view_mine,
    "r" :  reg_user,
    "ds" : display_stats,
    "gr" : generate_reports
}


task_actions = {
    "d" : edit_due_date,
    "o" : edit_owner,
    "s" : edit_status,
}

    
# ==== Task manager function ======
# This is responsible for loading credentials and tasks
# Then it will guide the user through the menu and call appropriate functions
def task_manager(cred_file, task_file):
    # Obtain credentials and tasks, log the first user in
    credentials = get_creds(cred_file)
    task_list = get_tasks(task_file)
    active_user = user_login(credentials)
    while True:
        # Present the menu to the user and convert user input to lower case.
        print('''\nThe following options are available:
a  - Add a task
va - View all tasks
vm - View my tasks
l  - Return to login
e  - Exit''')
        if active_user == "admin":    # Selections available only to admin
            print("r  - Register a user\nds - Display statistics\ngr - Generate reports")
            
        main_choice = input("Please enter your selection: ").strip().lower()

        if main_choice == 'e':   # User is finished
            print('\nGoodbye!')
            break

        if main_choice == 'l':   # User is switching
            active_user = user_login(credentials)
            continue

        main_op = main_actions.get(main_choice)

        if main_op == None:
            print("\nUnrecognised selection, please try again")
        else:
            main_op(
                credentials = credentials,
                cred_file = cred_file,
                task_list = task_list,
                task_file = task_file,
                active_user = active_user
                )

task_manager("user.txt", "tasks.txt")
