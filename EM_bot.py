from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

async def start(update: Update, context: CallbackContext):
    await update.message.reply_text('Halo! Saya bot penghitung energi metabolisme. Gunakan perintah /hitung untuk mulai.')

async def hitung(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "Masukkan nilai dalam format berikut (pisahkan dengan spasi):\n"
        "Kadar Air (%) Abu (%) Protein Kasar (%) Lemak Kasar (%) Serat Kasar (%)\n"
        "Contoh: 10 5 20 15 10"
    )

async def handle_message(update: Update, context: CallbackContext):
    try:
        # Ambil input pengguna
        text = update.message.text
        values = list(map(float, text.split()))

        if len(values) != 5:
            await update.message.reply_text("Mohon masukkan 5 angka sesuai format yang diminta.")
            return

        moisture, ash, protein, fat, fiber = values

        # Hitung BETN
        betn = 100 - (moisture + ash + protein + fat + fiber)

        # Hitung Energi Metabolisme (ME)
        me = (53 * protein) + (85 * fat) + (37 * betn)

        # Hitung TDN
        tdn = protein + (fat * 2.25) + betn - (ash * 0.5) - fiber

        # Kirim hasil ke pengguna
        await update.message.reply_text(
            f"Hasil Perhitungan:\n\n"
            f"Kadar Air: {moisture}%\n"
            f"Abu: {ash}%\n"
            f"Protein Kasar: {protein}%\n"
            f"Lemak Kasar: {fat}%\n"
            f"Serat Kasar: {fiber}%\n"
            f"BETN: {betn:.2f}%\n"
            f"Energi Metabolisme: {me:.2f} kkal/kg\n"
            f"TDN: {tdn:.2f}%"
        )
    except ValueError:
        await update.message.reply_text("Ada kesalahan dalam format input. Pastikan kamu memasukkan angka dengan benar.")

def main():
    application = Application.builder().token("7988022748:AAFxqIiAY4ySbCdbHIxsBOfsca_JRaoErE8").build()

    # Handler untuk /start
    application.add_handler(CommandHandler("start", start))
    
    # Handler untuk /hitung
    application.add_handler(CommandHandler("hitung", hitung))
    
    # Handler untuk semua pesan (input nilai)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling()

if __name__ == '__main__':
    main()