install:
	pip3 install pypugjs

build:
	pypugjs index.pug index.html
	pypugjs about/index.pug about/index.html
	python3 _sitemap.py
