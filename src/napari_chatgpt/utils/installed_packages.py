import traceback

_image_processing_analysis_packages = \
    ['OpenCV', 'Pillow', 'PyWavelets', 'scipy', 'networkx', 'tifffile',
     'scikit-image', 'napari', 'psygnal', 'numpy', 'imagecodecs', 'dask',
     'dask-core',
     'brotlipy', 'vispy', 'tqdm', 'openai', 'zarr', 'numcodecs', 'blosc',
     'imagecodecs', 'imageio', 'imagesize', 'scikit-image', 'cupy', 'cucim',
     'tensorflow', 'pytorch', 'mahotas', 'SimpleITK', 'matplotlib', 'pgmagick',
     'xarray', 'image', 'magicgui', 'arbol', 'tqdm']


def installed_package_list(clean_up: bool = True,
                           version: bool = True,
                           filter=_image_processing_analysis_packages):
    package_list = pip_list(version=version) + conda_list(version=version)

    if clean_up:
        package_list = [pkg for pkg in package_list if not 'aws-' in pkg]
        package_list = [pkg for pkg in package_list if not 'lib' in pkg]

    if filter:
        package_list = [pkg for pkg in package_list if
                        any(f in pkg for f in filter)]

    # Remove duplicates in list:
    package_list = list(set(package_list))

    return package_list


def pip_list(version: bool = False):
    try:
        import importlib.metadata as metadata

        # Get a list of installed packages
        if version:
            package_list = [f"{pkg.metadata['name']}=={pkg.metadata['version']}"
                            for pkg in metadata.distributions()]
        else:
            package_list = [pkg.metadata['name'] for pkg in
                            metadata.distributions()]

        return package_list

    except Exception as e:
        print(traceback.format_exc())
        return []


def conda_list(version: bool = False):
    try:
        import subprocess

        # Run the conda command to get a list of installed packages
        output = subprocess.check_output(['conda', 'list']).decode(
            'utf-8').strip()

        # Split the output into lines and print the package names
        if version:
            package_list = [f"{line.split()[0]}=={line.split()[1]}" for line in
                            output.split('\n') if not line.startswith('#')]
        else:
            package_list = [line.split()[0] for line in output.split('\n') if
                            not line.startswith('#')]

        return package_list

    except Exception as e:
        print(traceback.format_exc())
        return []
