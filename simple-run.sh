scrapy crawl dvsvc -o $1 2>&1 | grep --color -E "DVSVCPage|DVSVCPageSet|Mean lscore|$"