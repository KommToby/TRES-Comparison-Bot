import discord

class Embed:
    def __init__(self):
        pass

    async def create_comparison_embed(self, beatmaps_data):
        description = ""
        for i in range(0, 10):
            description = description + f"{i}. [{beatmaps_data[i]['beatmapset']['title']} [{beatmaps_data[i]['version']}]]({beatmaps_data[i]['url']}) - {beatmaps_data[i]['difficulty_rating']}:star:\n\t**Accuracy: {beatmaps_data[i]['accuracy']} - HP Drain: {beatmaps_data[i]['drain']} - BPM: {beatmaps_data[i]['bpm']}**\n\n"
        ts = "=\t=\t=\t=\t=\t=\t" # tab string

        embed = discord.Embed(
            title="__Taiko Map Comparison__",
            color=discord.Colour.blue()
        )
        embed.description = description
        embed.add_field(name="Please order the maps above in which you believe to be hardest -> easiest",
                        value=f"{ts}{ts}{ts}{ts}{ts}{ts}\n__**Commands**__\n`-harder x x x x x x x x x x` where x is a number 0-9\n`-skip` if you want to skip this comparison and generate a new one.\n**take your time making your decision, every comparison makes a difference!**")
        return embed

    async def create_confirmation_embed(self, beatmaps_data, discord_id, password):
        ts = "=\t=\t=\t=\t=\t=\t" # tab string
        embed = discord.Embed(
            title="__Confirmation Needed__",
            color=discord.Colour.red()
        )
        description = ""
        for i, beatmap in enumerate(beatmaps_data):
            if i == 0:
                description = description + f"**{i}:** {beatmap['difficulty_rating']}☆: [{beatmap['beatmapset']['title']} [{beatmap['version']}]]({beatmap['url']})** <- (Hardest)**\n"
            elif i == len(beatmaps_data)-1:
                description = description + f"**{i}:** {beatmap['difficulty_rating']}☆: [{beatmap['beatmapset']['title']} [{beatmap['version']}]]({beatmap['url']})** <- (Easiest)**\n"
            else:
                description = description + f"**{i}:** {beatmap['difficulty_rating']}☆: [{beatmap['beatmapset']['title']} [{beatmap['version']}]]({beatmap['url']})\n"
        description = description + f"{ts}{ts}{ts}{ts}{ts}{ts}"
        embed.description = description
        embed.add_field(name="Please confirm the order above is the order you have selected (hardest at the top, easiest at the bottom)",
                        value=f"`There is no undo command. There is no going back after confirming!`\n**To retry:** use the `-harder` command again.\n**To confirm:** please write `-confirm {password}`" )
        return embed