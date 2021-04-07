# Bio50
#### Video Demo:   https://www.youtube.com/watch?v=xv2zmk2OD8g
#### Description:
Bio50 is a web-based bioinformatics tool in which users can upload .txt files and process files with the provided methods.

__Created by Cem Sağlam for the course CS50.__

## For users
When entering the website, the user is redirected to the log in page.
If the user cannot provide credidentials, they can register for a new account by clicking on the "Register" button on the navigation bar.
After logging in, the user will see an accordion of cards, each showing a body description and sample input/outputs when toggled.
The [KEYWORD] refers to the key of the method. This will be useful when processing the file.
The rest of the title is the full name of the method.
When toggled, the accordion will expand, showing a paragraph of description.
This description will be followed by a sample input and an output with their descriptions.
When clicked on "New File" on the navigation bar, the user can submit their files and their desired method via the submit button.
If anything goes wrong, the website will show an error message. The user then should check if they have any mistakes.
The user should also make sure to use the right format, as specified with the descriptions and samples.

For any questions, feel free to email cemsaglam07@gmail.com or send a message.
Interested developers can ask for a setup documentation and/or tutorial.

## For developers
My Bio50 web project is presented to the users with HTML templates written in HTML and Jinja programming languages.
The Python application called "application.py" formats them to render the desire template, which is ultimately presented to the users via Flask, a micro web framework.
The application.py file also has two helper files, helpers.py and methods.py.
The helpers.py file consists of methods "login_required" and "apology."
The apology function renders the formatted "apology.html" template with its contents adapted to the thrown error message.

Another file is "bio50.db," which is a SQL database file powered by SQLite3.
The SQL database file has three tables: "cards", "users", and "files."
The "cards" table has eight fields. The fields id, scp, title, bodytext, txtgiv, txtin, txtret, txtout refer to the SQLite-assigned unique identifiers, method keywords, full names of the methods, description of the problem set, file input formatting info, sample input for documentation, file output formatting info, and sample output for documentation respectively.
Developers can feel free to implement their own methods as per the formatting.
It is recommended to check the website and SQL database beforehand to format the new methods in the style of the original methods.

The uploads folder is for the server to upload the user input to later process them.
The files are stored in the folder and are not deleted for the developer to check on them later.
However, this may cause memory issues, so the developer is free to dispose of the files.
If this is the case, the developer should NOT delete the "uploads" folder, but should only delete what is inside.
The uploads folder was hard coded in the application.py file; deleting it would cause missing file errors.

Again, this is just a set of recommendations. The developers may as well delete or alter everything as they please, as long as they understand the coding.
For any clarifications, please do not hesitate to email cemsaglam07@gmail.com or send a message
