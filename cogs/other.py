def gtm(message):
    if message.text:
        print('Пользователь {}, @{}, {} написал: {}'.format(message.from_user.id, message.from_user.username, message.from_user.first_name, message.text))
    elif message.photo:
        print('Пользователь {}, @{}, {} отправил фото: {}'.format(message.from_user.id, message.from_user.username, message.from_user.first_name, message.photo[0].file_id))
    elif message.sticker:
        print('Пользователь {}, @{}, {} отправил стикер: {}'.format(message.from_user.id, message.from_user.username, message.from_user.first_name, message.sticker.emoji))
    elif message.location:
        print('Пользователь {}, @{}, {} отправил локацию'.format(message.from_user.id, message.from_user.username, message.from_user.first_name))

print("Cogs | other.py is ready")