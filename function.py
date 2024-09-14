import discord
from discord import Embed
from discord.ui import Button, View
from discord.ext import commands, tasks
import random

class Cleaner:
    def __init__(self):
        self.Recommendations = ["öneri1","öneri2","öneri3"]
    
    async def YesCallBack(self, interaction: discord.Interaction):
        await interaction.followup.send("Glad to hear that!", ephemeral=True, view=self.GetAnotherView())

    async def NoCallback(self, interaction: discord.Interaction):
        await interaction.followup.send(self.GetARecommendation(), ephemeral=True, view=self.GetYesOrNoView())    

    async def ThanksCallback(self, interaction: discord.Interaction):
        await interaction.followup.send("Yor'ue welcome", ephemeral=True)   

    async def GetAnother(self, interaction: discord.Interaction):
        await interaction.followup.send("Glad to hear that!", ephemeral=True, view=self.GetYesOrNoView())

    def ButtonCallbackMatcher(self, buttonList: list, name: str, View:View):
        for i in range(len(buttonList)):
            callback = ""

            match name:
                case "Yes":
                    callback = self.YesCallBack()
                case "No":
                    callback = self.NoCallback()
                case "Thank you!":
                    callback = self.ThanksCallback()
                case "Get Another Recommendation!":
                    callback = self.GetAnother()

            buttonList[i].callback = callback
            View.add_item(buttonList[i])

    def ButtonListMaker(self, length:int, names:list, styles:list, emojis:list = None) -> list:
        buttonList = []

        for i in range(length):
            button = Button(label=names[i], emoji=emojis[i] if emojis else None, style=styles[i])
            buttonList.append(button)

        return buttonList

    def GetARecommendation(self):
        recommendation = random.choice(self.Recommendations)

        return recommendation

    def GetYesOrNoView(self) -> View:
        view = View

        names = []
        emojis = []
        styles = []

        names.append("Yes"); emojis.append("👍"), styles.append(discord.ButtonStyle.success)
        names.append("No"); emojis.append("👎"), styles.append(discord.ButtonStyle.red)

        ButtonList = self.ButtonListMaker(length=2, names=names, emojis=emojis, styles=styles)      

        self.ButtonCallbackMatcher(buttonList=ButtonList, name=names, view=view)

        return view
    
    def GetAnotherView(self) -> View:
        view = View

        names = []
        emojis = []
        styles = []

        names.append("Get Another Recommendation!"); emojis.append("✅"), styles.append(discord.ButtonStyle.success)
        names.append("Thank you!"); emojis.append("👌"), styles.append(discord.ButtonStyle.gray)

        ButtonList = self.ButtonListMaker(length=2, names=names, emojis=emojis, styles=styles)      

        self.ButtonCallbackMatcher(buttonList=ButtonList, name=names, view=view)

        return view
    
async def Starter(interaction: discord.Interaction):
    cleaner = Cleaner()
    await interaction.followup.send(cleaner.GetARecommendation(), ephemeral=True, view=cleaner.GetYesOrNoView())
