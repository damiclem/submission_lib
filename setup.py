import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
        name='submission_lib',
        version='0.1.0',
        author='Alessio Del Conte',
        author_email='ale.delconte96@gmail.com',
        description='DRMAA interface for slurm/SGE @ biocomputingUp lab',
        long_description=long_description,
        long_description_content_type="text/markdown",
        url='https://github.com/damiclem/submission_lib/',
        license='MIT',
        packages=[
            'submission_lib',
            'submission_lib.slurm',
            'submission_lib.sge'
        ],
        package_dir={
            'submission_lib': '.'
        },
        install_requires=['requests', 'drmaa']
)
