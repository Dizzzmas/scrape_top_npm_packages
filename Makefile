.PHONY: build run

build:
	docker build --network="host" -t npm_scraper .



# Download binaries for local dev
bin:
	mkdir -p bin

	# Get chromedriver
	curl -SL https://chromedriver.storage.googleapis.com/2.43/chromedriver_mac64.zip > chromedriver.zip
	unzip chromedriver.zip -d bin/

	# Get Headless-chrome
	curl -SL https://github.com/adieuadieu/serverless-chrome/releases/download/v1.0.0-55/stable-headless-chromium-amazonlinux-2017-03.zip > headless-chromium.zip
	unzip headless-chromium.zip -d bin/

	# Clean
	rm headless-chromium.zip chromedriver.zip

run: build
	docker run -it --network="host" -v /dev/shm:/dev/shm npm_scraper

clean:
	rm -rf bin
