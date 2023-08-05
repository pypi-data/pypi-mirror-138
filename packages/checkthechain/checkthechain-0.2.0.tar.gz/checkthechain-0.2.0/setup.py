import setuptools

setuptools.setup(
    name='checkthechain',
    version='0.2.0',
    packages=setuptools.find_packages("./src"),
    package_dir={'': 'src'},
    install_requires=[
        #
        # data science
        'matplotlib',
        'numpy',
        'pandas',
        'pandas-stubs',
        #
        # data dependencies
        'aiohttp',
        'aiofiles',
        'pyyaml',
        'toml',
        #
        # tool suite
        'toolcache',
        'toolcli',
        'toolconf',
        'toolplot',
        'toolstr',
        'tooltable',
        'tooltime',
        #
        # EVM dependencies
        'pysha3',  # for keccak()
        'eth_abi',  # for encode_single()/decode_single()
        'eth_utils',  # for collapse_if_tuple()
        'rlp',  # for create2 address computation
    ],
    extras_require={
        'dev': [
            'pytest',
            'pytest-asyncio',
        ],
    },
    scripts=[
        './scripts/ctc',
    ]
)

