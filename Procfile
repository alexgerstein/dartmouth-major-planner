web: gunicorn app:app
init: python db_create.py && python scrapers/scrape_all.py
upgrade: python db_upgrade.py && python scrapers/scrape_all.py
edit: python db_upgrade.py && python scrapers/scrape_edit.py
delete: python db_trash.py