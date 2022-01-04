import discord

class Embed:
    def __init__(self):
        pass

    async def create_comparison_embed(self, beatmap_1_data, beatmap_2_data):
        beatmap_1_string = f"{beatmap_1_data['beatmapset']['title']} [{beatmap_1_data['version']}]"
        beatmap_2_string = f"{beatmap_2_data['beatmapset']['title']} [{beatmap_2_data['version']}]"
        beatmap_1_info = f"**Accuracy: {beatmap_1_data['accuracy']} - HP Drain: {beatmap_1_data['drain']} - BPM: {beatmap_1_data['bpm']}**"
        beatmap_2_info = f"**Accuracy: {beatmap_2_data['accuracy']} - HP Drain: {beatmap_2_data['drain']} - BPM: {beatmap_2_data['bpm']}**"
        ts = "=\t=\t=\t=\t=\t=\t" # tab string

        embed = discord.Embed(
            title="__Taiko Map Comparison__",
            color=discord.Colour.blue()
        )
        embed.description = f":blue_circle: [{beatmap_1_string}]({beatmap_1_data['url']}) - {beatmap_1_data['difficulty_rating']}:star:\n\t{beatmap_1_info}\n\n:red_circle: [{beatmap_2_string}]({beatmap_2_data['url']}) - {beatmap_2_data['difficulty_rating']}:star:\n\t{beatmap_2_info}"
        embed.add_field(name="Please choose which map you believe to be harder of the two above:",
                        value=f"{ts}{ts}{ts}{ts}{ts}{ts}\n__**Commands**__\n`-harder 1` if :blue_circle: is harder\n`-harder 2` if :red_circle: is harder\n`-harder 0` if they are roughly the same difficulty.\n**take your time making your decision, every comparison makes a difference!**")
        return embed