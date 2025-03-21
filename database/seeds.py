import sqlite3


def filters():
    conn = sqlite3.connect("recipes.db")
    cur = conn.cursor()
    ingredients = [
        "Harina",
        "Azúcar",
        "Sal",
        "Huevos",
        "Leche",
        "Mantequilla",
        "Aceite de oliva",
        "Levadura",
        "Vainilla",
        "Chocolate",
        "Fresas",
        "Manzanas",
        "Zanahorias",
        "Papas",
        "Cebollas",
        "Tomates",
        "Pollo",
        "Carne molida",
        "Queso",
        "Orégano",
        "Pimienta",
        "Canela",
        "Albahaca",
        "Ajo",
        "Limón",
        "Arroz",
        "Frijoles",
        "Pan",
        "Crema",
        "Champiñones",
        "Espinacas",
        "Perejil",
        "Chile",
        "Apio",
        "Pimientos",
        "Miel",
        "Jengibre",
        "Cilantro",
        "Mostaza",
        "Ketchup",
        "Salsa de soya",
        "Vinagre",
        "Caldo de pollo",
        "Pescado",
        "Camarones",
        "Lentejas",
        "Yogur",
        "Almendras",
        "Nueces",
        "Pasas",
        "Maíz",
        "Avena",
        "Pan integral",
        "Aguacate"
    ]

    diet_types = [
        "Vegetariana",
        "Vegana",
        "Sin gluten",
        "Sin lactosa",
        "Sin trigo",
        "Baja en carbohidratos",
        "Keto (Cetogénica)",
        "Mediterránea",
        "Dieta DASH",
        "Dieta nórdica",
        "Sin azúcar",
        "Baja en sodio",
        "Alta en proteínas",
        "Baja en grasas",
        "Dieta macrobiótica",
        "Dieta carnívora",
        "Sin soja",
        "Sin huevo",
        "Low FODMAP",
        "Whole30",
        "Dieta baja en colesterol",
        "Dieta rica en fibra",
        "Dieta hiperproteica",
        "Dieta para diabéticos",
        "Dieta DASH vegetariana",
        "Dieta rica en calcio",
        "Dieta sin cítricos",
        "Dieta sin fructosa",   
    ]

    difficulty = ["fácil", "medio", "difícil", "profesional"]

    measure_types = [
        "Gramos",
        "Mililitros",
        "Cucharadita",
        "Chucharaditas",
        "Cucharada",
        "Cucharadas",
        "Pizca",
        "Taza",
        "Tazas",
        "Onza",
        "Onzas",
        "Libra",
        "Libras",
        "Pinta",
        "Pintas",
        "Chorrito",
        "Gota",
        "Gotas",
        "Rama",
        "Diente",
        "Dientes",
        "Rodaja",
        "Rodajas",
        "Puñado",
        "Puñados",
        "Manojo",
        "Manojos",
        "Ración",
        "Raciones",
        "Porción",
        "Porciones",
        "Cáscara",
        "Cáscaras",
        "Rebanada",
        "Rebanadas",
        "Unidad",
        "Unidades",
        "Pieza",
        "Piezas",
        "Chorro grande",
        "Vasito",
        "Vasitos",
        "Vaso",
        "Vasos"
        
    ]

    dish_types = ["Entrante", "Plato principal", "Acompañamientos", "Postre", "Bebida"]

    food_groups = [
        "Tapas Calientes",
        "Tapas frías",
        "Canapé",
        "Hojaldres",
        "Empanadillas",
        "Empanadas",
        "Crudités",
        "Carpaccio",
        "Salsas",
        "Encurtidos",
        "Carnes",
        "Aves",
        "Ensaladas",
        "Verduras",
        "Purés",
        "Patatas",
        "Panes",
        "Hojaldres",
        "Pescados",
        "Tartas",
        "Pasteles",
        "Helados",
        "Sorbetes",
        "Flanes y puddings",
        "Galletas",
        "Bizcochos",
        "Frutas",
        "Soufflés",
        "Mariscos",
        "Cócteles",
        "Bebidas refrescantes",
        "Batidos y licuados",
        "Pasta",
        "Arroces",
        "Guisos y potajes",
        "Parrilla o Barbacoa",
        "Platos al horno",
        "Frituras",
        "Platos étnicos"
    ]


    try:
        for ing in ingredients:
            cur.execute("INSERT OR IGNORE INTO ingredients (name) VALUES (?);", (ing.capitalize(), ))

        for diet in diet_types:
            cur.execute("INSERT OR IGNORE INTO diet_type (name) VALUES (?);", (diet.capitalize(), ))

        for d in difficulty:
            cur.execute("INSERT OR IGNORE INTO difficulty (name) VALUES (?);", (d.capitalize(), ))

        for measure in measure_types:
            cur.execute("INSERT OR IGNORE INTO measure_type (name) VALUES (?);", (measure.capitalize(), ))

        for dish in dish_types:
            cur.execute("INSERT OR IGNORE INTO dish_type(name) VALUES (?);", (dish.capitalize(), ))

        for food in food_groups:
            cur.execute("INSERT OR IGNORE INTO food_groups(name) VALUES (?);", (food.capitalize(), ))
        conn.commit()
        return "filters added successfully"
    except Exception as e:
        conn.rollback()
        return f"There was an error adding the data: {e}"
    finally:
        conn.close()
    
    
    
