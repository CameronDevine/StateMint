.PHONY: version tutorial

# Copy the web tutorial to the repository root, where GitHub renders its $...$
# and $$...$$ math natively, pointing its figure paths at web/HTML/tutorial/.
define prog
with open('web/HTML/tutorial/tutorial.md') as f: text = f.read()
note = '<!-- Generated from web/HTML/tutorial/tutorial.md by `make tutorial`; edit that file instead. -->\n\n'
with open('tutorial.md', 'w') as f: f.write(note + text.replace('](tutorial/', '](web/HTML/tutorial/'))
endef
export prog

tutorial:
	python3 -c "import os;exec(os.environ['prog'])"

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
