conda_dev:
	conda env remove -n card_rec_env
	conda env create -f conda.yaml

build:
	python setup.py sdist bdist_wheel

deploy:
	twine upload dist/*

clean:
	rm -rf build dist *.egg-info
	rm -rf .pytest_cache