def recipes(recipe):
    conn = sqlite3.connect("recipes.db")
    cur = conn.cursor()
    
    title = recipe[0]
    summary = recipe[1]
    cooking_time = recipe[2]
    approx_price = recipe[3]
    servings = recipe[4]
    instructions = recipe[5]
    difficulty = recipe[6]
    dish_type = recipe[7]
    food_groups = recipe[8]
    ingredients = recipe[9]
    diet_type = recipe[10]
    link = recipe[11]
    license = recipe[12]
    image = recipe[13]
    email = recipe[14]


    try:
        cur.execute("SELECT id FROM difficulty WHERE name = ?", (difficulty.capitalize(), ))
        difficulty_id = cur.fetchone()[0]
        cur.execute("SELECT id FROM dish_type WHERE name = ?", (dish_type.capitalize(), ))
        dish_type_id = cur.fetchone()[0]
        cur.execute("INSERT OR IGNORE INTO recipes (title, summary, cooking_time, approx_price, servings, instructions, difficulty_id, dish_type_id, link, license,image, email) VALUES (?,?,?,?,?,?,?,?,?,?,?,?) ON CONFLICT(title) DO NOTHING",(title, summary, cooking_time, approx_price, servings, instructions, difficulty_id, dish_type_id, link, license, image,email))
        cur.execute("SELECT id FROM recipes where title = (?)", (title, ))
        recipe_id = cur.fetchone()[0]
    
        for r in ingredients:
           
            cur.execute("INSERT INTO measure_type (name) VALUES (?) ON CONFLICT(name) DO NOTHING", (r[1].capitalize(),))
            cur.execute("SELECT id FROM measure_type where name = (?)", (r[1].capitalize(),))
            measure_type_id = cur.fetchone()[0]
            cur.execute("INSERT INTO ingredients (name) VALUES (?) ON CONFLICT(name) DO NOTHING", (r[2].capitalize(),))
            cur.execute("SELECT id FROM ingredients where name = (?)", (r[2].capitalize(),))
            ingredients_id = cur.fetchone()[0]
            cur.execute("INSERT OR IGNORE INTO recipes_ingredients (recipes_id, ingredients_id, measure_type_id, quantity) VALUES (?, ?, ?, ?)", (recipe_id, ingredients_id, measure_type_id, r[0]))

        for dt in diet_type:
            cur.execute("INSERT INTO diet_type (name) VALUES (?) ON CONFLICT(name) DO NOTHING", (dt.capitalize(),))
            cur.execute("SELECT id FROM diet_type where name = (?)", (dt.capitalize(),))
            diet_type_id = cur.fetchone()[0]
            cur.execute("INSERT OR IGNORE INTO recipes_diet_type (recipes_id, diet_type_id) VALUES (?, ?)", (recipe_id, diet_type_id))

        for fg in food_groups:
            cur.execute("INSERT INTO food_groups (name) VALUES (?) ON CONFLICT(name) DO NOTHING", (fg.capitalize(),))
            cur.execute("SELECT id FROM food_groups where name = (?)", (fg.capitalize(),))
            food_groups_id = cur.fetchone()[0]
            cur.execute("INSERT OR IGNORE INTO recipes_food_groups (recipes_id, food_groups_id) VALUES (?, ?)", (recipe_id, food_groups_id))
        conn.commit()
        return f"Recipes added successfully"
    except Exception as e:
        conn.rollback()
        return f"There was an error adding the data: {e}"
    finally:
        conn.close()






