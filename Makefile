.PHONY: test
test:
	@python -m pytest -s

.PHONY: deploy
deploy:
	@git push heroku master

