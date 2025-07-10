import os, discord
from discord.ext import commands
from config import api_key, TOKEN
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
import PIL.Image

# Pastikan folder temp ada
if not os.path.exists('./temp'):
    os.makedirs('./temp')

# Inisialisasi bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

# Event saat bot siap
@bot.event
async def on_ready():
    print(f'Kami telah masuk sebagai {bot.user}')

# Perintah !start
@bot.command(name='start')
async def start(ctx):
    async with ctx.typing():
        await ctx.send("Halo! Saya adalah bot AI untuk mengedit gambar. Kirim perintah `!edit` disertai gambar dan prompt editan.")

# Perintah !help
@bot.command(name='help')
async def help_command(ctx):
    help_text = (
        "**Panduan Bot AI Edit Gambar:**\n\n"
        "`!start` - Memulai interaksi dengan bot\n"
        "`!help` - Menampilkan bantuan ini\n"
        "`!edit <deskripsi>` - Gunakan ini dengan melampirkan gambar dan memberi deskripsi edit\n\n"
        "Contoh: `!edit tambahkan efek api pada pedang`"
    )
    async with ctx.typing():
        await ctx.send(help_text)

# Event untuk pesan
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    await bot.process_commands(message)

    if not message.content.startswith("!edit"):
        return

    if not message.attachments:
        await message.channel.send("Mohon lampirkan gambar untuk diproses.")
        return

    # Kirim pesan loading
    status_msg = await message.channel.send("🛠️ Sedang membuat gambar...")

    for attachment in message.attachments:
        file_name = attachment.filename
        temp_input_path = f"./temp/{file_name}"
        temp_output_path = "./temp/output_image.png"

        await attachment.save(temp_input_path)

        try:
            image = PIL.Image.open(temp_input_path)
            text_input = message.content[len("!edit"):].strip()

            client = genai.Client(api_key=api_key)

            async with message.channel.typing():
                response = client.models.generate_content(
                    model="gemini-2.0-flash-preview-image-generation",
                    contents=[text_input, image],
                    config=types.GenerateContentConfig(
                        response_modalities=['TEXT', 'IMAGE']
                    )
                )

            for part in response.candidates[0].content.parts:
                if part.text is not None:
                    print(part.text)
                elif part.inline_data is not None:
                    gen_image = Image.open(BytesIO(part.inline_data.data))
                    gen_image.save(temp_output_path)

            # Kirim gambar hasil
            with open(temp_output_path, 'rb') as r:
                await message.channel.send(file=discord.File(r, 'output_image.png'))

        except Exception as e:
            await message.channel.send(f"Terjadi kesalahan saat memproses gambar: {e}")

        finally:
            # Hapus file input & output setelah digunakan
            if os.path.exists(temp_input_path):
                os.remove(temp_input_path)
            if os.path.exists(temp_output_path):
                os.remove(temp_output_path)
            # Hapus pesan status
            await status_msg.delete()


if __name__ == "__main__":
    bot.run(TOKEN)
