import random
import discord
from discord.ext import commands

intents = discord.Intents.default()  # Créez un objet Intents avec les intentions par défaut
intents.typing = False  # Vous pouvez désactiver des intentions spécifiques si nécessaire
intents.presences = False
intents.message_content = True


Token = 'ODUzMjA0OTIwNjA0Njg4NDA0.Gz4-Ah.vZ1hTHUp5XhtiXRiezLzyc7uv890v9zFiTZ-bo'# clef du bot discord qui va permettre de le connecter
client = commands.Bot(command_prefix='?',intents=intents)  # prefix a mettre avant les commandes
client.remove_command('help') #permet de supprimer la commande de base du help pour qu'on puisse la remplacer par la notre


# plusieurs événements on été trouver grâce à l'API sur le site de discord
# ctx est une constante
# 'async' est une coroutine
# 'await' fais parti de la coroutine si on le met pas cela va engendrer des erreurs

@client.event  # les client.event détecte automatiquement une action, il réagit donc à un événement
async def on_ready():  # permet seulement de vérifier que le bot est bien lancé
    print("Démarrage du bot")
    print(".....DEMARRAGE.....")
    print(client.user.name, "PRET")  # va donner le nom du bot

@client.event
async def bienvenue(ctx, nouveau_membre: discord.Member):
    pseudo = nouveau_membre.mention
    await ctx.send(f"Bienvenue{pseudo}, tu fais maintenant parti du Crew")  # le 'f' permet de formaté


@client.event
async def on_command_error(ctx, error):  # va permettre de détecter s'il manque un argument par exemple pour la commande 'etat'
    if isinstance(error, commands.MissingRequiredArgument):  # isinstance va vérifier que 'error' est du même type que 'commands.MissingRequiredArgument'
        await ctx.send("Il manque un argument")


@client.command()  # les client.command vont détecter le préfixe '?' donner plus haut suivit du nom de la commande
async def edt(ctx):
    await ctx.send("Regarder vos notes : https://monucp.u-cergy.fr/uPortal/f/u410l1s6/normal/render.uP%22")


@client.command()
async def scodoc(ctx):
    await ctx.send("Regarder vos notes : https://iutcergy.org/notesscodoc/%22")


@client.command()
async def api(ctx):
    await ctx.send("Regardez l'API pour m'améliorer : https://discordpy.readthedocs.io/en/stable/api.html")


@client.command()
async def etat(ctx, *, question):  # si on ne met pas le '*' cela ne va pas prendre le reste de la phrase
    reponses = ["Je vais bien",
                "Je me sens faible",
                "Je pète la forme",
                "Je suis prêt à travailler",
                "Très bien et toi",
                "je suis un peu malade"]
    await ctx.send(f"Question: {question}\n{random.choice(reponses)}")
    # ici on formate 'question' qui est la phrase que l'on va écrire puis on formate 'reponses' qui va être chosie aléatoirement


@client.command()
async def meme(ctx):
    meme = ["https://lh3.googleusercontent.com/proxy/D7zn_QSI5oJBK1gRHUxShOqQbCWrdslHv8X3f2yVM6UYuUyRqgpRRbzglEMFmAVVhcfKl43VD6yCA9utahYkbOSXBwM7GARUSnNeH_Z6HMxJRhl5hdhhxZSwY0_27SW2mZ4r7ThQP4FDGhOdEbHio6p6pt1KXPJBfilL9hvS8YguknH9yO4vRPYmIx76JM0",
            "https://images.theconversation.com/files/256803/original/file-20190201-109820-h6bsfj.jpg?ixlib=rb-1.1.0&q=45&auto=format&w=754&fit=clipe",
            "hhttps://file1.closermag.fr/var/closermag/storage/images/1/3/0/0/1/13001774/donald-balboa.png?alias=original",
            "https://pbs.twimg.com/profile_images/1278817894952955904/u9yblLLY_400x400.jpg",
            "https://pbs.twimg.com/media/D3dPskmWAAAi9Pu.jpg",
            "https://pbs.twimg.com/media/Eh9AX8ZWsAE4Z0n.jpg",
            "https://www.bootsandcats.agency/wp-content/uploads/2017/07/comprendu.jpg"
            ]

    await ctx.send(f"{random.choice(meme)}")


