import nest_asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import logging
import asyncio

# Enable nested asyncio
nest_asyncio.apply()

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Command to start the bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Selamat datang di Bot Penghitung Nutrisi Pakan Ayam!')

# Command to help user input
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Kirim data pakan dengan format:\n\n'
                                     'Nama Bahan, Protein (%), Energi (kkal/kg), Harga (Rp/kg), Berat (kg)\n\n'
                                     'Contoh: Jagung, 8.5, 3330, 3000, 1')

# Function to calculate nutrition
def calculate_nutrition(data):
    total_protein = 0
    total_energy = 0
    total_price = 0
    total_weight = 0
    
    for item in data:
        name, protein, energy, price, weight = item.split(',')
        protein = float(protein)
        energy = float(energy)
        price = float(price)
        weight = float(weight)

        total_protein += protein * weight
        total_energy += energy * weight
        total_price += price * weight
        total_weight += weight

    return (total_protein / total_weight, total_energy / total_weight, total_price / total_weight) if total_weight else (0, 0, 0)

# Handle incoming messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_input = update.message.text
    data = user_input.splitlines()
    results = calculate_nutrition(data)

    response = (f'Total Protein: {results[0]:.2f}%\n'
                f'Total Energi: {results[1]:.2f} kkal/kg\n'
                f'Total Harga: Rp {results[2]:.2f}/kg')

    await update.message.reply_text(response)

async def main():
    # Replace 'YOUR_TOKEN' with your bot token
    application = ApplicationBuilder().token("7811042692:AAEw3hjT_H5VwW8ZBcLz8ctkmEHq06wpJzk").build()

    # Register commands and message handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start the bot
    await application.run_polling()

if __name__ == '__main__':
    asyncio.run(main())