recipe_1 = [
    "Huevos Revueltos con Aguacate y Tostada",
    "Una receta saludable y llena de energía, ideal para un desayuno o brunch lleno de sabor y nutrientes. Los huevos revueltos con aguacate son una opción perfecta para comenzar el día de manera ligera pero sustanciosa.",
    10, 4, 2,
    "1. Tostar las rebanadas de pan integral o el pan de tu preferencia.\n"
    "2. Pelar y cortar el aguacate en láminas finas o triturarlo con un tenedor hasta obtener un puré cremoso.\n"
    "3. Batir los huevos con un tenedor en un recipiente, añadir una pizca de sal, pimienta y, si deseas, un chorrito de leche para hacerlos más suaves (opcional).\n"
    "4. Calentar una sartén antiadherente con una cucharadita de aceite de oliva a fuego medio.\n"
    "5. Verter los huevos batidos en la sartén y, con una espátula, revolver suavemente hasta que se cocinen pero mantengan una textura cremosa y esponjosa.\n"
    "6. Colocar las tostadas en el plato, agregar los huevos revueltos encima y cubrir con el aguacate.\n"
    "7. Opcionalmente, espolvorear con un poco de chile en polvo o añadir unas gotas de limón para un toque extra de sabor.",
    "fácil", "plato principal",
    ["Ensaladas", "Verduras", "Pan", "Desayunos"],
    [[2, "rebanadas",  "Pan integral"],
    [2, "Unidades", "Huevos grandes"],
    [1, "Unidad", "Aguacate maduro"],
    [1, "Pizca", "Sal"],
    [1, "Pizca", "Pimienta negra"],
    [1, "Cucharada", "Aceite de oliva extra virgen"],
    [1, "Cucharadita", "Leche"]],
    ["vegetariana"],
    None, "ChatGPT",
    "images/huevos_revueltos_con_aguacate.png",
    "noemail@email.com"
]

recipe_2 = [
    "Tortilla de Espinacas y Queso",
    "Una tortilla ligera y nutritiva, ideal para un desayuno o cena rápida. Con espinacas frescas y queso, es una opción deliciosa y saludable.",
    15, 4, 2,
    "1. Lavar y picar las espinacas.\n"
    "2. Batir los huevos con una pizca de sal y pimienta.\n"
    "3. Calentar una sartén con aceite de oliva y saltear las espinacas hasta que se ablanden ligeramente.\n"
    "4. Verter los huevos batidos sobre las espinacas y añadir el queso rallado.\n"
    "5. Cocinar a fuego medio hasta que la tortilla esté completamente firme.\n"
    "6. Servir caliente, disfrutando de una comida ligera y sabrosa.",
    "fácil", "plato principal",
    ["Verduras", "Lácteos", "Huevos"],
    [[3, "Unidades", "Huevos"],
    [1, "Taza", "Espinacas frescas"],
    [50, "gramos", "Queso rallado"],
    [1, "Cucharada", "Aceite de oliva"],
    [1, "Pizca", "Sal"],
    [1, "Pizca", "Pimienta"]],
    ["vegetariana"],
    None, "ChatGPT",
    "images/tortilla_de_espinacas_y_queso.png",
    "noemail@email.com"
]


recipe_3 = [
    "Ensalada Mediterránea",
    "Una ensalada fresca, vibrante y saludable, cargada de los sabores típicos de la dieta mediterránea. Perfecta como entrante o acompañante en cualquier comida.",
    10, 3, 2,
    "1. Lavar y cortar los tomates, pepino y cebolla en rodajas finas.\n"
    "2. Desmenuzar el queso feta en trozos pequeños o deshacerlo con las manos.\n"
    "3. Mezclar los ingredientes en un bol grande y añadir las aceitunas negras o verdes, según prefieras.\n"
    "4. Aliñar con aceite de oliva extra virgen, vinagre balsámico, orégano, sal y pimienta al gusto.\n"
    "5. Revolver suavemente para que todos los ingredientes se impregnen bien con el aliño.\n"
    "6. Servir fría, como entrada refrescante o acompañamiento de platos principales.",
    "fácil", "Entrante",
    ["Verduras", "Lácteos", "Ensaladas"],
    [[1, "Unidad", "Pepino"],
    [2, "Unidades", "Tomates maduros"],
    [0.5, "Unidad", "Cebolla roja"],
    [50, "gramos", "Queso feta"],
    [10, "Unidades", "Aceitunas"],
    [2, "Cucharadas", "Aceite de oliva extra virgen"],
    [1, "Cucharada", "Vinagre balsámico"],
    [1, "Pizca", "Orégano seco"],
    [1, "Pizca", "Sal"],
    [1, "Pizca", "Pimienta negra"]],
    ["vegetariana"],
    None, "ChatGPT",
    "images/ensalada_mediterranea.png",
    "noemail@email.com"
]

