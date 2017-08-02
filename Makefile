conda-env:
	# Create conda environment or update existing
	if ! (conda env list | grep -q "bigforecast"); then \
		echo "bigforecast conda environment doesn't exist. Creating..." && \
		conda env create -f python/bigforecast.yml; \
	else \
	    conda env update -q -n bigforecast -f python/bigforecast.yml; \
	fi
	
install_python:
	# Creat or update conda env
	# Install bigforecast Python package into bigforecast env
	make conda-env && \
	source activate bigforecast && \
	echo "Installing bigforecast package..." && \
	python python/setup.py install && \
	echo "Installed bigforecast."
	
make docs_python:
	# Create sphinx rst files for every package and subpackage
	cd python && \
	sphinx-apidoc -f -e -o docs bigforecast && \
	cd docs && \
	make html && \
	cp -R _build/html/* ../../docs/