conda-env:
	# Create conda environment or update existing
	if ! (conda env list | grep -q "bigforecast"); then \
		echo "bigforecast conda environment doesn't exist. Creating..." && \
		conda env create -f python/bigforecast.yml; \
	else \
	    conda env update -q -n bigforecast -f python/bigforecast.yml; \
	fi

clean_python_cache:
	@echo "Removing Python cache directories..." && \
	rm -rf python/bigforecast.egg-info && \
	rm -rf python/bigforecast/__pycache__ && \
	echo "Done."

install_python:
	# Creat or update conda env
	# Install bigforecast Python package into bigforecast env
	make clean_python_cache && \
	make conda-env && \
	echo "Installing bigforecast package..." && \
	cd python && \
	pip install -e . && \
	source activate bigforecast && \
	python setup.py install && \
	source deactivate && \
	cd .. && \
	make clean_python_cache && \
	echo "Installed bigforecast."
	
make docs_python:
	# Create sphinx rst files for every package and subpackage
	cd python && \
	sphinx-apidoc -f -e -o docs bigforecast && \
	cd docs && \
	make html && \
	cp -R _build/html/* ../../docs/