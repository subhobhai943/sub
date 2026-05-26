.PHONY: install build-kotlin build-java clean

install:
	cp src/python/sub.py /usr/local/bin/sub
	chmod +x /usr/local/bin/sub
	@echo "[+] sub installed at /usr/local/bin/sub"

build-kotlin:
	kotlinc src/kotlin/Sub.kt -include-runtime -d sub-kotlin.jar
	@echo "[+] Kotlin JAR: sub-kotlin.jar"

build-java:
	mkdir -p out
	javac src/java/Sub.java -d out/
	cd out && jar cfe ../sub-java.jar Sub .
	@echo "[+] Java JAR: sub-java.jar"

clean:
	rm -f sub-kotlin.jar sub-java.jar *.deb
	rm -rf out/
