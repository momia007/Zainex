# Imagen oficial de MySQL
FROM mysql:8.0

# Establece variables de entorno para inicializar la base
ENV MYSQL_DATABASE=zainex_scout \
    MYSQL_USER=scout_user \
    MYSQL_PASSWORD=*02chi08* \
    MYSQL_ROOT_PASSWORD=aGhe/u4i

# Exponer el puerto MySQL
EXPOSE 3306

# Volumen para persistencia de datos
VOLUME ["/var/lib/mysql"]

# Copia el script SQL para inicializar la base de datos
COPY estructura.sql /docker-entrypoint-initdb.d/
