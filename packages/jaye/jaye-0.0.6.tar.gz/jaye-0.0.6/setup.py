from setuptools import setup

setup(
    name ='jaye',
    version= '0.0.6',
    license = 'jaye',
    author = 'jaye_official',
    author_email = 'help@jayecorp.com',
    description = 'jaye에서 가공한 퀀트 데이터와 분석자료를 제공하는 패키지입니다.',
    packages = ['jaye'],
    install_requires =[
        'numpy==1.22.0',
        'pandas==1.3.5',
        'requests',
        'rich'
    ]
)