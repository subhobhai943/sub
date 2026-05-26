.PHONY: install uninstall build clean

install:
	@echo "Installing sub..."
	cp src/sub.py /usr/local/bin/sub
	chmod +x /usr/local/bin/sub
	@echo "Done. Run: sub help"

uninstall:
	@echo "Uninstalling sub..."
	rm -f /usr/local/bin/sub
	@echo "sub removed."

build:
	@echo "Building .deb package..."
	@which fpm || (echo "Install fpm first: gem install fpm" && exit 1)
	fpm -s dir -t deb \
		-n sub \
		-v 1.0.0 \
		--description "sub - hacking & utility CLI by subhobhai943" \
		--maintainer "Subhobhai Sarkar <subhobhai943@users.noreply.github.com>" \
		--url "https://github.com/subhobhai943/sub" \
		--depends python3 \
		--category utils \
		--deb-recommends nmap \
		--deb-recommends whois \
		--deb-recommends dnsutils \
		src/sub.py=/usr/local/bin/sub
	@echo "Build complete: sub_1.0.0_all.deb"

clean:
	rm -f *.deb
