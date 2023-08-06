import re
import os
import json
import shutil
import colorama
import platform
import unicodedata
from math import ceil
from inspect import stack
from qrcode import QRCode
from typing import Any, List
from time import sleep, time
from mimetypes import guess_type
from send2trash import send2trash
from dataclasses import dataclass, field

from webdriver_manager.chrome import ChromeDriverManager

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import NoSuchElementException

from .message import *
from .error import LoginError


class Whatsapp:

    def _get_qrcode(self, timeout: int, before: int) -> None:

        colorama.init()

        update_qr = ''

        while ((time() - before) < timeout) if timeout else True:
            
            qr_element = self._driver.find_element(By.XPATH, "//canvas/..")

            qr_data = qr_element.get_attribute("data-ref")

            if qr_data and qr_data != update_qr:
                update_qr = qr_data

                os.system("cls||clear")
                qr = QRCode(version=1, border=2)
                qr.add_data(qr_data)
                qr.make()
                qr.print_ascii(invert=True)
                
                print("Scan the QRCode with your phone")

            sleep(1)

    def login(self, visible: bool = False, timeout: int = 0) -> None:
        """Logs in whatsapp and shows the QRCode if necessary

        Args:
            visible (bool, optional): Shows the process. Defaults to False.
            timeout (int, optional): Limit time to login in seconds. Defaults to 0
        """

        os.environ["WDM_LOG_LEVEL"] = "0"

        OS_PATH = {
            "Windows": rf"{os.path.expanduser('~')}/AppData/Local/Google/Chrome/User Data/Default",   # Windows
            "Linux": rf"{os.path.expanduser('~')}/.config/google-chrome/default",                     # Linux
            "Darwin": rf"{os.path.expanduser('~')}/Library/Application Support/Google/Chrome/Default" # Mac OS
        }

        USR_PATH = OS_PATH[platform.system()] 

        if not os.path.exists("data.json"):
            with open("data.json", "w+") as f:
                json.dump({"user_agent": ""}, f)

        with open("data.json", "r") as f:
            data = json.load(f)

        if not data["user_agent"]:

            options = webdriver.ChromeOptions()
            options.add_argument("--hide-scrollbars")
            options.add_argument("--disable-gpu")
            options.add_argument("--log-level=OFF")
            options.add_experimental_option("excludeSwitches", ["enable-logging"])

            driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

            data = {
                "user_agent": driver.execute_script(
                    "return navigator.userAgent"
                )
            }

            with open("data.json", "w") as f:
                json.dump(data, f)

            driver.close()

        caps = DesiredCapabilities.CHROME
        caps['goog:loggingPrefs'] = {'performance': 'ALL'}
        
        options = webdriver.ChromeOptions()
        options.add_argument(f"--user-data-dir={USR_PATH}")
        options.add_argument(f"--user-agent={data['user_agent']}")
        options.add_argument("--start-maximized")
        options.add_argument("--hide-scrollbars")
        options.add_argument("--disable-gpu")
        options.add_argument("--mute-audio")
        options.add_argument("--log-level=OFF")
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        
        if not visible:
            options.add_argument("--headless")

        self._driver = webdriver.Chrome(
            ChromeDriverManager().install(), 
            desired_capabilities=caps,
            options=options
        )
        self._driver.get("https://web.whatsapp.com")

        before = time()
        while ((time() - before) < timeout) if timeout else True:
            try:
                self._driver.find_element(By.ID, "side")
                break
            
            except NoSuchElementException:
                if not visible:
                    try:
                        self._driver.find_element(By.CLASS_NAME, "landing-main")
                        self._get_qrcode(timeout, before)
                        
                    except NoSuchElementException:
                        pass
        else:
            self.close()
            raise LoginError("Failed when trying to log into whatsapp (Took too long to respond)")

        print("Successfully logged in")
        sleep(2)

    def close(self) -> None:
        """Exit whatsapp"""

        self._driver.close()

    def chat(self, name: str) -> None:

        self._Chat._open_chat(self, name)

        info = self._driver.find_element(By.CSS_SELECTOR, "section")
        
        return (
            self.Group(self, name) 
            if info.find_elements(By.CSS_SELECTOR, "span[dir=auto].copyable-text button") 
            else self.Contact(self, name))

    def new_group(self, name: str, contacts: list) -> None:
        number_regex = re.compile(r"^\+?[0-9]{10,15}$")
        
        self._driver.find_element(By.CSS_SELECTOR, "span[data-testid=chat]").click()
        self._driver.find_element(By.CSS_SELECTOR, "div[data-testid=cell-frame-container]").click() 
        sleep(.5)
        
        # Search for the contact
        text_box = self._driver.find_element(By.CSS_SELECTOR, "input")
        
        not_saved = []
        for contact in contacts:
            if number_regex.match(contact):
                not_saved.append(contact)
                continue
            
            text_box.clear()
            text_box.send_keys(contact)
            sleep(.5)
            
            # Verify if the contact exists
            search_box = self._driver.find_element(By.XPATH, "//header/..")
            found = search_box.find_elements(By.CSS_SELECTOR, "[data-testid=cell-frame-container]")
            
            if not len(found):
                raise ValueError(f'Contact not found: "{contact}"')
            
            # Select the contact
            text_box.send_keys(Keys.ENTER) 
            sleep(.5)

        if len(not_saved) == len(contacts):
            raise ValueError("You need to provide at least one added contact")

        self._driver.find_element(By.CSS_SELECTOR, "span[data-testid=arrow-forward]").click()
        self._driver.find_element(By.CSS_SELECTOR, "[role=textbox]").send_keys(name)
        self._driver.find_element(By.CSS_SELECTOR, "span[data-testid=checkmark-medium]").click()
        sleep(1.5)

        # If the person can only be added by invite link
        if self._driver.find_elements(By.CSS_SELECTOR, "div[data-animate-modal-popup=true]"):
            self._driver.find_elements(By.CSS_SELECTOR, "div[role=button]")[1].click()
            sleep(.5)
            self._driver.find_element(By.CSS_SELECTOR, "div[role=button]").click()

        sleep(.5)

        group = self.Group(self, name)

        for contact in not_saved:
            self._driver.get(f"https://web.whatsapp.com/send?phone={contact}&text={group.invite_link}")
            while True:
                try:
                    self._driver.find_element(By.ID, "side")
                    sleep(1)
                    break
                except NoSuchElementException:
                    pass

            text_box = self._driver.find_elements(By.CSS_SELECTOR, "div[role=textbox]")[1]
            text_box.send_keys(Keys.ENTER)
            group._open_chat(group.name)

        return group

    @property
    def me(self) -> Any:
        # TODO: Get all user data and make it editable
        raise NotImplementedError("Not implemented yet")

    @property
    def contact_list(self) -> List[str]:
        """Return a list of your contacts"""

        self._driver.find_element(By.CSS_SELECTOR, "span[data-testid=chat]").click()
        
        scroll = self._driver.find_element(By.XPATH, "//div[@data-testid='contact-list-key']/..")
        contact_list_key = scroll.find_element(By.CSS_SELECTOR, "div[data-testid=contact-list-key] > div > div")
        contact_list_element = contact_list_key.find_elements(By.CSS_SELECTOR, "span[dir=auto]:not(.selectable-text)")

        max_height = int(contact_list_key.get_attribute("scrollHeight"))
        list_size = len(contact_list_element)*int(contact_list_element[0].get_attribute("offsetHeight"))

        contact_list = []
        for _ in range(ceil(max_height/list_size)):

            contact_list_element = contact_list_key.find_elements(By.CSS_SELECTOR, "span[dir=auto]:not(.selectable-text)")
            for contact in contact_list_element:
                contact_list.append(contact.get_attribute("title"))
            
            self._driver.execute_script("""
                arguments[0].scrollBy(0, arguments[1]);
            """, scroll, list_size)
            sleep(.01)

        self._driver.find_element(By.CSS_SELECTOR, "span[data-testid=back]").click()

        return sorted(list(set(contact_list)))

    @property
    def pinned_chats(self) -> List[str]:
        raise NotImplementedError("Not implemented yet")

    @dataclass
    class _Chat:

        _driver: Any = field(repr=False, default=None)

        def _open_chat(self, name: str = None, force=False) -> None:
            """Open a chat

            Args:
                name (str): The name of the chat you want to open
            """

            name = name or self.name

            if not force and len(self._driver.find_elements(By.CSS_SELECTOR, "header")) == 3 and\
                self._driver.find_elements(By.CSS_SELECTOR, f"span[title='{name}']"):
                return

            number_regex = re.compile(
                r"\(?\+[0-9]{1,3}\)? ?-?[0-9]{1,3} ?-?[0-9]{3,5} ?-?[0-9]{4}( ?-?[0-9]{3})? ?(\w{1,10}\s?\d{1,6})?")
            if number_regex.match(name):
                for char in [" ", "-", "(", ")"]:
                    name = name.replace(char, "")
                
                self._driver.get(f"https://web.whatsapp.com/send?phone={name}")
                while True:
                    try:
                        self._driver.find_element(By.ID, "side")
                        sleep(1)
                        break
                    except NoSuchElementException:
                        pass
            else:
                self._driver.find_element(By.CSS_SELECTOR, "#side div[role=textbox]").send_keys(name + Keys.ENTER)
                
            self._driver.find_element(By.CSS_SELECTOR, "#main > header > div").click()

            section = self._driver.find_element(By.CSS_SELECTOR, "section")
            if len(section.find_elements(By.CSS_SELECTOR, "button[type=button]")) > 1:
                section.find_elements(By.CSS_SELECTOR, "button[type=button]")[1].click()
            sleep(1.5)

        def send(self, message: str = "", file: str = "") -> None:
            """Sends a message

            Args:
                message (str): The message you want to send
                file (str): The path of the file you want to send
            """

            # For letters outside english alphabet (most likely in latin based languages)
            def normalize(string):
                return ''.join(
                    char for char in unicodedata.normalize('NFD', string)
                    if unicodedata.category(char) != 'Mn'
                )

            def send_message(message: str, text_box: Any) -> None:

                # Mentioning
                message = re.sub(
                    rf"\<(@.+?)\>",
                    lambda matchobj: normalize(matchobj.group(1)) + Keys.ENTER,
                    message
                )
                
                if "\n" in message:
                    for line in message.split("\n"):
                        text_box.send_keys(line)
                        text_box.send_keys(Keys.SHIFT + Keys.ENTER)
                else:
                    text_box.send_keys(message)

            self._open_chat()

            text_box = self._driver.find_elements(By.CSS_SELECTOR, "div[role=textbox]")[-1]
            
            if file:
                if os.path.isfile(file) or os.path.isdir(file):
                    file = os.path.abspath(file)
                    file_name = os.path.basename(file)
                    file_type = "document"

                    if (
                        "image" in guess_type(file)[0] or
                        guess_type(file)[0] in ["video/mp4", "video/3gpp", "video/quicktime"]
                    ):
                        file_type = "image"
                        
                    elif os.path.isdir(file):
                        shutil.make_archive(file_name, "zip", file_name)
                        file = os.path.abspath(file_name + ".zip")

                    self._driver.find_element(By.CSS_SELECTOR, "span[data-testid=clip]").click()
                    attach = self._driver.find_element(By.XPATH, f"//span[@data-testid='attach-{file_type}']/../input")
                    attach.send_keys(file)
                    sleep(.5)

                    while True:
                        if send_btn := self._driver.find_elements(By.CSS_SELECTOR, "span[data-testid=send]"):
                            send_btn = send_btn[0]
                            if file_type == "image":
                                text_box = self._driver.find_element(By.CSS_SELECTOR, "div[role=textbox]")
                                send_message(message, text_box)
                                send_btn.click()
                                return
                            else:
                                send_btn.click()
                                break

                    if ".zip" in file:
                        send2trash(file)
                else:
                    raise FileNotFoundError(f"File {file} not found")
                
            send_message(message, text_box)
            text_box.send_keys(Keys.ENTER)

        @property
        def last_message(self) -> Any:
            """Gets the last message from the chat

            Returns:
                Class: Last message
            """

            self._open_chat()

            message = self._driver.find_elements(By.CLASS_NAME, "message-in")[-1]
            type = "Text"

            # Audio
            if message.find_elements(By.CSS_SELECTOR, "span[data-testid=audio-play]"):
                type = "Audio"
                # Recorded audio
                if message.find_elements(By.CSS_SELECTOR, "span[data-testid=audio-file]"):
                    type = "AudioFile"

            # Video
            elif message.find_elements(By.CSS_SELECTOR, "span[data-testid=media-play]"):
                type = "Video"

            # Live Location
            elif message.find_elements(By.CSS_SELECTOR, "span[data-testid=live-location-android]"):
                type = "LiveLocation"

            # Location
            elif (
                message.find_elements(By.TAG_NAME, "a") and
                "maps.google.com" in message.find_element(By.TAG_NAME, "a").get_attribute("href")
            ):
                type = "Location"

            # Contacts
            elif len(message.find_elements(By.CSS_SELECTOR, "div[role=button]")) == 4:
                type = "ContactCard"

            # Image
            elif imgs := len(message.find_elements(By.CSS_SELECTOR, "img")):
                type = "Image"
                # Sticker
                if imgs == 1:
                    type = "Sticker"

            # Documents
            elif message.find_elements(By.CSS_SELECTOR, "span[data-testid=type]"):
                type = "Document"

            if type == "AudioFile":
                return Audio(_chat=self, _element=message, isrecorded=True)
            
            return eval(type)(_chat=self, _element=message)

    @dataclass
    class Contact(_Chat):

        name: str = ""
        number: str = ""
        about: str = ""
        profile_picture: str = None

        def __init__(self, parent, name) -> None:
            """Initialize a contact"""

            self._driver = parent._driver
            self._open_chat(name)

            info = self._driver.find_element(By.CSS_SELECTOR, "section")

            while True:
                contact_info = info.find_elements(By.CSS_SELECTOR, "span[dir=auto].copyable-text")

                # Wait until it loads
                if len(contact_info) > 2:
                    break
            
            self.name = contact_info[0].text
            self.number = contact_info[1].text
            self.about = contact_info[2].get_property("title")

            img_section = self._driver.find_element(By.CSS_SELECTOR, "section > div")
            if img_element := img_section.find_elements(By.CSS_SELECTOR, "img"):
                self.profile_picture = img_element[0].get_attribute("src")

            number_regex = re.compile(r"^\+?[0-9]{10,15}$")
            if number_regex.match(self.name):
                self.name, self.number = (
                    self.number.replace("~", ""), 
                    self.name
                )

        def __setattr__(self, __name: str, __value: Any) -> None:

            if stack()[1][3] == "__init__":
                return super().__setattr__(__name, __value)

            raise AttributeError("You cant edit a contact")

    @dataclass
    class Group(_Chat):

        name: str = ""
        description: str = ""
        profile_picture: str = None
        invite_link: str = None
        admin: bool = False
        participants: List[str] = field(default_factory=list)
        _left: bool = field(repr=False, default=False)

        def __init__(self, parent, name) -> None:
            """Initializes a group"""

            self._driver = parent._driver
            self._open_chat(name)
            
            info = self._driver.find_element(By.CSS_SELECTOR, "section")

            # to prevent some bugs
            self._driver.find_element(By.CSS_SELECTOR, "span[data-testid=x]").click()
            sleep(.5)
            self._open_chat(name, force=True)
            info = self._driver.find_element(By.CSS_SELECTOR, "section")
            sleep(.5)

            self.name = info.find_element(By.CSS_SELECTOR, "div[role=textbox]").text
            self.description = info.find_elements(By.CSS_SELECTOR, "span[dir=auto].copyable-text")[1].text

            img_section = self._driver.find_element(By.CSS_SELECTOR, "section > div")
            if img_element := img_section.find_elements(By.CSS_SELECTOR, "img"):
                self.profile_picture = img_element[0].get_attribute("src")
            sleep(.5)

            while True:
                name = info.find_elements(By.CSS_SELECTOR, "div[role=gridcell]")

                # Wait until it loads
                if len(name):
                    break
                
            self.admin = "\n" in name[-2].text

            participants_element = self._driver.find_elements(By.CSS_SELECTOR, "section > div")[-2]
            contact_list = []

            if btn_more := participants_element.find_elements(By.CSS_SELECTOR, "button"):
                actions = ActionChains(self._driver)
                actions.move_to_element(btn_more[0])
                actions.click(btn_more[0])
                actions.perform()

                scroll = self._driver.find_element(By.XPATH, "//header/../div[2]")
                contact_list_key = scroll.find_element(By.CSS_SELECTOR, "div > div > div")
                contact_list_element = contact_list_key.find_elements(By.CSS_SELECTOR, "span[dir=auto]:not(.selectable-text)")

                max_height = int(contact_list_key.get_attribute("scrollHeight"))
                list_size = len(contact_list_element)*int(contact_list_element[0].get_attribute("offsetHeight"))

                for _ in range(ceil(max_height/list_size)):

                    contact_list_element = contact_list_key.find_elements(By.CSS_SELECTOR, "span[dir=auto]:not(.selectable-text)")
                    for contact in contact_list_element:
                        if len(contact.get_attribute("class").split(" ")) > 1:
                            contact_list.append(contact.get_attribute("title"))
                    
                    self._driver.execute_script("""
                        arguments[0].scrollBy(0, arguments[1]);
                    """, scroll, list_size)

                    sleep(.01)

                self._driver.find_element(By.CSS_SELECTOR, "span[data-testid=x]").click()

                self.participants = sorted(list(set(contact_list)))
            else:
                for contact in participants_element.find_elements(By.CSS_SELECTOR, "span[dir=auto]:not(.selectable-text)"):
                    if len(contact.get_attribute("class").split(" ")) > 1:
                        contact_list.append(contact.get_attribute("title"))

                self.participants = sorted(list(set(contact_list)))

            self._driver.execute_script("arguments[0].scrollTop = 0;", info.find_element(By.XPATH, ".."))

            if self.admin:
                self._driver.find_elements(By.CSS_SELECTOR, "div[data-testid=cell-frame-container]")[1].click()
                sleep(.5)
                self.invite_link = self._driver.find_element(By.CSS_SELECTOR, "#group-invite-link-anchor").text
                
                self._driver.find_element(By.CSS_SELECTOR, "span[data-testid=back]").click()
                sleep(1)

        def __setattr__(self, __name: str, __value: Any) -> None:

            if stack()[1][3] == "__init__":
                return super().__setattr__(__name, __value)
            
            self._open_chat()

            info = self._driver.find_element(By.CSS_SELECTOR, "section")
            edit_btns = info.find_elements(By.XPATH, "//span[@data-testid='pencil']/..")

            if not edit_btns:
                raise PermissionError("You don't have permission to edit this group")

            sleep(.5)
            match __name:
                
                case "name":
                    edit_btns[0].find_element(By.XPATH, "../..").click()
                    edit_btns[0].click()

                    edit_name = info.find_element(By.CSS_SELECTOR, "div[role=textbox]")
                    edit_name.clear()
                    edit_name.send_keys(__value + Keys.ENTER)

                case "description":
                    edit_btns[1].find_element(By.XPATH, "../..").click()
                    edit_btns[1].click()

                    edit_description = info.find_elements(By.CSS_SELECTOR, "div[role=textbox]")[1]
                    edit_description.clear()
                    
                    if "\n" in __value:
                        for line in __value.split("\n"):
                            edit_description.send_keys(line)
                            edit_description.send_keys(Keys.SHIFT + Keys.ENTER)
                    else:
                        edit_description.send_keys(__value)

                    edit_description.send_keys(Keys.ENTER)

                case "profile_picture":
                    info.find_element(By.CSS_SELECTOR, "input[type=file]").send_keys(__value)
                    self._driver.find_element(By.CSS_SELECTOR, "div[data-animate-modal-popup=true] div[role=button]").click()

                    img_section = self._driver.find_element(By.CSS_SELECTOR, "section > div")
                    if img_element := img_section.find_elements(By.CSS_SELECTOR, "img"):
                        return super().__setattr__(__name, img_element[0].get_attribute("src"))

                case _:
                    raise AttributeError(f"{__name} is not a valid attribute")
                
            return super().__setattr__(__name, __value)

        def _participant_options(self, contacts, function) -> None:
            """Local function to go to the participants options and execute a function"""
            
            self._open_chat()

            if self._left:
                raise PermissionError("You have left the group")
            
            # Verify if you are admin
            if not self.admin:
                raise PermissionError("You are not a group admin!")

            for contact in contacts:
                # Click on the search icon
                self._driver.find_element(By.CSS_SELECTOR, "span[data-testid=search]").click()

                # Search for the contact
                text_box = self._driver.find_element(By.CSS_SELECTOR, "[role=textbox]")
                text_box.clear()
                text_box.send_keys(contact)
                sleep(.3)

                # Verify if the contact exists
                search_box = self._driver.find_element(By.XPATH, "//header/..")
                contacts_found = search_box.find_elements(By.CSS_SELECTOR, "div[data-testid=cell-frame-container]")
                
                if not len(contacts_found):
                    raise ValueError(f'Contact not found: "{contact}"')

                # Verify if the contact is an admin
                contact_name = search_box.find_element(By.CSS_SELECTOR, "div[role=gridcell]")
                contact_admin = "\n" in contact_name.text

                contacts_found[-1].click()
                options = self._driver.find_elements(By.CSS_SELECTOR, "li > div:nth-child(1)")
                sleep(.5)
                
                function(options, contact, contact_admin)

            self._driver.find_element(By.CSS_SELECTOR, "span[data-testid=x]").click()

        def add(self, contacts: List[str]) -> None:
            """Adds new participants to the group

            Args:
                contacts (list): A list of contacts that you want to add to the group
            """
            number_regex = re.compile(r"^\+?[0-9]{10,15}$")

            self._open_chat()

            if self._left:
                raise PermissionError("You have left the group")

            # Verify if you are admin
            if not self.admin:
                raise PermissionError("You are not a group admin!")

            # Click to add a participant
            self._driver.find_element(By.CSS_SELECTOR, "[data-testid=cell-frame-container]").click() 
            
            # Search for the contact
            text_box = self._driver.find_element(By.CSS_SELECTOR, "[role=textbox]")
            
            not_saved = []
            for contact in contacts:
                if number_regex.match(contact):
                    not_saved.append(contact)
                    continue
                
                text_box.clear()
                text_box.send_keys(contact)
                sleep(.5)
                
                # Verify if the contact exists
                search_box = self._driver.find_element(By.XPATH, "//header/..")
                found = search_box.find_elements(By.CSS_SELECTOR, "[data-testid=cell-frame-container]")
                
                if not len(found):
                    raise ValueError(f'Contact not found: "{contact}"')
                
                # Select the contact
                text_box.send_keys(Keys.ENTER) 
                sleep(.5)

            for contact in not_saved:
                self._driver.get(f"https://web.whatsapp.com/send?phone={contact}&text={self.invite_link}")
                while True:
                    try:
                        self._driver.find_element(By.ID, "side")
                        sleep(1)
                        break
                    except NoSuchElementException:
                        pass

                text_box = self._driver.find_elements(By.CSS_SELECTOR, "div[role=textbox]")[1]
                text_box.send_keys(Keys.ENTER)
                self._open_chat()

            # Click to add them
            self._driver.find_element(By.CSS_SELECTOR, "span[data-testid=checkmark-medium]").click()
            
            # Confirm the addition
            self._driver.find_elements(By.CSS_SELECTOR, "div[role=button]")[1].click()
            sleep(1.5)

            # If the person can only be added by invite link
            if self._driver.find_elements(By.CSS_SELECTOR, "div[data-animate-modal-popup=true]"):
                self._driver.find_elements(By.CSS_SELECTOR, "div[role=button]")[1].click()
                sleep(.5)
                self._driver.find_element(By.CSS_SELECTOR, "div[role=button]").click()

            sleep(.5)

        def remove(self, contacts: List[str]) -> None:
            """Removes participants from the group

            Args:
                contacts (list): A list of contacts that you want to remove from the group
            """

            def _remove(options, contact, contact_admin) -> None:
                
                # NOTE: In python, 0 == False and 1 == True, 
                # so, if the user is admin it will click on the first option
                # else, it will click on the second option (because of the "not" operator)
                options[not contact_admin].click()

            self._participant_options(contacts, _remove)

        def promote(self, contacts: List[str]) -> None:
            """Promotes participants to admin

            Args:
                contacts (list): A list of contacts that you want to promote to admin
            """
            
            def _promote(options, contact, contact_admin) -> None:
                if not contact_admin:
                    options[0].click()
                else:
                    raise ValueError(f'"{contact}" is already an admin!')

            self._participant_options(contacts, _promote)

        def demote(self, contacts: List[str]) -> None:
            """Demotes participants to member

            Args:
                contact (str): The contact that you want to demote to member
            """
            
            def _demote(options, contact, contact_admin) -> None:
                if contact_admin:
                    options[1].click()
                else:
                    raise ValueError(f'"{contact}" is not an admin!')

            self._participant_options(contacts, _demote)

        def leave(self) -> None:
            """Leaves the group"""

            if self._left:
                raise PermissionError("You have already left the group")
            
            info = self._driver.find_element(By.CSS_SELECTOR, "section")
            info.find_elements(By.CSS_SELECTOR, "div[role=button]")[-2].click()
            popup = self._driver.find_element(By.CSS_SELECTOR, "div[data-animate-modal-popup='true']")
            popup.find_elements(By.CSS_SELECTOR, "div[role=button]")[1].click()

            self._left = True
