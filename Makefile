.PHONY: tutorial

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
