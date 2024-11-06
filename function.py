import discord
from discord import Embed
from discord.ui import Button, View
from discord.ext import commands, tasks
import random

class Cleaner:
    def __init__(self):
        self.Recommendations = ["öneri1", "öneri2", "öneri3"]
    
    async def YesCallBack(self, interaction: discord.Interaction):
        await interaction.response.send_message("Glad to hear that!", ephemeral=True, view=self.GetAnotherView())

    async def NoCallback(self, interaction: discord.Interaction):
        await interaction.response.send_message(self.GetARecommendation(), ephemeral=True, view=self.GetYesOrNoView())    

    async def ThanksCallback(self, interaction: discord.Interaction):
        await interaction.response.send_message("You're welcome", ephemeral=True)   

    async def GetAnother(self, interaction: discord.Interaction):
        await interaction.response.send_message("Here's another recommendation!", ephemeral=True, view=self.GetYesOrNoView())

    def ButtonCallbackMatcher(self, buttonList: list, names: list, view: View):
        for i in range(len(buttonList)):
            match names[i]:
                case "Yes":
                    buttonList[i].callback = self.YesCallBack
                case "No":
                    buttonList[i].callback = self.NoCallback
                case "Thank you!":
                    buttonList[i].callback = self.ThanksCallback
                case "Get Another Recommendation!":
                    buttonList[i].callback = self.GetAnother

            view.add_item(buttonList[i])

    def ButtonListMaker(self, length: int, names: list, styles: list, emojis: list = None) -> list:
        buttonList = []

        for i in range(length):
            button = Button(label=names[i], emoji=emojis[i] if emojis else None, style=styles[i])
            buttonList.append(button)

        return buttonList

    def GetARecommendation(self):
        recommendation = random.choice(self.Recommendations)
        return recommendation

    def GetYesOrNoView(self) -> View:
        view = View()

        names = ["Yes", "No"]
        emojis = ["👍", "👎"]
        styles = [discord.ButtonStyle.success, discord.ButtonStyle.danger]

        buttonList = self.ButtonListMaker(length=2, names=names, styles=styles, emojis=emojis)
        self.ButtonCallbackMatcher(buttonList=buttonList, names=names, view=view)

        return view
    
    def GetAnotherView(self) -> View:
        view = View()

        names = ["Get Another Recommendation!", "Thank you!"]
        emojis = ["✅", "👌"]
        styles = [discord.ButtonStyle.success, discord.ButtonStyle.secondary]

        buttonList = self.ButtonListMaker(length=2, names=names, styles=styles, emojis=emojis)
        self.ButtonCallbackMatcher(buttonList=buttonList, names=names, view=view)

        return view
    
async def Starter(interaction: discord.Interaction):
    cleaner = Cleaner()
    await interaction.response.send_message(cleaner.GetARecommendation(), ephemeral=True, view=cleaner.GetYesOrNoView())
