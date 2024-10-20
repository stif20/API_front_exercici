# Proyecto-Actividad2

## Apartado 1

### Para empezar con esta nueva práctica de FastAPI lo que haremos es hacer un fork del repositorio de atalens1 

![image](https://github.com/user-attachments/assets/ba829c2c-0042-4b11-87a9-1a86fb3a05b9)

### Una vez hemos hecho el fork, clonaremos este repositorio nuevo para poderlo tener en local

![image](https://github.com/user-attachments/assets/9ffcd41b-9d10-4340-ab47-6993d9d87f06)

### Una vez clonado lo que hacemos es editar el archivo script.js donde llamaremos al endpoint de la API utilizando fetch

![image](https://github.com/user-attachments/assets/24e33398-1d41-47ef-b315-9e6be00e2f89)

### Una vez hehcho esto añadiremos todos los campos que se nos piden como puede ser Cicle, Curs, Grup y DescAula los cuales son variables que se iran añadiendo a una tabla en forma de td

![image](https://github.com/user-attachments/assets/66468839-470a-488a-9833-7b3b8acf44f0)

### Ahora lo que hare es crear una nueva carpeta llamada API al mismo nivel que se encuentra la carpeta front

![image](https://github.com/user-attachments/assets/edf7457e-9466-4c71-830c-5c841f50987e)

### Al haber realizado estos cambios tengo que adaptar la query del endpoint para que solo se seleccionen los campos que se nos piden 

![image](https://github.com/user-attachments/assets/ddbc756f-0053-411d-8ac1-9dc8f04d4314)

### A consecuencia del cambio anterior tengo que adaptar el alumne_schema para que solo esten los campos deseados y asi poder realizar un fetch

![image](https://github.com/user-attachments/assets/7adf4663-4118-4541-866d-ee21664f3e82)

### Ahora en el main.py tengo que añadir el import de CORSMiddleware

![image](https://github.com/user-attachments/assets/aceccf8a-4753-469f-9b23-656b0aea318b)

### Y posteriormente añadire estas nuevas lineas justo debajo del app = FastAPI()

![image](https://github.com/user-attachments/assets/10bbcb95-ea84-4cae-9f87-2035a7851adb)

### Una vez añadidas estas lineas tengo que hacer que el endpoint que me retorna la lista que en mi caso es alumne/listAll incorpore “response_model=List[tablaAlumne]”

![image](https://github.com/user-attachments/assets/ff6762c3-500b-4ee5-a27f-8dd5a2eaec15)

### Al realizar el cambio anterior me obliga a crear una nueva class llamada tablaAlumne la cual contiene los campos que nos interesan

![image](https://github.com/user-attachments/assets/9d810fb4-95e5-4ec9-bd81-e8a73f2077af)

### Una vez hecho todos estos cambios lo que hago es abrir el archivo index.html en el cual solo veremois un boton en el cual dice Ver Alumnos

![image](https://github.com/user-attachments/assets/146b3906-9135-4301-8afc-7cb6d68f87da)

### Al darle a un boton se nos cargan todos los alumnos que tenemos en nuestra base de datos en una tabla

![image](https://github.com/user-attachments/assets/eaaadca7-a289-44c2-86eb-037ecde8753c)

## Apartado 2

### ?orderby= (str) 

  ### Ruta

Orderby=asc

![image](https://github.com/user-attachments/assets/81c238f5-931c-4253-bf6d-80f070179001)

Orderby=desc

![image](https://github.com/user-attachments/assets/ee356d31-9164-4262-85db-d0035490279b)

  ### Prueba

Orderby=asc

![image](https://github.com/user-attachments/assets/c554b529-6e2f-48fe-a563-9cdb3341e806)

Orderby=desc

![image](https://github.com/user-attachments/assets/86b58015-07df-4979-af03-8b674460b3aa)


### ?contain=(str)

 ### Ruta

 ![image](https://github.com/user-attachments/assets/d25469f4-9eca-4300-b9cd-ac41a714d838)

 ![image](https://github.com/user-attachments/assets/17c1e777-8765-4893-b0e4-83d5303fa875)

 ### Prueba

![image](https://github.com/user-attachments/assets/3f43f1b3-23a7-4adc-aa77-4b5c17fd68bc)

![image](https://github.com/user-attachments/assets/3993f0b6-3273-4554-861c-33b2b56f790a)

### ?skip= (int)&limit=(int)

 ### Ruta

 ![image](https://github.com/user-attachments/assets/cab22063-9d59-45a2-93eb-4125562788f3)

 ### Prueba

Para que se entienda en esta query lo que hago es saltar los dos primeros alumnos y limitarlo a que salgan un total de 10

![image](https://github.com/user-attachments/assets/f1db71dc-49f6-412f-860f-15adfde66232)

## Apartado 3 

En este último apartado lo que vamos a hacer es crear un nuevo endpoint con el cual vamos a hacer que acepte un archivo csv con tal de poder cargar masivamente datos a la base de datos

  ### Ruta

![image](https://github.com/user-attachments/assets/3bcac384-899e-47cd-b444-0a22417f8bd4)


  ### Prueba

Para probar de que este endpoint funcione correctamente y cargue los datos atraves del archivo csv, lo que hago es ir a /docs en el cual seleccionare este nuevo endpoint

![image](https://github.com/user-attachments/assets/6e4c64a8-3ae3-4711-9d7c-755a64a3ae42)

![image](https://github.com/user-attachments/assets/80bdd670-bb9c-46a5-8143-00d5d5e1d049)

Una vez lo selecciono le doy a Try it out

![image](https://github.com/user-attachments/assets/ffc201ea-2a8b-4a7f-a44e-e2fdf0d64c16)

Y en el apartado de file le doy a seleccionar archivo el cual tendra que tener la extensión .csv, en mi caso lo he creado yo mismo

![image](https://github.com/user-attachments/assets/ba074f53-bb54-4432-950d-6352a099ca70)

![image](https://github.com/user-attachments/assets/94d19846-3650-4ee7-854c-bfd2eca88107)

![image](https://github.com/user-attachments/assets/bb3464a2-7c7e-4d2d-b98c-61209ffac2e9)

Una vez sunbido el archivo le damos a Execute

![image](https://github.com/user-attachments/assets/5dea6652-fb11-4b87-8893-c2508b2e4d09)

Una vez ejecutado veremos que se nos devuelve el mensaje de Carga masiva completada, que esto quiere decir que a sido un exito

![image](https://github.com/user-attachments/assets/abd921f8-63f3-49ef-b92e-bcae037f8fa6)

Hasta podemos comprobarlo en HeidiSQL en el cual veremos que tenemos mas registros

![image](https://github.com/user-attachments/assets/de778a15-119c-4971-8402-c26b549c1c3a)






