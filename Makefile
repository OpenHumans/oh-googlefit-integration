.PHONY: test
test:
	@python -m pytest -s

.PHONY: deploy
deploy:
	@git push heroku master

.PHONY: force_deploy
force_deploy:
	@git push -f heroku master

.PHONY: update_data
update_data:
	@heroku run python manage.py update_data


