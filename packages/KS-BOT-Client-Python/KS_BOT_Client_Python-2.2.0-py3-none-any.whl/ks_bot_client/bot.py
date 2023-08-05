import socketio
import requests
import time
import threading

from ..ks_bot_client.ks_bot_exceptions import LoggingInError

class Bot:

  def __init__(self, name:str, password:str):
    """
    @param {string} name: Name can either email address, user name, or first name
    @param {string} password: Your password
    """

    self.sio =  socketio.Client()

    self.name = name

    self.password = password

    self.session_id = None


  def log_in(self):
    """
      Logs in your bot to server
    """
    x = requests.post("https://ksbot.kidssmit.com/does_user_exist", json = {
      "name": self.name,
      "password": self.password
    })

    try: 
      if x.json()["returns"] == "User exist":
        self.session_id = x.json()['data']["id"]
        return True
    except Exception as e: pass
  
    return False

  def run(self):
    """
      Starts your bot, to be able to receive and send commands to server
    """
    logged_in = self.log_in()
    
    if logged_in:
      self.sio.on("connect", handler=self.connect)
      self.sio.on("WelcomeMessage", handler=self._event_welcome_message)
      self.sio.on("BotProcessReply", handler=self._event_bot_process_reply)
      self.sio.on("Timer Over", handler=self._event_timer_over)
      self.sio.connect("https://ksbot.kidssmit.com")
      #self.sio.wait()
    else:
      raise LoggingInError("There was a problem login you in")

  def connect(self):
    print("Client Connected")
    self.sio.emit("launch_bot", {"session_id": self.session_id})

  def WelcomeMessage(self, data):
    """
      This event gives you, your previous messages with bot.
    """
    print("KS-BOT said 'welcome'")

  def _event_welcome_message(self, data):
    """
      Runs welcome message event
    """
    threading.Thread(target=self.WelcomeMessage, args=[data]).start() # Runs in thread so it won't disturb main program

  def BotProcessReply(self, data):
    """
      Returns bot reply to the message you sent it
    """
    print("KS-BOT said: ", data)

  def _event_bot_process_reply(self, data):
    threading.Thread(target=self.BotProcessReply, args=[data]).start() # Runs in thread so it won't disturb main program

  def TimerOver(self, data):
    """
      Handles Event Server sends when timer is over
    """

    print("KS-BOT said: Timer is over, Timer: ", data)

  def _event_timer_over(self, data):
    threading.Thread(target=self.TimerOver, args=[data]).start() # Runs in thread so it won't disturb main program

  def send_command(self, command, timeZone=None, log=False):
    """
      Sends command to server and wait for reply
      @param {string} command - Command you would like server to process
      @param {string} timeZone - Defualt is your current timeZone, but it tells server what your timeZone is, you can change
      @param {bool} log - Would you like a print statement to verify message has been sent
    """

    self.sio.emit("process_new_message",  
      {
        "session_id": self.session_id, 
        "new_message": {
          "message":  command,
          "timeZone": timeZone or time.tzname
        }
      }
    )

    if log:
      print("Sent message: ", command)

    