# permet de donner un avis, puis de réagir dessus
@client.command()
async def avis(ctx):
    await ctx.send("Ecriver vos avis")

    def checkMessage(message):
        return message.author == ctx.message.author and ctx.message.channel == message.channel
    # vérifie que celui qui a utiliser la commande doit envoyer une réponse dans le bon channel
    try:  # c'est une exception, ici on test le temps que va prendre l'utilisateur pour écrire l'avis
        idee = await client.wait_for("message", timeout=10,
                                     check=checkMessage)  # permet d'attendre le message de l'utilisateur dans un temps donner
    except:  # si le test (le try) n'a pas fonctionner, cette partie va gérer l'erreur et va donc envoyer un message
        await ctx.send("Veuillez reformuler votre avis.")
        return
    message = await ctx.send(
        "L'avis de {} a été poser. êtes vous d'accord. Réagissez ✅. Sinon réagissez avec ❌".format(ctx.message.author))# autre manière pour formater
    await message.add_reaction("✅")  # 'message.add_reaction' va rajouter une petite îcone en dessous du message
    await message.add_reaction("❌")

    def checkEmoji(reaction,
                   user):  # ctx.message.author == user vérifie que c'est celui qui a mis le message qui doit réagir
        return ctx.message.author == user and message.id == reaction.message.id and (
                (reaction.emoji) == "✅" or (reaction.emoji) == "❌")

    try:
        reaction, user = await client.wait_for("reaction_add", timeout=10, check=checkEmoji)
        if reaction.emoji == "✅":
            await ctx.send("Avis favorable.")
        else:
            await ctx.send("Avis défavorable.")
    except:
        await ctx.send("Vous avez pris trop de temps")


@client.command()
async def python(
        ctx):  # même principe que la commande 'état' sauf qu'il n'y a pas de CheckMesssage car on en pas besoin
    message = await ctx.send("Quel cours voulez-vous ? Le 1️⃣, 2️⃣ ou le 3️⃣")
    await message.add_reaction("1️⃣")
    await message.add_reaction("2️⃣")
    await message.add_reaction("3️⃣")

    def checkEmoji(reaction, user):
        return ctx.message.author == user and message.id == reaction.message.id and (
                (reaction.emoji) == "1️⃣" or (reaction.emoji) == "2️⃣") or (reaction.emoji == "3️⃣")

    try:
        reaction, user = await client.wait_for("reaction_add", timeout=20, check=checkEmoji)
        if reaction.emoji == "1️⃣":
            await ctx.send("L’objet 'range' de python permet de créer une liste d’entier range(debut,fin,pas ) "
                           "est une liste d’entier qui va de début à fin exclus avec un pas")
        if reaction.emoji == "2️⃣":
            await ctx.send("Un moyen facile de sortir d’une boucle est d’utiliser un 'break'")
        if reaction.emoji == "3️⃣":
            await ctx.send("Une 'Liste' est un tableau (mutable ou modifiable ) de données qu’on peut parcourir")

    except:
        await ctx.send("Tu as pris trop de temps")


# commande "help"
@client.command()
async def help(ctx):
    author = ctx.message.author  # donne le nom de l'auteur du message
    embed = discord.Embed(title="Aide", description="Voici les commandes du bot",
                          colour=discord.Colour.purple())  # création de l'intégration ( ce sont des messages spéciaux )
    embed.set_author(name="Crew App")  # cela va donné le l'auteur de notre intégration, ici le nom de notre bot
    embed.add_field(name='Cours',
                    value='edt,scodoc,\n python')  # va donner nos catégories des commandes ainsi que le nom des commandes
    embed.add_field(name='Divers', value='etat,avis,api')
    embed.add_field(name="Nettoyage", value='clear')
    embed.set_thumbnail(url=ctx.author.avatar_url) #cela va nous permettre de mettre une vignette, ici celle de l'auteur de la commande
    await ctx.send(author, embed=embed)


@client.command() # Commande pour Effacer les messages
async def clear(ctx, nombre : int): #'nombre : int' permet de prendre seulement des nombres sinon cela ne marche pas
  messages = await ctx.channel.history(limit = nombre + 1).flatten() # +1 pour effacer "n" message plus le 'clear command'
  for message in messages:  #permet de répéter le 'delete' en boucle selon le nombre qu'on a mis après le clear
        await message.delete()


client.run(Token)