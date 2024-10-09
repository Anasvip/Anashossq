import telebot
from anti_deepnude import process_image

# التوكن الخاص بالبوت الذي تحصلت عليه من BotFather
API_TOKEN = 'YOUR_BOT_API_TOKEN'

bot = telebot.TeleBot(API_TOKEN)

# رسالة الترحيب
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "أهلاً! أرسل لي صورة وسأقوم بإزالة الملابس منها.")

# استقبال الصورة من المستخدم
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    try:
        # تحميل الصورة من تيليجرام
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        with open("input_image.jpg", 'wb') as new_file:
            new_file.write(downloaded_file)
        
        # معالجة الصورة باستخدام الذكاء الاصطناعي
        output_image_path = process_image("input_image.jpg")
        
        # إرسال الصورة الناتجة
        with open(output_image_path, 'rb') as img:
            bot.send_photo(message.chat.id, img)
    
    except Exception as e:
        bot.reply_to(message, f"حدث خطأ: {str(e)}")

# تشغيل البوت
bot.polling()