recipe_4 = [
    "Crema de Calabaza",
    "Una sopa suave, cremosa y reconfortante, perfecta para los días fríos. Con un sabor delicado y un toque especiado, esta crema es ideal para disfrutar como entrada o plato principal.",
    25, 5, 4,
    "1. Pelar y cortar la calabaza en trozos medianos.\n"
    "2. Picar finamente la cebolla y el ajo.\n"
    "3. En una olla grande, calentar el aceite de oliva a fuego medio y sofreír la cebolla y el ajo hasta que estén dorados y fragantes.\n"
    "4. Añadir los trozos de calabaza y el caldo de verduras caliente a la olla.\n"
    "5. Cocinar a fuego medio-bajo durante unos 20-25 minutos, hasta que la calabaza esté tierna y se pueda pinchar fácilmente con un tenedor.\n"
    "6. Triturar la mezcla con una batidora de mano o en una licuadora hasta obtener una crema suave y homogénea.\n"
    "7. Volver a poner la crema en la olla y calentar a fuego bajo. Añadir sal, pimienta y una pizca de nuez moscada al gusto. Ajustar la consistencia con más caldo si es necesario.\n"
    "8. Servir caliente, decorada con un chorrito de crema o un toque de aceite de oliva si lo deseas.",
    "medio", "Entrante",
    ["Verduras", "Sopas"],
    [[500, "gramos", "Calabaza"],
    [1, "Unidad", "Cebolla"],
    [1, "Diente", "Ajo"],
    [500, "ml", "Caldo de verduras"],
    [1, "Cucharada", "Aceite de oliva extra virgen"],
    [1, "Pizca", "Sal"],
    [1, "Pizca", "Pimienta negra"],
    [1, "Pizca", "Nuez moscada"]], 
    ["vegetariana"],
    None, "ChatGPT",
    "images/crema_de_calabaza.png",
    "noemail@email.com"
]


recipe_5 = [
    "Tortilla de Patatas",
    "Un clásico de la gastronomía española, sabroso y reconfortante. Perfecta para cualquier comida, ya sea caliente o fría, ideal para un almuerzo, cena o picnic.",
    30, 4, 4,
    "1. Pelar las patatas y cortarlas en rodajas finas, procurando que sean del mismo grosor para una cocción uniforme.\n"
    "2. Picar finamente la cebolla.\n"
    "3. En una sartén grande, calentar abundante aceite de oliva a fuego medio y freír las patatas con la cebolla hasta que estén tiernas pero no doradas, unos 15-20 minutos. Escurrir el exceso de aceite.\n"
    "4. Batir los huevos en un bol grande con una pizca de sal. Añadir las patatas y cebolla escurridas y mezclar bien.\n"
    "5. Calentar una sartén antiadherente con un poco de aceite de oliva a fuego medio. Verter la mezcla de huevos y patatas en la sartén.\n"
    "6. Cocinar durante unos 5-7 minutos hasta que los bordes estén dorados y la parte inferior esté cocida. Para dar la vuelta, cubrir la sartén con un plato y voltear la tortilla con cuidado.\n"
    "7. Cocinar el otro lado durante 3-4 minutos más o hasta que esté dorada y bien cocida por dentro.\n"
    "8. Dejar reposar unos minutos antes de servir, puede servirse tanto caliente como a temperatura ambiente.",
    "fácil", "Plato principal",
    ["Huevos", "Verduras"],
    [[4, "Unidades", "Huevos"],
    [500, "gramos", "Patatas"],
    [1, "Unidad", "Cebolla"],
    [200, "ml", "Aceite de oliva extra virgen"],
    [1, "Pizca", "Sal"]],
    ["vegetariana"],
    None, "ChatGPT",
    "images/tortilla_de_patatas.png",
    "noemail@email.com"
]


recipe_6 = [
    "Gazpacho Andaluz",
    "Una sopa fría y refrescante, llena de sabor y frescura, perfecta para los días calurosos. Un plato saludable y ligero que destaca por sus ingredientes frescos.",
    15, 3, 4,
    "1. Lavar bien los tomates, el pepino, el pimiento verde y el diente de ajo. Pelar el pepino si prefieres una textura más suave.\n"
    "2. Cortar los tomates en cuartos, el pepino en rodajas, y el pimiento en trozos pequeños.\n"
    "3. Colocar todos los ingredientes en una licuadora o procesador de alimentos junto con el aceite de oliva, el vinagre y la sal.\n"
    "4. Licuar a alta velocidad hasta obtener una mezcla homogénea. Si prefieres una textura más líquida, puedes añadir un poco de agua fría.\n"
    "5. Probar el gazpacho y ajustar la sal o vinagre según tu gusto.\n"
    "6. Enfriar en la nevera durante al menos 1 hora para que los sabores se mezclen bien.\n"
    "7. Servir bien frío, acompañado de picatostes, trozos de pepino, pimiento o cebolla, si lo deseas.",
    "fácil", "Entrante",
    ["Verduras"],
    [[4, "Unidades", "Tomates"],
    [1, "Unidad", "Pepino"],
    [1, "Unidad", "Pimiento verde"],
    [1, "Diente", "Ajo"],
    [2, "Cucharadas", "Aceite de oliva extra virgen"],
    [1, "Cucharada", "Vinagre de jerez"],
    [1, "Pizca", "Sal"]],
    ["vegana"],
    None, "ChatGPT",
    "images/gazpacho_andaluz.png",
    "noemail@email.com"
]



