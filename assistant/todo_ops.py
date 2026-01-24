# Importing necessary libraries
import speech_recognition as sr
from assistant.speech import speak
import os

class TODO:
    """
    A simple task manager that handles operations on a todo list stored in a text file.

    Attributes:
        filename (str): The name of the file used to store todo tasks.
    """

    def __init__(self, filename="todo.txt"):
        """
        Initializes the TODO object and ensures the task file exists.

        Args:
            filename (str): The name of the todo file. Default is 'todo.txt'.
        """
        self.filename = filename
        self.file_exist()

    def file_exist(self):
        """
        Checks whether the task file exists.
        If not, it creates an empty file.
        """
        if not os.path.exists(self.filename):
            open(self.filename, "w").close()

    def read_task(self):
        """
        Reads all tasks from the todo file.

        Returns:
            list[str]: A list of all tasks in the file.
        """
        self.file_exist()
        with open(self.filename, "r") as f:
            return [line.strip() for line in f if line.strip()]

    def add_tasks(self, task):
        """
        Appends a new task to the todo file.

        Args:
            task (str): The task description to add.
        """
        with open(self.filename, "a") as f:
            f.write(task + "\n")
        print(f"[ ] {task} : added!")

    def write_tasks(self, to_do):
        """
        Overwrites the todo file with a new list of tasks.

        Args:
            to_do (list[str]): List of tasks to write.
        """
        with open(self.filename, "w") as f:
            for to_dos in to_do:
                f.write(to_dos + "\n")

    def show_tasks(self):
        """
        Displays all current tasks in the todo list.
        """
        todo = self.read_task()

        if not todo:
            print("Your todo list is empty.")
        else:
            print("\nYour current todo list:")
            for i, to_do in enumerate(todo, start=1):
                print(f"{i}. {to_do}")

    def delete_task(self, num):
        """
        Deletes a task by its number in the list.

        Args:
            num (int): Index number of the task to delete.
        """
        todo = self.read_task()

        if num < 1 or num > len(todo):
            print("Invalid task number.")
            return

        removed = todo.pop(num - 1)
        self.write_tasks(todo)

        print(f"Todo: '{removed}' deleted!")

    def clear_all(self):
        """
        Removes all tasks by clearing the todo file.
        """
        open(self.filename, "w").close()
        print("All tasks cleared!")


# Create the Todo Manager object
todo = TODO("todo.txt")

# Create a speech recognizer instance
recognizer = sr.Recognizer()


def todo_voice_handler(command):
    """
    Handles voice commands related to 'todo' actions such as:
    add, delete, show, and clear.

    Workflow:
        - Detect user intent (add/delete/show/clear)
        - Ask follow-up questions
        - Perform the required action via the TODO class

    Args:
        command (str): The initial voice command spoken by the user.
    """

    if "to do" in command.lower() or "todo" in command.lower():
        speak("Do you want to add, delete, show, or clear tasks?")

        # Capture follow-up command for the type of action
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source)

        try:
            action = recognizer.recognize_google(audio).lower()
        except sr.UnknownValueError:
            speak("I couldn't understand. Please say add, delete, show, or clear.")
            return
        except sr.RequestError:
            speak("Speech service is unavailable.")
            return

        # ADD TASK
        if "add" in action:
            speak("What task should I add, sir?")
            with sr.Microphone() as source:
                audio = recognizer.listen(source, duration=0.5)
                task = recognizer.recognize_google(audio)

            todo.add_tasks(task)
            speak(f"Task {task} added.")

        # DELETE TASK
        elif "delete" in action:
            todo.show_tasks()
            speak("Say the number of the task to delete.")

            with sr.Microphone() as source:
                audio = recognizer.listen(source, duration=0.5)
                num = recognizer.recognize_google(audio)

            if num.isdigit():
                todo.delete_task(int(num))
                speak("Task deleted.")
            else:
                speak("I didn’t understand the number.")

        # SHOW TASKS
        elif "show" in action:
            todo.show_tasks()
            speak("These are your current tasks.")

        # CLEAR ALL TASKS
        elif "clear" in action:
            todo.clear_all()
            speak("All tasks cleared.")

    else:
        # speak("I didn’t understand that.")
        return