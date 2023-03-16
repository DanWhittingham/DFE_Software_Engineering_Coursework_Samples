'''
Demonstration of loops and file handling
Create a program for a small business that can help it to manage tasks
assigned to each member of the team. This program will work with two text files,
user.txt and tasks.txt. Allow users to log in, manage users and view or assign tasks.
This is developed further in later tasks.
'''

#=====importing libraries===========
import datetime

#====Login Section====
# Obtain the credentials
users = []
passwords =[]
with open("user.txt", "r") as creds:
    for line in creds:
        curr_cred = line.split(", ")    # Standard delimeter

        # Skip any strange lines:
        if len(curr_cred) != 2:
            print("\nWarning: unecognised user formats found")   
            continue
        curr_cred[0] = curr_cred[0].strip().lower()

        # Skip any duplicate users:
        if curr_cred[0] in users:
            print(f"\nWarning: duplicate user {curr_cred[0]}, kept first one")
            continue

        # Otherwise, go ahead to add the credentials
        users.append(curr_cred[0].strip().lower())
        passwords.append(curr_cred[1].strip())

# Make sure we have some users, set user_index beyond the range
n_users = len(users)
if n_users == 0:
    print("No valid users exist, exiting")
    exit()
user_index = n_users

# Begin user login 
while True:
    active_user = input("\nPlease enter a valid user: ")
    active_user = active_user.strip().lower()
    active_pass = input("\nPlease enter your password: ")
    active_pass = active_pass.strip()

    # Now see if user inputs are valid credentials
    for i in range (0, n_users):
        if active_user == users[i]:
            if active_pass == passwords[i]:
                user_index = i  # We have a valid user
            break
    if user_index < n_users:  # Allow the valid user to proceed to the menu
        break
    else:
        print("\nNot recognised")  # User not found or password doesn't match
        
while True:
    # present the menu to the user and convert user input to lower case.
    menu = input('''\nSelect one of the following options:
r - Register a user
a - Add a task
va - View all tasks
vm - View my tasks
e - Exit
: ''').strip().lower()

    if menu == 'r':    # Registering a user
        # Obtain username, make sure it's available, valid & non-empty:
        while True:
            new_user = input("\nPlease enter a new username with no , or \: ")
            new_user = new_user.strip().lower()
            if new_user == "":
                print("\nUsername must not be empty.")

            elif "\\" in new_user or "," in new_user:
                print("\nUsername may not contain , or \, please try again")

            elif new_user in users:
                print("\nUsername already registered. Returning to menu.")
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
                        with open("user.txt", "a") as creds:
                            creds.write(f"\n{new_user}, {new_pass}")
                            print(f"\nNew user {new_user} registered.")
                        break
                    else:
                        print("\nPasswords did not match, try again.")
                break
        
  
    elif menu == 'a':    # Adding a new task
        # Tasks are: [user, title, details, date added, due date, status]
        new_task = [""]*6
        new_task[0] = input("\nEnter the username to assign a task to: ")
        new_task[0] = new_task[0].strip().lower()
        if new_task[0] in users:
            # We will only take the rest of the task if the user exists
            new_task[1] = input("\nEnter the task title with no , or \\: ")
            new_task[1] = new_task[1].strip().replace(",", "").replace(
                "\\", "")
            new_task[2] = input("\nEnter the task details with no , or \\: ")
            new_task[2] = new_task[2].strip().replace(",", "").replace(
                "\\", "")
            date_today = datetime.date.today()
            month_strs =    ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                            "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
            month_today = month_strs[date_today.month - 1]
            new_task[3] = f"{date_today.day} {month_today} {date_today.year}"
            new_task[4] = input("\nEnter a due date in form DD MMM YYYY: ")
            # Could validate if users frequently give bad date formats
            # The program won't mind so just check for , and \ as usual
            new_task[4] = new_task[4].strip().replace(",", "").replace(
                "\\", "")
            new_task[5] = "No"

            # We have the entire task, so write to the file on a new line
            new_task_string = ", ".join(new_task)
            with open("tasks.txt", "a") as all_tasks:
                all_tasks.write("\n" + new_task_string)
                print(f"\nTask  successfully added:\n{new_task_string}")

        else:
            print("Invalid user, returning to menu; try registering them.")
       

    elif menu == 'va':    # viewing all tasks

        # Obtain tasks and display in turn
        n_valid_tasks = 0
        with open("tasks.txt", "r") as all_tasks:
            for line in all_tasks:
                curr_task = line.split(", ")  # Standard task delimiter
                if len(curr_task) != 6:
                    print(f"\nWarning, unrecognised task format: {curr_task}")
                    continue    # Skip any bad tasks; must have six entries
                n_valid_tasks += 1
                print(f'''
{"-"*70}
Task:               {curr_task[1]}
Assigned to:        {curr_task[0]}
Date assigned:      {curr_task[3]}
Due date:           {curr_task[4]}
Task complete?      {curr_task[5]}
Task description:
    {curr_task[2]}
{"-"*70}''')
        print(f"\nNumber of valid tasks found: {n_valid_tasks}")


    elif menu == 'vm':    # View tasks assigned to active user
        n_user_tasks = 0

        # Obtain tasks and display in turn
        with open("tasks.txt", "r") as all_tasks:
            for line in all_tasks:
                curr_task = line.split(", ")
                if len(curr_task) != 6:
                    print(f"\nWarning, unrecognised task format: {curr_task}")
                    continue    # Skip any bad tasks
                if curr_task[0] == active_user:
                    # Only display tasks for the current user
                    n_user_tasks += 1
                    print(f'''
{"-"*70}
Task:               {curr_task[1]}
Assigned to:        {curr_task[0]}
Date assigned:      {curr_task[3]}
Due date:           {curr_task[4]}
Task complete?      {curr_task[5]}
Task description:
    {curr_task[2]}
{"-"*70}''')
        print(f"\nNumber of valid tasks assigned to you: {n_user_tasks}")

    elif menu == 'e':   # User is finished
        print('\nGoodbye!!!')
        exit()

    else:   # Unrecognised selection
        print("\nYou have made a wrong choice, Please Try again")
