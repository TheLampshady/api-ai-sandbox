
push:
	git push -u origin master

deploy:
	appcfg.py -A huge-echo update .

deploy_echo:
	appcfg.py -A huge-echo --module=echo update echo.yaml

deploy_dispatch:
	appcfg.py -A huge-echo update_dispatch .

install-libs:
	# pip install everything in requirements.txt to libs
	if [ -f lib_requirements.txt ]; then \
		if [ -f ~/.pydistutils.cfg.backup ]; then \
			cp ~/.pydistutils.cfg.backup ~/.pydistutils.cfg; \
		fi; \
		pip install -t libs -q -r lib_requirements.txt; \
		if [ -f ~/.pydistutils.cfg ]; then \
			rm ~/.pydistutils.cfg; \
		fi; \
	fi;


