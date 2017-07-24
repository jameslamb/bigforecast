# Set bigforecast home directory
if [[ ! -d "$BIGFORECAST_HOME" ]]; then
    export BIGFORECAST_HOME="~/bigforecast"
    echo 'export BIGFORECAST_HOME="~/bigforecast"' >> ~/.bashrc
fi
