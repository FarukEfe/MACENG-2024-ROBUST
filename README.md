IMPORTANT
=========
Follow the below steps to get the app running on your device.

# Step 1: Install MySQL Services

First of all, you have to make sure you have MySQL and MySQLWorkbench installed on your computer.

- Download MySQL: https://dev.mysql.com/downloads/
- Download Workbench: https://dev.mysql.com/downloads/workbench/

Make sure to find the right version that fits your operating system.

While you're setting up your MySQL configuration, **take note of your password** and leave the default server as `localhost` and `root`. This information will be needed later.

After installing workbench, create a new connection with the name `loginapp`. Keep the default values `root`, `localhost`, and port `3306`. After creating the connection, make sure you start running it by doing `Right Click -> Start Command Line Client`. When the command line opens you're going to be asked a password, this is the same password you created when setting up MySQL on your computer.

# Step 2: Install Project and Create Virtual Environment

In the next step, fork this project into your github account, and download it to your local computer. After opening up the program, execute `python -m venv .env` in the project root directory to create a virtual environment. You can also use `python3` if you're on that version.

To activate the virtual environment, execute the following command in the project root directory.

**Windows** 

```.env\Scripts\activate```
          
**macOS/Linux**

```. .env/bin/activate```
or
```source .env/bin/activate```

# Step 3: Install Required Modules

I have conveniently created a `requirements.txt` file which lists the name of all the modules needed to run the project. Go ahead and run `pip install -r requirements.txt` in the project root directory **after making sure the virtual environment is activated**. You can also use `pip3` based on your pip version.

# Step 4: Final Changes

Navigate to `app.py` and navigate to the following section:

```
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '*******' #Replace ******* with  your database password.
app.config['MYSQL_DB'] = 'loginapp'
```

And replace the ******* string field with your MySQL password.

# Step 5: Run the app

Finally, we can run our flask app. Execute the following commands for assurance:

```
set FLASK_APP=app
set FLASK_ENV=development
flask run
```

Finally, you can get the localhost link from the command line output and check out the project!

**Here's a demo of the project:**

https://github.com/user-attachments/assets/0509ab1a-5be9-4dff-b6a5-615108954235


