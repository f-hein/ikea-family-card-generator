import requests
import luhn
from PIL import Image, ImageDraw, ImageFont
import os

barcode_addr = 'https://ikea-imgsrv.loyaltypoint.pl/getBarcode.ashx?cn='
card_number = '62759 8043'


def generate_and_save_barcode(card_no):
    barcode_addr = 'https://ikea-imgsrv.loyaltypoint.pl/getBarcode.ashx?cn=' + card_no
    print(barcode_addr)
    r = requests.get(barcode_addr)
    if r.status_code == 200:
        with open('barcode.png', 'wb') as f:
            for chunk in r:
                f.write(chunk)


def generate_loyalty_card(name_surname, card_no):
    # replace transparency with white colour
    barcode = Image.open('barcode.png')
    pixel_data = barcode.load()
    if barcode.mode == "RGBA":
        for y in range(barcode.size[1]):
            for x in range(barcode.size[0]):
                if pixel_data[x, y][3] < 255:
                    pixel_data[x, y] = (255, 255, 255, 255)
    barcode.save('barcode2.png')
    # add barcode to background
    background = Image.open('background.png')
    barcode = Image.open('barcode2.png')
    background.paste(barcode, (20, 110))
    background.convert('RGBA').save('background_with_barcode.png')
    os.remove('barcode2.png')
    # add credentials to the card
    background = Image.open('background_with_barcode.png')
    font_type = ImageFont.truetype('verdana.ttf', size=11)
    draw = ImageDraw.Draw(background)
    draw.text((20, 170), name_surname.upper(), fill='#000000', font=font_type)
    draw.text((20, 185), card_no, fill='#000000', font=font_type)
    background.show()
    background.save('your_finished_card.png')
    os.remove('barcode.png')
    os.remove('background_with_barcode.png')


if __name__ == "__main__":
    name_surname = input('Please provide your name and surname: ')
    while True:
        second_part_of_card_no = (input('Please pick your card number (9 Xs) [62759 8043 XXXX XXXX X]: '))
        card_no = (card_number + second_part_of_card_no).replace(' ', '')
        print(len(card_no))
        card_no_with_checksum = luhn.append(card_no)
        if luhn.verify(card_no_with_checksum) \
                and len(card_no) == 18 \
                and card_no.isdigit():
            print('Your final card number: {}, verification by Luhn algorithm says: {}'
                  .format(card_no_with_checksum, luhn.verify(card_no_with_checksum)))
            generate_and_save_barcode(card_no_with_checksum)
            generate_loyalty_card(name_surname, card_no_with_checksum)
            print("Your card is saved and ready for action! :)")
            break
        else:
            print("[!] Could not create a card. Number you provided was corrupted in some way.")