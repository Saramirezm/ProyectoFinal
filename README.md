# ProyectoFinal
El código de encarga de analizar los sentimientos que se presentan en los tweets de una base de datos sobre algún tema específico dado por un query.

Es bastante útil tener de manera visual un entendimiento de lo que las personas opinan respecto a un tema reciente, de esta manera se puede analizar si hubo algún suceso de relevancia que influya en el tema tomado. 

En el código de encuentra el analisis hecho por la librería nltk.sentiment.vadernltk.sentiment.vader de Python. Con esta obtenemos un valor numérico según el sentimiento que exprese el tweet, 0 para negativo, 1 para neutro y 2 para positivo, a partir de estos valores tenemos la posibilidad de hacer graficas que son una ayuda visual para entender estos análisis que el programa hace. 

Adicionalmente dado que se hace uso de información de la aplicación twitter, es indispensable solicitar credenciales de su api para que sea posible extraer la información necesaria y que así mismo fluya el código de la manera correcta.
