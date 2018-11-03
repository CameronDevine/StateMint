.PHONY: version tutorial

define prog
from urllib import quote
with open('web/HTML/tutorial/tutorial.md') as f: text = f.read()
chunks = text.split('$$')
chunks = ['![$${}$$](http://latex.codecogs.com/svg.latex?{})'.format(eqn, quote(eqn)) if i % 2 == 1 else chunks[i].replace('](tutorial/', '](HTML/tutorial/') for i, eqn in enumerate(chunks)]
with open('tutorial.md', 'w') as f: f.write(''.join(chunks))
endef
export prog

tutorial:
	echo $$prog
	python -c "import os;exec(os.environ['prog'])"

version:
	if [ "$(old)" ] && [ "$(new)" ] && [ "$(message)" ]; then \
		echo "$(old)->$(new)"; \
		for f in $$(git ls-tree -r --name-only HEAD); do \
			grep -q -F "$(old)" "$$f"; \
			if [ $$? -eq 0 ]; then \
				echo $$f; \
				sed -i -e "s/$(old)/$(new)/g" $$f; \
				git add $$f; \
			fi; \
		done; \
		git commit -m "rolled the version number to $(new)"; \
		git tag -a "$(new)" -m "$(message)"; \
		git push; \
		git push origin "$(new)"; \
		$(MAKE) -C python; \
		$(MAKE) -C installer; \
		$(MAKE) -C HTML; \
	else \
		echo "please supply old and new version numbers along with a release message:"; \
		echo "make version old=<old version> new=<new version> message=<release message>"; \
	fi;
