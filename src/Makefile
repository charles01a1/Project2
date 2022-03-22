port = 27012
target=		submit
allFiles=      Makefile config.py connection.py main.py utils.py name.basics.tsv title.basics.tsv title.principals.tsv title.ratings.tsv
scpDir=		chengxua@ug05.cs.ualberta.ca:~/291
# ------------------------------------------------------------

tar:
	touch $(target).tar.gz
	mv $(target).tar.gz  x$(target).tar.gz
	tar -cvf $(target).tar $(allFiles)
	gzip $(target).tar

main:
	python3 main.py

db:
	mkdir database
	mongod --port $(port) --dbpath ./database

scp:
	scp $(target).tar.gz $(scpDir)

clean:
	rm -rf database