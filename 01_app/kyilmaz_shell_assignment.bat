::12. Shell Assignment
:: a) Create the directory "shell_test"
md "shell_test"

:: b) Create the file "test_print.py" with a simple print into the directory
set msg=print("Hello World!")
echo %msg% > "shell_test/test_print.py"

:: c) Rename the file to "new_test_print.py"
ren "shell_test\test_print.py" "new_test_print.py"

:: d) List what is in the directory "shell_test" including their file permissions
dir "shell_test"
icacls "shell_test" /t

:: e) Execute the Python file and call the simple print
python "shell_test/new_test_print.py"

:: f) Remove the directory "shell_test" with its content
rmdir /s /q shell_test 