import config
import discord
import random
from discord.ext import commands

bot_intents = discord.Intents.default()
bot_intents.message_content = True

bot = commands.Bot(command_prefix=">:", intents=bot_intents, strip_after_prefix=True)

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}!")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return None

    if message.content.startswith("Binocular") or message.content.startswith("binocular"):
        if message.author.id == config.aspbix_id:
            roll = False
            if "roll" in message.content or "Roll" in message.content:
                roll = True # Roll: special command to show list of commands
            if roll:
                await message.channel.send(f"{message.author.mention} {random.choice(config.comms_ac)}")
                await message.channel.send(f"{random.choice(config.rolls)}")
                await message.author.send(config.command_registry)
            else:
                await message.channel.send(f"{message.author.mention} {random.choice(config.comms_ac)}")
                await message.author.send(random.choice(config.direct["follow_up"]))
        else:
            await message.channel.send(f"{message.author.mention} {random.choice(config.comms_dc)}")

    await bot.process_commands(message)


@bot.command()
async def dextools(ctx, tool, *, subject):
    if ctx.author.id in config.superuser:
        if tool == "rtag":
            subject = subject.strip()

            if subject == "me":
                target = ctx.author
            else:
                target = ctx.guild.get_member_named(subject)
                if target is None:
                    try:
                        results = await ctx.guild.query_members(query=subject, limit=1)
                        if results:
                            target = results[0]
                        else:
                            await ctx.send(f"{ctx.author.mention} `:: 🔎❌ rtag: user not found. ;;`")
                            return
                    except:
                        await ctx.send(f"{ctx.author.mention} `:: 🔎❌ rtag: user not found. ;;`")
                        return

            role_list = [role.name for role in target.roles if role.name != "@everyone"]
            roles = ", ".join(role_list) if role_list else "No Roles"

            embed_recon = discord.Embed(
                title="🔎✅ **TAG SUCCESS, SUBJECT FOUND.**",
                color=discord.Color.dark_red(),
            )

            embed_recon.add_field(name="Username", value=target.name, inline=True)
            embed_recon.add_field(name="Display", value=target.display_name, inline=True)
            embed_recon.add_field(name="User ID", value=str(target.id), inline=True)
            embed_recon.add_field(name="Roles", value=roles, inline=False)
            embed_recon.add_field(name="App?", value=str(target.bot), inline=True)
            embed_recon.add_field(name="Joined", value=target.joined_at.strftime('%Y-%m-%d') if target.joined_at else 'Unknown', inline=True)
            embed_recon.add_field(name="Created", value=target.created_at.strftime('%Y-%m-%d') if target.created_at else 'Unknown', inline=True)
            embed_recon.set_image(url=target.display_avatar.url)
            
            await ctx.send(ctx.author.mention)
            await ctx.send(embed=embed_recon)
        elif tool == "global":
            if subject == "me":
                target = await bot.fetch_user(ctx.author.id)

                embed_global = discord.Embed(
                    title="📡🌐 **GLOBAL TAG SUCCESS, SUBJECT FOUND.**",
                    color=discord.Color.dark_red(),
                )

                embed_global.add_field(name="Username", value=target.name, inline=True)
                embed_global.add_field(name="Display", value=target.display_name, inline=True)
                embed_global.add_field(name="User ID", value=str(target.id), inline=True)
                embed_global.add_field(name="App?", value=str(target.bot), inline=True)
                embed_global.add_field(name="Created", value=target.created_at.strftime('%Y-%m-%d') if target.created_at else 'Unknown', inline=True)
                embed_global.set_image(url=target.display_avatar.url)

                await ctx.send(ctx.author.mention)
                await ctx.send(embed=embed_global)
            else:
                try: 
                    subject = int(subject)
                    if isinstance(subject, int):
                        try:
                            target = await bot.fetch_user(subject)

                            embed_global = discord.Embed(
                                title="📡🌐 **GLOBAL TAG SUCCESS, SUBJECT FOUND.**",
                                color=discord.Color.dark_red(),
                            )

                            embed_global.add_field(name="Username", value=target.name, inline=True)
                            embed_global.add_field(name="Display", value=target.display_name, inline=True)
                            embed_global.add_field(name="User ID", value=str(target.id), inline=True)
                            embed_global.add_field(name="App?", value=str(target.bot), inline=True)
                            embed_global.add_field(name="Created", value=target.created_at.strftime('%Y-%m-%d') if target.created_at else 'Unknown', inline=True)
                            embed_global.set_image(url=target.display_avatar.url)

                            await ctx.send(ctx.author.mention)
                            await ctx.send(embed=embed_global)
                        except discord.NotFound:
                            await ctx.send(f"{ctx.author.mention} `:: 📡❌ global: user not found.`")
                    else:
                        await ctx.send(f"{ctx.author.mention} `:: 📡 global: integer (user.id) parameters required. ;;`")
                except ValueError:
                    print(f"{ctx.author} attempt alphanumeric in global syntax. ")
                    await ctx.send(f"{ctx.author.mention} `:: 📡 global: integer (user.id) parameters required. ;;`")
        else:
            await ctx.send(f"{ctx.author.mention} `:: 🔧 DexTools: unrecognized command! ;;`")
    else:
        await ctx.send(f"{ctx.author.mention} `:: ❌ DexTools: unauthorized permission to use DexTools. ;;`")

@bot.command()
async def rrr(ctx, tool = None):
    if tool == "acc":
        if ctx.author.id == config.aspbix_id:
            auth = "Owner"
        elif ctx.author.id in config.superuser:
            auth = "Premium"
        else:
            auth = "Basic"

        rrr_card = discord.Embed(
            title="🎖️ **RRRecon Member Card**",
            color=discord.Color.dark_red()
        )

        rrr_card.add_field(name="Name", value=ctx.author.name, inline=True)
        rrr_card.add_field(name="Status", value=auth, inline=True)
        rrr_card.set_image(url=ctx.author.display_avatar.url)
        
        await ctx.send(ctx.author.mention)
        await ctx.send(embed=rrr_card)
    elif tool == "guild":
        server = bot.get_guild(ctx.guild.id)

        guild_card = discord.Embed(
            title="🛡️ **Current Server**",
            color=discord.Color.dark_red()
        )

        server_channel = [channel.name for channel in server.channels]
        channels = ", ".join(server_channel)

        server_role = [role.name for role in server.roles if role.name != "@everyone"]
        roles = ", ".join(server_role) if server_role else "No Roles"

        guild_card.add_field(name="Server Name", value=server.name, inline=True)
        guild_card.add_field(name="Server ID", value=server.id, inline=True)
        guild_card.add_field(name="Description", value=server.description, inline=False)
        guild_card.add_field(name="Channels", value=channels, inline=False)
        guild_card.add_field(name="Roles", value=roles, inline=False)
        guild_card.set_image(url=server.icon.url)

        await ctx.send(ctx.author.mention)
        await ctx.send(embed=guild_card)
    else:
        await ctx.send(f"{ctx.author.mention} `:: 🔧 rrr: unrecognized command! ;;`")

if __name__ == "__main__":
    bot.run(config.bot_token)