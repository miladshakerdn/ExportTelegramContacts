# ExportTelegramContacts

## Export Telegram Contacts with profile images as VCF file.
<p align="center"><a href="https://github.com/miladshakerdn/ExportTelegramContacts" ><img title="Export Telegram Contacts with profile images as VCF file" src="./ExportTelegramContacts.png" alt="UI" style="border-radius: 20px;"></a></p>

# Used for
* Backup from your Telegram contacts
* Export contact as vcf file
* Useable for phones contact list and other devices Vcard supported
* Support contact photo with high and medium quality

## How to use
1. First you have to register at https://my.telegram.org/auth
2. Then enter the retrieved 'api_id' and 'api_hash' and 'phone' in contact.py file
3. NOTIC! phone with country code.
* Sample country-code:98 phone:09120000000 => 989120000000
```contact.py
api_id = api_id
api_hash = "api_hash"
phone = 989120000000
```
4. Install the necessary dependencies python 3 [telethon,click,asyncio,...]
5. When first time run the application receives your phone number and received Telegram code. Two-step verification password receives if there are.
6. Then store Telegram connection data to CSV_contact_maker_for_phone.session ,important for reuse the program without re-registering.
7. You can now use the program. require contact  list photo or not and ...