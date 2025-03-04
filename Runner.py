import subprocess, multiprocessing
from Extractors.Utils.DB import DB

db = DB()

commands = []

scrape_id = db.create_new_scrape_id()
command = 'python .\Extractors\ListingsExtractor.py --url "%url%" --neighborhood "%neighborhood%" --scrapeid %scrape_id%'

urls_to_scrape = db.get_urls_to_scrape()
for url in urls_to_scrape:
    commands.append(
        command.replace("%url%", url[0])
        .replace("%neighborhood%", url[1])
        .replace("%scrape_id%", scrape_id)
    )

print(f"Total commands: {str(len(commands))}")

for command in commands:
    subprocess.Popen(command)

print(f"[!] Results saved with scrape_id: {str(scrape_id)}.")