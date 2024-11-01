.SUFFIXES: .md.erb

default:
	@for f in `find . -name '*.md.erb'`; do make $${f%.erb}; done

%: %.erb
	erb $^ > $@
