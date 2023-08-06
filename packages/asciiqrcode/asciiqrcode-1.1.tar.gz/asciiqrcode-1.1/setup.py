from distutils.core import setup

homepage = "https://github.com/MasterAge/asciiqrcode"

setup(
  name='asciiqrcode',
  packages=['asciiqrcode'],
  version='1.1',
  license='MIT',
  description='A library for processing ASCII representations of QR Codes.',
  author='Adrian Seddon',
  url=homepage,
  download_url='https://github.com/MasterAge/asciiqrcode/releases/download/v1.0/asciiqrcode-1.0.tar.gz',
  keywords=['ASCII', 'QR', 'QRCODE', 'CTF', 'MISC'],
  scripts=['asciiqrcode/asciiqrcode.py'],
  install_requires=[
    'pyzbar',
    'pillow',
  ],
  classifiers=[
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Topic :: Security',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.6',
  ],
  long_description="See: " + homepage,
)
