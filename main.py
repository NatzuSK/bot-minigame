import nextcord
from nextcord.ext import commands
from nextcord.ui import Button, View
import json
import random
import asyncio


bot = commands.Bot(command_prefix="!", intents=nextcord.Intents.all())
config = json.load(open("config.json","r"))

def rockpaper(choice):
    bot_choice = random.choice(["rock", "paper", "scissors"])

    if choice == bot_choice:
        return "เสมอ"  

    elif choice == "rock":
        if bot_choice == "scissors":
            return "ชนะ"  
        elif bot_choice == "paper":
            return "แพ้"  

    elif choice == "paper":
        if bot_choice == "rock":
            return "ชนะ" 
        elif bot_choice == "scissors":
            return "แพ้"

    elif choice == "scissors":
        if bot_choice == "paper":
            return "ชนะ"  
        elif bot_choice == "rock":
            return "แพ้" 

    else:
        return "กรุณาเลือก 'rock', 'paper', หรือ 'scissors' เท่านั้น!"






@bot.slash_command(name="คิดเลขไว", description="ตอบโจทย์เลขให้ไว!")
async def fast_math(interaction: nextcord.Interaction):
    a = random.randint(1, 1000)
    b = random.randint(1, 1000)
    operator = random.choice(["+", "-"])

    if operator == "-" and a < b:
        a, b = b, a

    question = f"{a} {operator} {b}"
    answer = eval(question)

    question_embed = nextcord.Embed(
        color=nextcord.Color.orange(),
        title="💡 คณิตคิดไว",
        description=f"```{question} = ?```"
    )
    question_embed.set_footer(text="ตอบให้ถูกใน 10 วินาที!")

    await interaction.response.send_message(embed=question_embed, ephemeral=True)

    def check(m):
        return m.author == interaction.user and m.channel == interaction.channel

    try:
        msg = await bot.wait_for("message", timeout=10.0, check=check)
        if msg.content.strip() == str(answer):
            await msg.delete()
            result_embed = nextcord.Embed(
                color=nextcord.Color.blue(),
                title="✅ ถูกต้อง!",
                description="```เก่งมากกก 🎉```"
            )
        else:
            await msg.delete()
            result_embed = nextcord.Embed(
                color=nextcord.Color.blue(),
                title="❌ ผิดนะ",
                description=f"```คำตอบคือ {answer}```"
            )
        await interaction.followup.send(embed=result_embed, ephemeral=True)
    except asyncio.TimeoutError:
        await msg.delete()
        timeout_embed = nextcord.Embed(
            color=nextcord.Color.blue(),
            title="⏰ หมดเวลา!",
            description=f"```คำตอบคือ {answer}```"
        )
        await interaction.followup.send(embed=timeout_embed, ephemeral=True)







@bot.slash_command(name="เป้ายิ้งฉุบ", description="เริ่มเกมยิ้งฉุบ")
async def rock_paper_scissors(interaction: nextcord.Interaction):

    rock_button = Button(label="ค้อน", style=nextcord.ButtonStyle.primary, custom_id="rock")
    paper_button = Button(label="กระดาษ", style=nextcord.ButtonStyle.primary, custom_id="paper")
    scissors_button = Button(label="กรรไกร", style=nextcord.ButtonStyle.primary, custom_id="scissors")
    
    view = View()
    view.add_item(rock_button)
    view.add_item(paper_button)
    view.add_item(scissors_button)
    
    embed = nextcord.Embed(
        color=nextcord.Color.blue(),
        title="**Mini Game มาแล้ววว**",
        description="```เลือก ค้อน,กรรไกรม,กระดาษ ได้เลยยย😋```"
    )
    embed.set_image(url="https://mir-s3-cdn-cf.behance.net/project_modules/disp/d1e3cf36880203.5731151fed538.gif")

    await interaction.response.send_message(embed=embed, view=view ,ephemeral=True)

    async def button_callback(interaction: nextcord.Interaction):
        user_choice = interaction.data["custom_id"]
        result = rockpaper(user_choice)
        if result == "ชนะ":
            embed = nextcord.Embed(
                color=nextcord.Color.blue(),
                title="**คุณชนะ**",
                description="```ฟลุ๊ครึป่าวววววว 😜```"
            )
            await interaction.response.edit_message(view=None,embed=embed)
        elif result == "เสมอ":
            embed = nextcord.Embed(
                color=nextcord.Color.blue(),
                title="**เสมอ**",
                description="```ชนะไม่ได้ว้ายยๆๆๆ 😜```"
            )
            await interaction.response.edit_message(view=None,embed=embed)
        elif result == "แพ้":
            embed = nextcord.Embed(
                color=nextcord.Color.blue(),
                title="**คุณแพ้**",
                description="```อ่อนๆแพ้บอท 😜```"
            )
            await interaction.response.edit_message(view=None,embed=embed)

    rock_button.callback = button_callback
    paper_button.callback = button_callback
    scissors_button.callback = button_callback




@bot.event
async def on_ready():
    print(f'✅ Logged in as {bot.user}')


bot.run(config["token"])