recipe_7 = [
    "Paella Valenciana",
    "El plato más emblemático de la gastronomía española, con una combinación perfecta de arroz, carne, verduras y especias, ideal para disfrutar en buena compañía.",
    60, 10, 4,
    "1. En una paellera, calienta el aceite de oliva a fuego medio y sofríe el pollo y el conejo troceados hasta que estén dorados por todos lados.\n"
    "2. Añadir las judías verdes y el garrofón, y rehogar durante unos minutos hasta que las verduras se ablanden ligeramente.\n"
    "3. Incorpora los tomates pelados y triturados, y cocina durante unos minutos hasta que el tomate se haya reducido y concentrado.\n"
    "4. Añadir el arroz y el pimentón, removiendo bien para que se impregne de los sabores.\n"
    "5. Verter el caldo de ave caliente y añadir el azafrán, ajustando la sal al gusto. Cocina a fuego medio-alto sin remover el arroz.\n"
    "6. Cocinar durante unos 20-25 minutos o hasta que el arroz haya absorbido casi todo el caldo. Si es necesario, añadir un poco más de caldo caliente.\n"
    "7. Dejar reposar la paella unos 5-10 minutos antes de servir, para que los sabores se integren y el arroz termine de cocerse en su propio vapor.",
    "difícil", "Plato principal",
    ["Cereales", "Carnes", "Legumbres"],
    [[300, "gramos", "Arroz tipo bomba o valenciano"],
    [500, "gramos", "Pollo troceado (preferiblemente muslos o pechugas)"],
    [300, "gramos", "Conejo troceado"],
    [150, "gramos", "Judías verdes"],
    [100, "gramos", "Garrofón"],
    [2, "Unidades", "Tomates maduros"],
    [1, "Cucharada", "Pimentón dulce"],
    [1, "Pizca", "Azafrán"],
    [1, "Litro", "Caldo de ave (mejor casero)"],
    [3, "Cucharadas", "Aceite de oliva extra virgen"],
    [1, "Pizca", "Sal"]],
    ["Mediterránea"],
    None, "ChatGPT",
    "images/paella_valenciana.png",
    "noemail@email.com"
]



recipe_8 = [
    "Fabada Asturiana",
    "Un contundente plato tradicional del norte de España, ideal para disfrutar en días fríos. Con una mezcla de fabes y embutidos, es perfecto para compartir en familia.",
    120, 7, 4,
    "1. Remojar las fabes en agua la noche anterior.\n"
    "2. Cocer las fabes en una olla grande con el chorizo, la morcilla, el lacón y el tocino durante aproximadamente 2 horas a fuego lento.\n"
    "3. Picar la cebolla y el ajo, y añadirlos a la olla junto con el pimentón (preferentemente pimentón dulce de la Vera).\n"
    "4. Cocinar a fuego lento durante otras 2 horas, hasta que las fabes estén tiernas y los sabores bien integrados.\n"
    "5. Añadir sal al gusto y dejar reposar unos minutos antes de servir.\n"
    "6. Servir caliente, acompañado de pan crujiente.",
    "difícil", "Plato principal",
    ["Legumbres", "Carnes"],
    [[400, "gramos", "Fabes"],
    [1, "Unidad", "Chorizo asturiano"],
    [1, "Unidad", "Morcilla asturiana"],
    [200, "gramos", "Lacón"],
    [100, "gramos", "Tocino"],
    [1, "Unidad", "Cebolla"],
    [1, "Diente", "Ajo"],
    [1, "Cucharadita", "Pimentón dulce de la Vera"],
    [1, "Pizca", "Sal"]],
    ["Desconocida"],
    None, "ChatGPT",
    "images/fabada_asturiana.png",
    "noemail@email.com"
]

