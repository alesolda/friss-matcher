clean:
	rm -fr *.egg-info
	rm -fr .eggs
	rm -fr .pytest_cache
	rm -fr .coverage
	rm -fr build
	rm -fr dist
	find . -name "*.pyc" -prune -exec rm -fr {} \;
	find . -name "__pycache__" -prune -exec rm -fr {} \;
	find . -name "*.egg-info" -prune -exec rm -fr {} \;
