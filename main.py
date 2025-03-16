import discord
from numpy import random
import configparser
import pkgutil

config_data = pkgutil.get_data("jamcito", "config.ini").decode("utf-8")

config = configparser.ConfigParser()
config.read_string(config_data)
d_config = config['DEFAULT']

print(d_config)

JAM_SERVER = int(d_config['jam server']) 
TEST_SERVER = int(d_config['test server'])  
JAM_GENERAL_CHAT = int(d_config['jam general chat']) 
TEST_GENERAL_CHAT = int(d_config['test general chat'])

SPAM_COUNT_THRESHOLD = 10

INSULTOS_A_TARO = ["taro maricón"]
SALUDO_A_DANIELA = ["Una Daniela Beatriz!", "Una viciosa manca!", "Ya te toca dormir oye! {0.mention}"]
SALUDO_A_VERO = ["Una viciosa eh mierda!", "Una Georgina!"]
SALUDO_A_MARIHUANO = ["Un Marihuano!", "Un papá de Baloo!"]
SALUDO_A_TARO = ["Un marica!", "Y Karen? {0.mention}"]
SALUDO_A_GERARDO = ["Nadie importante", "Papá?"]
SALUDO_A_MAURICIO = ["Un enfermo!", "maincra, maincra :v"]


last_author_in_channel = {}
same_author_message_count = {}
taro_invokation_progress = 0

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  if await manage_spam(message):
    return
  message_content = process_message_content(message.content)
  if message_content == "MARICA":
    await invoke_taro(message.channel)
    return
  global taro_invokation_progress
  taro_invokation_progress = 0
  if "JAMCITO" in message_content or client.user in message.mentions:
    await jamcito_responds(message)
    return
  if mandaron_a_la_mierda(message_content):
    await jamcito_te_manda_a_la_mierda(message)

@client.event
async def on_voice_state_update(member, before, after):
  message = greeting_on_voice_channel(member)
  if just_connected_to(TEST_SERVER, before, after):
    await client.get_channel(TEST_GENERAL_CHAT).send(message)
  if just_connected_to(JAM_SERVER, before, after):
    await client.get_channel(JAM_GENERAL_CHAT).send(message)
  if just_left_voice_channel(JAM_SERVER, before, after):
    allowed = discord.AllowedMentions()
    await client.get_channel(JAM_GENERAL_CHAT).send("Adiós perra {0.mention}".format(member), allowed_mentions=allowed)
  if just_left_voice_channel(TEST_SERVER, before, after):
    allowed = discord.AllowedMentions()
    await client.get_channel(TEST_GENERAL_CHAT).send("Adiós perra {0.mention}".format(member), allowed_mentions=allowed)

def just_connected_to(server_id, before, after):
  return after.channel != None and after.channel.guild.id == server_id and before.channel == None and after.channel != None

def just_left_voice_channel(server_id, before, after):
  return before.channel != None and before.channel.guild.id == server_id and after.channel == None

def greeting_on_voice_channel(user):
  index = random.randint(100)
  if user.name == 'ger4rdo.92':
    return SALUDO_A_GERARDO[index % 2].format(user)
  if user.name == 'veka92':
    return SALUDO_A_VERO[index % 2].format(user)
  if user.name == 'frooz0148':
    return SALUDO_A_MARIHUANO[index % 2].format(user)
  if user.name == 'notechies':
    return SALUDO_A_TARO[index % 2].format(user)
  if user.name == 'spiderdani_':
    return SALUDO_A_DANIELA[index % 3].format(user)
  if user.name == 'tester2600':
    return SALUDO_A_MAURICIO[index % 2].format(user)
  return "Una mujerzuela!"