recipe_9 = [
    "Croquetas de Jamón",
    "Deliciosas croquetas crujientes por fuera y cremosas por dentro, con un toque de jamón serrano.",
    45, 5, 4,
    "1. Derretir la mantequilla en una sartén y añadir la harina. Cocinar removiendo constantemente hasta obtener una masa dorada.\n"
    "2. Agregar la leche poco a poco sin dejar de remover para evitar grumos.\n"
    "3. Incorporar el jamón picado finamente y cocinar unos minutos más para que se mezcle bien con la masa.\n"
    "4. Dejar enfriar la masa completamente y luego formar pequeñas croquetas.\n"
    "5. Pasar las croquetas por huevo batido y luego por pan rallado.\n"
    "6. Freír las croquetas en abundante aceite caliente hasta que estén doradas y crujientes por fuera.\n"
    "7. Colocar las croquetas sobre papel absorbente para eliminar el exceso de aceite antes de servir.",
    "medio", "Entrante",
    ["Lácteos", "Harinas", "Carnes"],
    [[50, "gramos", "Mantequilla"],
    [50, "gramos", "Harina"],
    [500, "ml", "Leche"],
    [100, "gramos", "Jamón serrano"],
    [1, "Unidad", "Huevo"],
    [100, "gramos", "Pan rallado"],
    [200, "ml", "Aceite de oliva"]],
    ["Desconocida"],
    None, "ChatGPT",
    "images/croquetas_de_jamon.jpg",
    "noemail@email.com"
]


recipe_10 = [
    "Pulpo a la Gallega",
    "Un plato tradicional gallego, ideal para disfrutar de un sabor auténtico con un toque de pimentón y aceite de oliva.",
    50, 12, 2,
    "1. Cocer el pulpo en agua hirviendo con sal hasta que esté tierno.\n"
    "2. Dejar reposar el pulpo unos minutos fuera del agua y luego cortarlo en rodajas.\n"
    "3. Cocer las patatas, pelarlas y cortarlas en rodajas.\n"
    "4. Servir las rodajas de patata como base y colocar las rodajas de pulpo encima.\n"
    "5. Espolvorear con pimentón y añadir aceite de oliva al gusto.\n"
    "6. Servir inmediatamente mientras esté caliente.",
    "medio", "Plato principal",
    ["Pescados", "Verduras"],
    [[1, "Unidad", "Pulpo"],
    [2, "Unidades", "Patatas"],
    [1, "Cucharadita", "Pimentón"],
    [2, "Cucharadas", "Aceite de oliva"],
    [1, "Pizca", "Sal"]],
    ["Mediterránea"],
    None, "ChatGPT",
    "images/pulpo_a_la_gallega.png",
    "noemail@email.com"
]


recipe_11 = [
    "Churros con Chocolate",
    "Un delicioso y crujiente desayuno o merienda español, acompañado de un rico chocolate caliente.",
    40, 3, 4,
    "1. Hervir el agua con una pizca de sal y añadir la harina, removiendo bien hasta obtener una masa suave.\n"
    "2. Dejar enfriar ligeramente la masa antes de formar los churros con una manga pastelera.\n"
    "3. Freír los churros en abundante aceite caliente hasta que estén dorados y crujientes por fuera.\n"
    "4. Servir los churros calientes acompañados de chocolate caliente para sumergir.",
    "medio", "Postre",
    ["Harinas", "Chocolates"],
    [[250, "gramos", "Harina"],
    [250, "ml", "Agua"],
    [1, "Pizca", "Sal"],
    [200, "ml", "Aceite de oliva"],
    [200, "gramos", "Chocolate negro"]],
    ["Desconocida"],
    None, "ChatGPT",
    "images/churros_con_chocolate.png",
    "noemail@email.com"
]

recipe_12 = [
    "Leche Frita",
    "Un postre tradicional con una textura cremosa por dentro y un rebozado crujiente por fuera, perfecto para cualquier ocasión.",
    60, 3, 4,
    "1. Mezclar la leche con el azúcar, la maicena y la canela en una cazuela.\n"
    "2. Cocinar a fuego lento, removiendo constantemente, hasta que la mezcla espese.\n"
    "3. Verter la mezcla en un molde engrasado y dejar enfriar completamente.\n"
    "4. Cortar en porciones, pasar por harina y luego por huevo batido.\n"
    "5. Freír las porciones en aceite caliente hasta que estén doradas y crujientes.\n"
    "6. Espolvorear con azúcar y canela al gusto antes de servir.",
    "medio", "Postre",
    ["Lácteos", "Harinas"],
    [[500, "ml", "Leche"],
    [100, "gramos", "Azúcar"],
    [50, "gramos", "Maicena"],
    [1, "Cucharadita", "Canela"],
    [2, "Unidades", "Huevos"],
    [100, "gramos", "Harina"]],
    ["Desconocida"],
    None, "ChatGPT",
    "images/leche_frita.jpg",
    "noemail@email.com"
]

