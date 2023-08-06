# KS-BOT-Client-Python

### Python framework for interacting with KS-BOT, without any app
> SIDE NOTE: To use ks-bot-client you will need to create a user account at: [kids smit](https://www.kidssmit.com)
__To get started simply install ks-bot-client, with the following command__
```Python

python -m pip install KS-BOT-Client-Python

```

## After Installation:

- Simple import ks-bot-client

```Python
import ks_bot_client
```

- Next create a custom Bot class by inherenting from ks_bot_client.bot class

```Python

class CustomBot(ks_bot_client.Bot):

  def __init__(self, name:str, password:str):
    """
      :param {string} name - Either Username, First Name of user or email of user
      :param {string} password - User password
    """

    super().__init__(name, password)


  def WelcomeMessage(self, data):
    """
      This event gives you, your previous messages with ks-bot.

      > Feel free to customize it
    """
    print("KS-BOT said 'welcome'")


  def BotProcessReply(self, data):
    """
      Returns bot reply to the message you sent it

      > Feel free to customize it
    """
    print("KS-BOT said: ", data)


  def TimerOver(self, data):
    """
      Handles Event Server sends when timer is over

      > Feel free to customize it
    """

    print("KS-BOT said: Timer is over, Timer: ", data)

  def weather(self, data):
    """
      This event runs whenever the server has weather report ready for you
    """
    pass

  def news(self, data):
    """
      This event runs whenever server has the news ready for you
    """
    pass

  def speak(self, what_to_speak):
    """
      This events runs when ever the server wants you to say something
    """
    pass

  def de_activate_smith(self, data):
    """
      This events runs after S.M.I.T.H has been De-Activated and KS-BOT has been activated
    """
    pass

  def activate_smith(self, data):
    """
      This event runs after S.M.I.T.H has been activated
    """
    pass
```

- Once your custom bot class is ready all that is left is for you to initialize your bot

```Python
bot = CustomBot("<your name>", "<your password>")
```

- Last but not list all you have to do is run the bot, so it can get and recieve messages from Server

```Python
bot.run()
```

- Now that your bot is recieving messages from server and can send message to server, Send your first message!

```Python
bot.send_command("<your message>", "<the timeZone you want to send the message from, default timeZone is your actual timeZone>", <log : True|False>)
```

## Developer Notes:

> -  Feel Free to reach us at: codingwithcn@gmail.com, for question
- But for issues and feature adding, we ask that you do that all on github
