# Quickstart Guide: Evolution of Todo Console Application

## Prerequisites
- Python 3.13+ installed
- Basic familiarity with command line interface

## Setup
1. Ensure Python 3.13+ is installed on your system
2. Clone or download the project repository
3. Navigate to the project directory

## Running the Application
1. Open a terminal/command prompt
2. Navigate to the project directory
3. Run the application with the command:
   ```bash
   python src/main.py
   ```

## Using the Application
1. The application will display a menu with numbered options
2. Enter the number corresponding to the action you want to perform
3. Follow the prompts to enter required information
4. The application will display results or error messages as appropriate

### Available Actions:
- **Add Task**: Enter title and optional description
- **View Tasks**: Display all tasks with their status
- **Update Task**: Modify title or description of existing task
- **Delete Task**: Remove a task by ID
- **Toggle Task Status**: Mark task as complete/incomplete
- **Exit**: Quit the application

## Example Workflow
1. Run `python src/main.py`
2. Select option 1 to add a task
3. Enter "Buy groceries" as the title
4. Optionally add a description
5. Select option 2 to view your tasks
6. Continue using other options as needed
7. Select option 6 to exit when finished

## Troubleshooting
- If you get a "command not found" error, ensure Python is in your system PATH
- If the application crashes, check that you're using Python 3.13+
- For invalid input errors, follow the prompts carefully and provide required information

## Notes
- All data is stored in memory only and will be lost when the application exits
- Task IDs are auto-generated and unique per session
- The application handles invalid inputs gracefully with helpful error messages