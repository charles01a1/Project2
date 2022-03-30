port = 27012
target =	submit
allFiles = Makefile config.py connection.py load-json.py main.py shell.py tsv-2-json.py user.py utils.py name.basics.tsv title.basics.tsv title.principals.tsv title.ratings.tsv
submitFiles = Makefile config.py connection.py load-json.py main.py shell.py tsv-2-json.py user.py utils.py
scpDir = chengxua@ug05.cs.ualberta.ca:~/291
localPath = ../database
labPath = database
# ------------------------------------------------------------

test-tar:
	touch $(target).tar.gz
	mv $(target).tar.gz  x$(target).tar.gz
	tar -cvf $(target).tar $(allFiles)
	gzip $(target).tar

submit-tar:
	touch $(target).tgz
	mv $(target).tgz  x$(target).tgz
	tar -cvzf $(target).tgz $(submitFiles)
	gzip $(target).tgz

scp:
	scp $(target).tar.gz $(scpDir)

main:
	python3 main.py $(port)

convert:
	python3 tsv-2-json.py
	
load:
	python3 load-json.py $(port)

local-db:
	mkdir $(localPath)
	mongod --port $(port) --dbpath $(localPath)

lab-db:
	mkdir $(labPath)
	mongod --port $(port) --dbpath $(labPath)
	
clean-local:
	rm -f *.json
	rm -rf $(localPath)

clean-lab:
	rm -f *.json
	rm -rf $(labPath)