async def manage_spam(message):
  user = message.author
  if 'Dice Roller' in user.name:
    return False
  channel_id = message.channel.id
  if channel_id in last_author_in_channel:
    if last_author_in_channel[channel_id] == user.name:
      same_author_message_count[channel_id] += 1
      if same_author_message_count[channel_id] > SPAM_COUNT_THRESHOLD:
        allowed = discord.AllowedMentions()
        await message.channel.send("Callate mierda! {0.mention}".format(user), allowed_mentions=allowed)
        return True
    else:
      same_author_message_count[channel_id] = 1
  else:
    last_author_in_channel[channel_id] = user.name
    same_author_message_count[channel_id] = 1
  return False

async def jamcito_te_manda_a_la_mierda(message):
  response = "Si andáte a la mierda :v"
  await message.channel.send(response)

def mandaron_a_la_mierda(message_content):
  return "ANDATE A LA MIERDA" in message_content or \
  "ANDÁTE A LA MIERDA" in message_content or \
  "VETE A LA MIERDA" in message_content or \
  "VETE A LA MIERDA" in message_content or \
  "VAYA A ECHARSE" in message_content

async def jamcito_responds(message):
  c = process_message_content(message.content)
  if "JAMCITO?" in c:
    await message.channel.send("Volví perras :sunglasses:")
    return
  if is_greetings(c):
    await message.channel.send("Hola {0}!".format(message.author.display_name))
    return
  if is_what_you_do(c):
    await message.channel.send("Lo que tú quieras bebé")
    return
  if is_insult(c):
    await message.channel.send("Ni que fuera taro")
    return
  await message.channel.send("Hablan de mi? :eyes:")

def is_greetings(message_content):
  return "HOLA" in message_content or \
  "QUE HAY" in message_content or \
  "BUENAS" in message_content or \
  "JELOU" in message_content or \
  "HELLO" in message_content or \
  "HENLO" in message_content or \
  "HENLO" in message_content or \
  "QUÉ HAY" in message_content

def is_what_you_do(message_content):
  return "PARA QUE SERVIS" in message_content or \
  "PARA QUE SIRVES" in message_content or \
  "QUE HACE" in message_content or \
  "PARA QUÉ SERVÍS" in message_content or \
  "PARA QUÉ SIRVES" in message_content or \
  "QUÉ HACE" in message_content or\
  "QUIÉN ES" in message_content or\
  "QUIÉN SOS" in message_content or\
  "QUÉ ES" in message_content or\
  "QUE ES" in message_content or\
  "QUIEN SOS" in message_content or\
  "QUIEN ES" in message_content

def is_insult(message_content):
  return "CHUPA PICHI" in message_content or \
  "CHUPAPICHI" in message_content or \
  "HIJO DE PUTA" in message_content or \
  "HIJO DE PERRA" in message_content or \
  "MARICON" in message_content or \
  "MARICÓN" in message_content or \
  "MARICA" in message_content or \
  "CHUPALA" in message_content or \
  "CHUPAMELA" in message_content or \
  "PENDEJO" in message_content or \
  "GAY" in message_content or \
  "PERRA" in message_content or \
  "PERRO" in message_content or \
  "PUTA" in message_content or \
  "PUTO" in message_content

async def invoke_taro(channel):
  global taro_invokation_progress
  if taro_invokation_progress == 0:
    await channel.send("QUIÉN?")
    taro_invokation_progress += 1
    return
  if taro_invokation_progress == 1:
    await channel.send("TU")
    taro_invokation_progress += 1
    return 
  if taro_invokation_progress == 2:
    await channel.send("YO?")
    taro_invokation_progress += 1
    return 
  if taro_invokation_progress == 3:
    user = discord.utils.get(channel.guild.members, name="notechies")
    allowed = discord.AllowedMentions()
    await channel.send("TARO! {0.mention}".format(user), allowed_mentions=allowed)
    taro_invokation_progress = 0
    return 
    
    

def process_message_content(message_content):
  c = message_content.upper()
  c = " ".join(c.split())
  return c

client.run(d_config['token'])

def main():
  print("running")
