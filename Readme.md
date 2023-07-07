To begin
1, Python must be installed in your system
2, Open this folder in the vscode terminal and so type the command "venv\Scripts\activate", then do this in the terninal -> "python manage.py makemigrations" and also this "python manage.py migrate"
3, enter the command -> "python manage.py runserver" then the port will be displayed
4, Copy and paste the port in 3 in the browser
5, To view the admin page stop the server by using ctrl + c in the terminal
6, use the command "python manage.py createsuperuser" and then follow the prompt and then do number 3 again
7, In your browser navigate to http://127.0.0.1:8000/admin and in the login form use the username you entered and also beware that the password field in the terminal will not show what you are typing