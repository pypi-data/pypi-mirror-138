from setuptools import setup
from jaye.settings import *

setup(
    name ='jaye',
    version= VERSION,
    license = 'jaye',
    author = 'jaye_official',
    author_email = 'help@jayecorp.com',
    description = 'jaye에서 가공한 퀀트 데이터와 분석자료를 제공하는 패키지입니다.',
    packages = ['jaye']
)