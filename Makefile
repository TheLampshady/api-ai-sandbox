
push:
	git push -u origin master

deploy:
	appcfg.py -A huge-echo update .

deploy_echo:
	appcfg.py -A huge-echo --module=echo update echo.yaml

deploy_dispatch:
	appcfg.py -A huge-echo update_dispatch .
