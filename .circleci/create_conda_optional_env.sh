#!/usr/bin/env bash

if [ ! -d $HOME/miniconda/envs/circle_optional ]; then
    # Download miniconda
    if [ "$PYTHON_VERSION" = "2.7" ]; then
        wget http://repo.continuum.io/miniconda/Miniconda2-latest-Linux-x86_64.sh -O miniconda.sh
    else
        wget http://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh
    fi

    chmod +x miniconda.sh

    # Install miniconda
    ./miniconda.sh -b -p $HOME/miniconda

    # Create environment
    # PYTHON_VERSION=2.7 or 3.5
    $HOME/miniconda/bin/conda create -n circle_optional --yes python=$PYTHON_VERSION

    # Install orca into environment
    $HOME/miniconda/bin/conda install --yes -n circle_optional -c plotly plotly-orca==1.3.1

    # Install additional dependencies
    $HOME/miniconda/bin/conda activate -n circle_optional
    cd packages/python/
    $HOME/miniconda/bin/python -m pip install -r ./plotly/test_requirements/requirements_38_optional.txt
fi