recipe_13 = [
    "Cocido Madrileño",
    "Un guiso tradicional madrileño de garbanzos con carne, verduras y caldo, ideal para los días fríos.",
    180, 8, 6,
    "1. Remojar los garbanzos en agua la noche anterior.\n"
    "2. Cocer los garbanzos con el chorizo, la morcilla, el tocino y la carne en una olla con agua y sal.\n"
    "3. Añadir las zanahorias, la patata y cualquier otra verdura de tu elección. Cocinar a fuego lento durante dos horas.\n"
    "4. Separar el caldo y utilizarlo para hacer una sopa con los fideos.\n"
    "5. Servir en tres partes: primero la sopa con fideos, luego los garbanzos con las verduras y, por último, las carnes.",
    "difícil", "Plato principal",
    ["Legumbres", "Carnes", "Verduras"],
    [[400, "gramos", "Garbanzos"],
    [200, "gramos", "Morcillo de ternera"],
    [100, "gramos", "Tocino"],
    [1, "Unidad", "Chorizo"],
    [1, "Unidad", "Morcilla"],
    [2, "Unidades", "Zanahorias"],
    [1, "Unidad", "Patata"],
    [100, "gramos", "Fideos"],
    [1, "Pizca", "Sal"]],
    ["Desconocida"],
    None, "ChatGPT",
    "images/cocido_madrileno.png",
    "noemail@email.com"
]

recipe_14 = [
    "Pimientos del Piquillo Rellenos de Bacalao",
    "Un plato tradicional del norte de España, con un relleno cremoso y sabroso de bacalao.",
    45, 7, 4,
    "1. Sofreír la cebolla y el ajo en aceite de oliva.\n"
    "2. Añadir el bacalao desmenuzado y cocinar unos minutos hasta que esté bien cocido.\n"
    "3. Mezclar el bacalao con la bechamel, ajustando la sal y pimienta al gusto. Dejar enfriar.\n"
    "4. Rellenar los pimientos con la mezcla de bacalao y bechamel.\n"
    "5. Servir con salsa de pimientos o tomate caliente por encima.",
    "medio", "Entrante",
    ["Pescados", "Lácteos", "Verduras"],
    [[8, "Unidades", "Pimientos del piquillo"],
    [200, "gramos", "Bacalao desalado"],
    [1, "Unidad", "Cebolla"],
    [1, "Diente", "Ajo"],
    [200, "ml", "Leche"],
    [1, "Cucharada", "Harina"],
    [2, "Cucharadas", "Aceite de oliva"],
    [1, "Pizca", "Sal"],
    [1, "Pizca", "Pimienta"]],
    ["Vegetariana",
    "Mediterránea",
    "Alta en proteínas"],
    None, "ChatGPT",
    "images/pimientos_del_piquillo_rellenos.png",
    "noemail@email.com"
]


recipe_15 = [
    "Calamares a la Romana",
    "Crujientes anillas de calamar rebozadas y fritas, perfectas como tapa o aperitivo.",
    30, 6, 4,
    "1. Cortar los calamares en anillas y secarlas bien con papel absorbente.\n"
    "2. Pasar las anillas por harina, luego por huevo batido y finalmente por pan rallado.\n"
    "3. Freír las anillas en abundante aceite caliente hasta que estén doradas y crujientes.\n"
    "4. Servir con limón en rodajas y mayonesa para acompañar.",
    "fácil", "Entrante",
    ["Pescados", "Harinas"],
    [[300, "gramos", "Calamares"],
    [100, "gramos", "Harina"],
    [1, "Unidad", "Huevo"],
    [100, "gramos", "Pan rallado"],
    [200, "ml", "Aceite de oliva"],
    [1, "Unidad", "Limón"],
    [1, "Pizca", "Sal"]],
    ["Desconocida"],
    None, "ChatGPT",
    "images/calamares_a_la_romana.png",
    "noemail@email.com"
]


recipe_16 = [
    "Empanada Gallega",
    "Una deliciosa empanada de atún con masa crujiente, perfecta para cualquier ocasión.",
    90, 10, 6,
    "1. Preparar la masa mezclando harina, agua, aceite y sal hasta formar una masa homogénea.\n"
    "2. Sofreír la cebolla y el pimiento rojo en aceite de oliva hasta que estén tiernos.\n"
    "3. Añadir el tomate triturado y el atún desmenuzado, y cocinar unos minutos más.\n"
    "4. Estirar la masa sobre una superficie plana, rellenar con la mezcla y cubrir con otra capa de masa.\n"
    "5. Sellar los bordes y hornear a 180°C durante 40 minutos o hasta que esté dorada.\n"
    "6. Servir templada o fría, ideal como plato principal o entrante.",
    "medio", "Plato principal",
    ["Pescados", "Harinas", "Verduras"],
    [[500, "gramos", "Harina"],
    [200, "ml", "Agua"],
    [100, "ml", "Aceite de oliva"],
    [1, "Unidad", "Pimiento rojo"],
    [1, "Unidad", "Cebolla"],
    [200, "gramos", "Atún en conserva"],
    [3, "Cucharadas", "Tomate triturado"],
    [1, "Pizca", "Sal"]],
    ["Desconocida"],
    None, "ChatGPT",
    "images/empanada_gallega.png",
    "noemail@email.com"
]



