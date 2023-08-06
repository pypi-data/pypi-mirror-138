from pip import main
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

# Есть много элементов конфигурации, некоторые из них не нужны, обратитесь к официальному документу https://packaging.python.org/guides/distributing-packages-using-setuptools/
setuptools.setup(
    name="neofti_ticsummary", # Имя проекта, который будет установлен через pip install hs_rpc в будущем и не может быть повторен с другими проектами, иначе загрузка не удастся
    version="0.0.13", # Номер версии проекта, решайте сами
    author="DmitryKorovkin", # Автор
    author_email="d.korovkin69@gmail.com", # email
    description="TIC data viewer",  # Описание Проекта
    long_description=long_description, # Загружаем содержимое read_me
    long_description_content_type="text/markdown", # Тип текста описания
    url="",  # Адрес проекта, например адрес github или gitlib
    packages= ['ticsummary'], #setuptools.find_packages(''),  # Эта функция может помочь вам найти все файлы в пакете, вы можете указать вручную
    entry_points={
        'console_scripts': [
            'ticsummary=ticsummary.__main__:main' # or any specific function you would like
        ]
    },
    classifiers=[  
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ], # Этот пакет совместим только с Python 3, под лицензией MIT, и не имеет ничего общего с операционной системой. Вы всегда должны включать по крайней мере версию Python, используемую вашим пакетом, лицензию, доступную для пакета, и операционную систему, которую ваш пакет будет использовать. Полный список классификаторов см. На https://pypi.org/classifiers/.
    install_requires=[
        'pyqtgraph',
        'numpy',
        'pyqt6',
        'wrapt_timeout_decorator',
        'mysql',
        'mysql-connector-python'
    ], # Зависимости проекта, вы также можете указать зависимую версию
)