# Instalar los paquetes necesarios
install.packages("DBI")
install.packages("RMySQL")


# Cargar los paquetes necesarios
library(DBI)
library(RMySQL)

# Configurar la conexión
con <- dbConnect(
  RMySQL::MySQL(),
  dbname = "dbcuwi9wwrkrrk",
  host = "34.175.14.63",
  user = "unasv8vnmxzty",
  password = "jkv6fpshdpqv"
)

# Verificar la conexión
if (!is.null(con)) {
  print("Conexión con éxito a la base de datos MySQL")
}


# Verificar la conexión
summary(con)

# Listar tablas disponibles
tablas <- dbListTables(con)
print(tablas)

# Listar campos de la tabla "Pacientes"
campos <- dbListFields(con, "Pacientes")
print(campos)

# Obtener tabla entera
pacientes1<-DBI::dbReadTable(con, 'Pacientes')
print(pacientes1)

# Obtener solo las primeras 10 filas de la tabla "Pacientes"
pacientes2 <- DBI::dbGetQuery(con, "SELECT * FROM Pacientes LIMIT 10")

# Mostrar las primeras filas
print(pacientes2)

# Obtener datos en lotes de 20 en 20 de la tabla "Pacientes“
query  <- DBI::dbSendQuery(con, 'select * from Pacientes')
# Obtener las primeras 20 filas
pacientes3_1 <- DBI::dbFetch(query, n = 20)
print(pacientes3_1)
# Obtener las siguientes 20 filas
pacientes3_2 <- DBI::dbFetch(query, n = 20)
print(pacientes3_2)

# Consulta SQL sencilla
query1 <- "SELECT * FROM Pacientes WHERE Sexo = 'F'"
pacientes_femeninos <- DBI::dbGetQuery(con, query1)
print(pacientes_femeninos)
# Consulta SQL más compleja
query2 <-  "SELECT *, TIMESTAMPDIFF(YEAR, Fecha_Nacimiento, CURDATE()) AS Edad 
FROM Pacientes WHERE TIMESTAMPDIFF(YEAR, Fecha_Nacimiento, CURDATE()) > 40
AND Nombre LIKE 'M%'"
pacientes_mas40<- DBI::dbGetQuery(con, query2)
print(pacientes_mas40)


# Consultas con dplyr
# Instalar paquete
install.packages("dplyr")

# Cargamos la libreria
library(dplyr)

# Filtrar pacientes femeninos
# Obtener tabla entera
pacientes1<-DBI::dbReadTable(con, 'Pacientes')
# Filtrar pacientes femeninos
pacientes_femeninos <- pacientes1 %>%
  filter(Sexo == "F")
print(pacientes_femeninos)

# Filtrar pacientes más de 40 años que comiencen por "M"
pacientes1 <- pacientes1 %>%
  mutate(Fecha_Nacimiento = as.Date(Fecha_Nacimiento, format = "%Y-%m-%d"))

#Calculamos la edad y añadimos columna
pacientes1 <- pacientes1 %>%    mutate(Edad = as.numeric(difftime(Sys.Date(), Fecha_Nacimiento, units = "days")) %/% 365)

# Filtrar pacientes mayores de 40 años cuyo nombre comience con "M"
pacientes_mas40 <- pacientes1 %>%
  filter(Edad > 40, grepl("^M", Nombre))

print(pacientes_mas40)
