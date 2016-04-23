#!/bin/sh
python3 /var/www/html/Vegarails/support/RSS\ downloader/RSSGet.py
python3 /var/www/html/Vegarails/support/interface.py
python3 /var/www/html/Vegarails/support/importer.py