recipe_17 = [
    "Patatas Bravas",
    "Un clásico de la cocina española, crujientes patatas acompañadas de una salsa picante.",
    40, 4, 4,
    "1. Pelar y cortar las patatas en cubos medianos.\n"
    "2. Freír las patatas en abundante aceite hasta que estén doradas y crujientes.\n"
    "3. Preparar la salsa brava calentando tomate, pimentón, guindilla, vinagre y sal en una sartén.\n"
    "4. Servir las patatas con la salsa por encima y acompañar con alioli si se desea.",
    "fácil", "Entrante",
    ["Verduras"],
    [[500, "gramos", "Patatas"],
    [200, "gramos", "Tomate triturado"],
    [1, "Cucharadita", "Pimentón"],
    [1, "Unidad", "Guindilla"],
    [3, "Cucharadas", "Aceite de oliva"],
    [1, "Pizca", "Sal"]],
    ["Vegana"],
    None, "ChatGPT",
    "images/patatas_bravas.png",
    "noemail@email.com"
]

recipe_18 = [
    "Rabo de Toro",
    "Un guiso tradicional andaluz de carne de toro o ternera, lleno de sabor.",
    180, 15, 4,
    "1. Dorar el rabo de toro en una cazuela con aceite de oliva.\n"
    "2. Sofreír la cebolla, el ajo, la zanahoria y el pimiento hasta que estén tiernos.\n"
    "3. Añadir el tomate triturado, vino tinto, sal y pimienta y cocinar a fuego lento durante tres horas.\n"
    "4. Servir con patatas cocidas o arroz como acompañamiento.",
    "difícil", "Plato principal",
    ["Carnes", "Verduras"],
    [[1, "kg", "Rabo de toro"],
    [1, "Unidad", "Cebolla"],
    [2, "Unidades", "Zanahorias"],
    [1, "Unidad", "Pimiento rojo"],
    [2, "Dientes", "Ajo"],
    [200, "ml", "Vino tinto"],
    [200, "gramos", "Tomate triturado"],
    [3, "Cucharadas", "Aceite de oliva"],
    [1, "Pizca", "Sal"],
    [1, "Pizca", "Pimienta"]],
    ["Sin gluten",
    "Keto (cetogénica)",
    "Alta en proteínas"],
    None, "ChatGPT",
    "images/rabo_de_toro.png",
    "noemail@email.com"
]

recipe_19 = [
    "Tarta de Santiago",
    "Un delicioso postre gallego con almendra y un toque de azúcar glas.",
    50, 8, 6,
    "1. Mezclar almendra molida, azúcar y huevos hasta obtener una masa homogénea.\n"
    "2. Verter la mezcla en un molde engrasado y hornear a 180°C durante 30 minutos.\n"
    "3. Dejar enfriar completamente y espolvorear con azúcar glas en forma de cruz de Santiago antes de servir.",
    "fácil", "Postre",
    ["Frutos secos", "Huevos"],
    [[250, "gramos", "Almendra molida"],
    [250, "gramos", "Azúcar"],
    [4, "Unidades", "Huevos"],
    [1, "Cucharadita", "Canela"],
    [1, "Cucharada", "Azúcar glas"]],
    ["Vegetariana"],
    None, "ChatGPT",
    "images/tarta_de_santiago.png",
    "noemail@email.com"
]



if __name__ == "__main__":
    print(filters())
    print(recipes(recipe_1))
    print(recipes(recipe_2))
    print(recipes(recipe_3))
    print(recipes(recipe_4))
    print(recipes(recipe_5))
    print(recipes(recipe_6))
    print(recipes(recipe_7))
    print(recipes(recipe_8))
    print(recipes(recipe_9))
    print(recipes(recipe_10))
    print(recipes(recipe_11))
    print(recipes(recipe_12))
    print(recipes(recipe_13))
    print(recipes(recipe_14))
    print(recipes(recipe_15))
    print(recipes(recipe_16))
    print(recipes(recipe_17))
    print(recipes(recipe_18))
    print(recipes(recipe_19))

 