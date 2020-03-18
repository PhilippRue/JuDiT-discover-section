
# JuDiT Database visualizer

This app visualizes the contents of the JuDiT database of impurities embedded into a topological insulator.
It starts an `bokeh server` which hosts the JuDiT web interface on `http://localhost:5006/judit/judit_website_main`.


### Installation

```
git clone https://github.com/PhilippRue/JuDiT-discover-section.git
cd JuDiT-discover-section
pip install -e judit-app   # install python dependencies
```

### Running the app

```
BOKEH_PREFIX="/judit" ./serve-app.sh   # run app
```

Note: Setting `BOKEH_PREFIX="/judit"` is needed so that the links that open the detail pages work properly.
This can also be done by setting the environment variable as it is done in the `Dockerfile`.

### Running the app in a docker container

In the `JuDiT-discover-section` directory run
```
docker-compose build
docker-compose up
```
