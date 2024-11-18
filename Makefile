IMAGE_TAG=whatsapp-leads-poc
CONTAINER_NAME=whatsapp-leads-bot

docker-build:
	docker build -t $(IMAGE_TAG) .

docker-run:
	@echo "docker run --rm --name $(CONTAINER_NAME)"
	@echo "\t-e TWILIO_ACCOUNT_SID=$(TWILIO_ACCOUNT_SID)"
	@echo "\t-e TWILIO_AUTH_TOKEN=XXXXXXX"
	@echo "\t-e WHATSAPP_BOT_NO=XXXXXXXX"
	@echo "\t-v $(PWD):/usr/src/app"
	@echo "\t-p 5000:5000"
	@echo "\t$(IMAGE_TAG)"
	@docker run --rm --name $(CONTAINER_NAME) \
		-e TWILIO_ACCOUNT_SID=$(TWILIO_ACCOUNT_SID) \
		-e TWILIO_AUTH_TOKEN=$(TWILIO_AUTH_TOKEN) \
		-e WHATSAPP_BOT_NO=$(WHATSAPP_BOT_NO) \
		-v $(PWD):/usr/src/app \
		-p 5000:5000 \
		$(IMAGE_TAG)
