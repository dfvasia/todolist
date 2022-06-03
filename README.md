0. # Настройки todolist.settings

# подключение postgresql (подключаем коробку)    
    DATABASES = { 
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'todolist',
            'USER': 'postgres',
            'PASSWORD': 'postgres123',
            'HOST': 'localhost',
            'PORT': '5432',
        }

    INSTALLED_APPS = [
        'rest_framework', # подключение DRF базовый
        'rest_framework_simplejwt', # подключение JWT token
        'rest_framework_simplejwt.token_blacklist', # блокирование уже исп. или скомпрометированных токенов
        'djoser',
        'corsheaders', # включение CORS
        'drf_spectacular' # подключение документации
        ]
    MIDDLEWARE_CLASSES = (
        ...
        'corsheaders.middleware.CorsMiddleware',
        'django.middleware.common.CommonMiddleware',
        ...
        )

    REST_FRAMEWORK = {
        "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
        "PAGE_SIZE": 10,
        "DEFAULT_AUTHENTICATION_CLASSES": [
            "rest_framework_simplejwt.authentication.JWTAuthentication",
        ],
        "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    }
    SIMPLE_JWT = {
        'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),  # время жизни ACCESS
        'REFRESH_TOKEN_LIFETIME': timedelta(days=10), # время жизни REFRESH
        'ROTATE_REFRESH_TOKENS': True, #  после измение новое время и новый REFRESH
        'BLACKLIST_AFTER_ROTATION': True # Блокировать исп. TOKEN
    }

    SPECTACULAR_SETTINGS ={
        "TITLE": "Курсовая работа №6 API",
        "DESCRIPTION": "Описание API",
        "VERSION": "0.0.1",
       }

    CORS_ORIGIN_ALLOW_ALL = True  # если включено то параметры CORS_ORIGIN_WHITELIST и CORS_ORIGIN_REGEX_WHITELIST НЕ НУЖНЫ!!!
    CORS_ALLOW_CREDENTIALS = True
    CORS_ORIGIN_WHITELIST = (
        'localhost:3030',
        'localhost:8000',
        '127.0.0.1:8000'
        )
    CORS_ORIGIN_REGEX_WHITELIST = (
        'localhost:3030',
        )

    DJOSER = {
    'PASSWORD_RESET_CONFIRM_URL': '#/password/reset/confirm/{uid}/{token}',
    'USERNAME_RESET_CONFIRM_URL': '#/username/reset/confirm/{uid}/{token}',
    'ACTIVATION_URL': '#/activate/{uid}/{token}',
    'SEND_ACTIVATION_EMAIL': True,
    'SERIALIZERS': {},
}

    AUTH_USER_MODEL = 'authentication.User'

1. # Подключение базы данных Postgres.
 создание докер контейнера с заданными параметрами
 docker run --name todolist -e POSTGRES_DB=todolist -e POSTGRES_PASSWORD=postgres123 -p 5432:5432 -d postgres
 # Настройки todolist.settings
 # подключение postgresql (подключаем коробку) 
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'todolist',
            'USER': 'postgres',
            'PASSWORD': 'postgres123',
            'HOST': 'localhost',
            'PORT': '5432',
        }

2. # Подключение DRF(Django REST Framework).
 poetry add djangorestframework
 poetry add djangorestframework-simplejwt
   # Настройки todolist.settings

    INSTALLED_APPS = [
        ...
        'rest_framework', # подключение DRF базовый
        'rest_framework_simplejwt', # подключение JWT token
        'rest_framework_simplejwt.token_blacklist', # блокирование уже исп. или скомпрометированных токенов
        ...
        ]
    REST_FRAMEWORK = {
        "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
        "PAGE_SIZE": 10, # Количество на 1 стр.
        "DEFAULT_AUTHENTICATION_CLASSES": [
            "rest_framework_simplejwt.authentication.JWTAuthentication", # Метод авторизации
        ],
    }
    SIMPLE_JWT = { # Настройки  JWT токена
        'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),  # время жизни ACCESS
        'REFRESH_TOKEN_LIFETIME': timedelta(days=10), # время жизни REFRESH
        'ROTATE_REFRESH_TOKENS': True, #  после измение новое время и новый REFRESH
        'BLACKLIST_AFTER_ROTATION': True # Блокировать исп. TOKEN
    }

 # Настройки todolist.urls
`  path('api-auth/', include('rest_framework.urls')) # urls с авторизацией`

3. # Подключение CORS headers.
 poetry add django-cors-headers
  # Настройки todolist.settings

    INSTALLED_APPS = [
        ...
        'corsheaders', # включение CORS
        ...
        ]

    MIDDLEWARE_CLASSES = (
       ...
       'corsheaders.middleware.CorsMiddleware',
       'django.middleware.common.CommonMiddleware',
       ...
       )

    CORS_ORIGIN_ALLOW_ALL = True # если включено то параметры CORS_ORIGIN_WHITELIST и CORS_ORIGIN_REGEX_WHITELIST НЕ НУЖНЫ!!!
    CORS_ALLOW_CREDENTIALS = True
    CORS_ORIGIN_WHITELIST = (
        'localhost:3030',
        )
    CORS_ORIGIN_REGEX_WHITELIST = (
        'localhost:3030',
        )
 

4. # Подключение Swagger.
 авто документация проекта django
 poetry add drf-spectacular
  # Настройки todolist.settings
 
    INSTALLED_APPS = [
        ...
        'drf_spectacular', # включение автодокументации 
        ]
    REST_FRAMEWORK = {
    ...
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.olpenapi.AutoShema", # схема по умолчанию
    }
    SPECTACULAR_SETTINGS ={ 
        "TITLE": "список дел",
        "DESCRIPTION": "Описание API",
        "VERSION": "0.0.1",
       }
 # Настройки todolist.urls
`  path('api/schema/', SpectacularAPIView.as_view(), name='schema') # urls c JSON `
`  path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema')) # графический интерфкейс  `

5. # Подключение Djoser.
 # Для настроек пользователей системы
 poetry add djoser
 
 # Настройки todolist.settings
    INSTALLED_APPS = [
        ...
        'djoser',
        ...
        ]
    DJOSER = {
        'PASSWORD_RESET_CONFIRM_URL': '#/password/reset/confirm/{uid}/{token}',
        'USERNAME_RESET_CONFIRM_URL': '#/username/reset/confirm/{uid}/{token}',
        'ACTIVATION_URL': '#/activate/{uid}/{token}',
        'SEND_ACTIVATION_EMAIL': True,
        'SERIALIZERS': {
        'user_create': 'users.serializers.UserRegistrationSerializer'
         },
        'LOGIN_FIELD': 'email'
        }