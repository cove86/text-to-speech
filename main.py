from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from polly import Polly
from document_manager import DocumentManager
import os
import subprocess
import sys

polly = Polly()
doc = DocumentManager()

parent = "/"
directory = "Text2Speech"

PATH = os.path.join(parent, directory)


class FileChoosePopup(Popup):
    load = ObjectProperty()


# Main app Screen
class ScreenOne(Screen):
    # Open pop up Screen
    def open_popup(self):
        self.the_popup = FileChoosePopup(load=self.load)
        self.the_popup.open()

    # Load content onto pop up screen
    def load(self, selection):
        self.file_path = str(selection[0])
        self.the_popup.dismiss()
        print(self.file_path)

        # check for non-empty list i.e. file selected
        if self.file_path:
            self.ids.selected_file.text = self.file_path.rsplit("\\", 1)[1]

    # Close pop up screen
    def dismiss(self):
        self.the_popup.dismiss()

    # Convert selected file, calls doc manager method to create text then passes
    # this to polly convert method along with the file name
    def convert(self):
        try:
            if self.file_path:
                if self.file_path.endswith(".pdf"):
                    pdf = doc.pdf_text(self.file_path)
                    polly.convert(pdf, self.ids.selected_file.text)
                elif self.file_path.endswith(".docx"):
                    docx = doc.doc_text(self.file_path)
                    polly.convert(docx, self.ids.selected_file.text)
                elif self.file_path.endswith(".txt"):
                    txt = doc.txt_text(self.file_path)
                    polly.convert(txt, self.ids.selected_file.text)
                self.ids.convert_button.text = "File Converted!"
                self.file_path = polly.output
                self.ids.selected_file.text = self.file_path
            else:
                self.ids.convert_button.text = "File Type must be pdf,docx or text!"
        except AttributeError:
            self.ids.convert_button.text = "File not Selected"

    # Resets label texts
    def reset_text(self):
        self.ids.convert_button.text = "Convert"
        self.ids.play.text = "Play File"


    # Plays selected file if MP3 using default Media Player
    def play(self):
        try:
            if sys.platform == "win32":
                os.startfile(self.file_path)
            else:
                # The following works on macOS and Linux. (Darwin = mac, xdg-open = linux).
                opener = "open" if sys.platform == "darwin" else "xdg-open"
                subprocess.call([opener, self.file_path])
        except (AttributeError, TypeError):
            self.ids.play.text = "File Not Selected"

    def clear(self):
        self.reset_text()
        self.ids.selected_file.text = "Filename"
        self.file_path = None


# Screen to input text and save as file
class ScreenTwo(Screen):
    text = ObjectProperty(None)

    # Takes entered file name and text from inputs and saves as a txt file
    def save_file(self):
        text = self.user_text.text
        file = f"{self.file_name.text}.txt"
        complete = os.path.join(PATH, file)
        with open(complete, "x") as f:
            f.write(text)
        self.user_text.text = f"File saved here: {complete}"


class ScreenMan(ScreenManager):
    pass


KV = Builder.load_file("gui.kv")


class Text2SpeechApp(App):
    def build(self):
        # Create Directory to save text files
        try:
            os.mkdir(PATH)
            print(f"Directory Created: {PATH}")
        except FileExistsError:
            print(f"Directory Exists: {PATH}")
        return KV


if __name__ == "__main__":
    Text2SpeechApp().run()
