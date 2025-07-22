import discord
from discord.ext import commands

TOKEN = "MTM5NzA2MDIwMDc3MDMxMDE3NQ.GUjGXL.OPdeVNYWiAmAobobx_Y42_RT4A2GKofeLx_d6o"  # <-- Replace with your bot token
PREFIX = "!"
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix=PREFIX, intents=intents)

# --- Allowed Users ---
ALLOWED_USERS = ["drhandle", "itsbielzinn"]

def is_allowed_user(ctx):
    return ctx.author.name in ALLOWED_USERS

@bot.event
async def on_ready():
    print(f"✅ Bot is online as {bot.user}")

# Kick
@bot.command()
async def kick(ctx, member: discord.Member, *, reason="No reason provided"):
    if not is_allowed_user(ctx):
        return await ctx.send("❌ You are not allowed to use this command.")
    await member.kick(reason=reason)
    await ctx.send(f"🚫 {member} has been kicked. Reason: {reason}")

# Ban
@bot.command()
async def ban(ctx, member: discord.Member, *, reason="No reason provided"):
    if not is_allowed_user(ctx):
        return await ctx.send("❌ You are not allowed to use this command.")
    await member.ban(reason=reason)
    await ctx.send(f"🔨 {member} has been banned. Reason: {reason}")

# Clear
@bot.command()
async def clear(ctx, amount: int = 5):
    if not is_allowed_user(ctx):
        return await ctx.send("❌ You are not allowed to use this command.")
    await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f"🧹 Cleared {amount} messages.", delete_after=3)

# Mute
@bot.command()
async def mute(ctx, member: discord.Member, *, reason="No reason provided"):
    if not is_allowed_user(ctx):
        return await ctx.send("❌ You are not allowed to use this command.")
    mute_role = discord.utils.get(ctx.guild.roles, name="Muted")
    if not mute_role:
        mute_role = await ctx.guild.create_role(name="Muted")
        for channel in ctx.guild.channels:
            await channel.set_permissions(mute_role, speak=False, send_messages=False)
    await member.add_roles(mute_role)
    await ctx.send(f"🔇 {member} has been muted. Reason: {reason}")

# Unmute
@bot.command()
async def unmute(ctx, member: discord.Member):
    if not is_allowed_user(ctx):
        return await ctx.send("❌ You are not allowed to use this command.")
    mute_role = discord.utils.get(ctx.guild.roles, name="Muted")
    if mute_role in member.roles:
        await member.remove_roles(mute_role)
        await ctx.send(f"🔊 {member} has been unmuted.")

bot.run(TOKEN)
