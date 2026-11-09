import pyperclip, pydirectinput, time, random, config
from groq import Groq

pydirectinput.PAUSE = 0.01
client = Groq(api_key=config.GROQ_API_KEY) #хуй тебе а не токен, config.py создашь, а там переменную GROQ_API_KEY, вставишь туда как с тг ботом

class Player:
    def __init__(self, nick: str, logdir: str):
        self.nick = nick # твой ник
        self.logdir = logdir # путь к latest.log (C:\\Users\\....\\.minecraft\\logs\\latest.log

    def send_message(self, message):
        pyperclip.copy(message)
        pydirectinput.press("t")
        pydirectinput.keyDown("ctrl")
        pydirectinput.press("v")
        pydirectinput.keyUp("ctrl")
        pydirectinput.press("enter")

    def main(self):
        with open(self.logdir, "r", encoding="utf-8", errors="ignore") as f:
            f.seek(0,2)
            while True:
                line = f.readline()
                if not line:
                    time.sleep(1)
                    continue
                print(line)
                if "[CHAT]" in line:
                    logline = line.split(" ")[4:]
                    usernick = logline[0].strip("<>")
                    message = " ".join(logline[1:])
                if usernick == self.nick:
                        if ".roll" in logline[1]: #Команда ролл, мне впадлу было парсить два числа, так что будет кубик 1-6, если захочешь сделаешь лучше.
                            self.send_message(f"roll 1-6:  {random.randint(1,6)}")

                        elif ".caps" in logline[1]: #а че тут, просто капсом написать чета
                            self.send_message(" ".join(logline[2:]).upper())

                        elif ".spam" in logline[1]: #спам командой, кстати не спамь .spam, рекурсию словишь
                            try:
                                retries = int(logline[2])
                            except ValueError:
                                retries = 5
                            for _ in range(retries):
                                self.send_message(" ".join(logline[3:]))

                        elif ".gpt" in logline[1]:
                            answer = client.chat.completions.create(messages=[{"role": "system", "content": "Ты майнкрафт-чатбот, отвечай ограничиваясь 256 символами, больше - игра не примет."},{"role": "user", "content":("Ты майнкрафт-чатбот, отвечай ограничиваясь 256 символами, больше - игра не примет." + "".join(logline[2:]))}],model="openai/gpt-oss-20b")
                            self.send_message(answer.choices[0].message.content[:256])

                        elif ".help" in logline[1]:
                            self.send_message(f"/tellraw {self.nick} \"---<Команды>---\"")
                            self.send_message(f"/tellraw {self.nick} \".gpt <запрос> - ИИ ответ\"")
                            self.send_message(f"/tellraw {self.nick} \".roll - кубик (1-6)\"")
                            self.send_message(f"/tellraw {self.nick} \".spam <кол-во> <текст> - спам (деф. 5)\"")
                            self.send_message(f"/tellraw {self.nick} \".caps <текст> - КАПС\"")
                else: pass




if __name__ == "__main__":
    player = Player(nick=config.NICKNAME, logdir=config.LOGPATH)
    player.main()