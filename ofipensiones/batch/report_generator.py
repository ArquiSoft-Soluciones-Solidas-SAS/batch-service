import logging
import redis
import json

from fastapi import BackgroundTasks
from pymongo import MongoClient

logger = logging.getLogger("report_generator")
MESES = [
    ("Enero", 1),
    ("Febrero", 2),
    ("Marzo", 3),
    ("Abril", 4),
    ("Mayo", 5),
    ("Junio", 6),
    ("Julio", 7),
    ("Agosto", 8),
    ("Septiembre", 9),
    ("Octubre", 10),
    ("Noviembre", 11),
    ("Diciembre", 12),
]
def generate_reports():
    logger.info("Generating reports...")
    client = MongoClient('mongodb://microservicios_user:password@10.128.0.87:27017')
    #obtenemos los nombres de las instituciones usando db = client['reportes-query-service'] y la collection institucion
    db = client['reportes-query-service']
    collection = db['institucion']
    # Devolvemos los nombres de las instituciones: nombreInstitucion
    instituciones = collection.find({}, {"nombreInstitucion": 1})
    logger.info(f"Instituciones: {instituciones}")
    r = redis.StrictRedis(host='10.128.0.88', port=6379, db=0)

    # for institucion in instituciones:
    #     # Pipeline
    #     pipeline = [
    #         {
    #             "$lookup": {
    #                 "from": "recibo_pago",
    #                 "localField": "_id",
    #                 "foreignField": "recibo_cobro",
    #                 "as": "pagos"
    #             }
    #         },
    #         {
    #             "$match": {
    #                 "pagos": {"$size": 0}
    #             }
    #         },
    #         {
    #             "$lookup": {
    #                 "from": "estudiante",
    #                 "localField": "estudiante",
    #                 "foreignField": "_id",
    #                 "as": "estudiante"
    #             }
    #         },
    #         {"$unwind": "$estudiante"},
    #         {
    #             "$lookup": {
    #                 "from": "institucion",
    #                 "localField": "estudiante.institucionEstudianteId",
    #                 "foreignField": "_id",
    #                 "as": "institucion"
    #             }
    #         },
    #         {"$unwind": "$institucion"},
    #         {
    #             "$match": {
    #                 "institucion.nombreInstitucion": institucion
    #             }
    #         },
    #         {"$unwind": "$detalles_cobro"},
    #         {
    #             "$lookup": {
    #                 "from": "cronograma_base",
    #                 "let": {"detalleId": "$detalles_cobro._id"},
    #                 "pipeline": [
    #                     {
    #                         "$match": {
    #                             "$expr": {
    #                                 "$in": ["$$detalleId", "$detalle_cobro._id"]
    #                             }
    #                         }
    #                     }
    #                 ],
    #                 "as": "cronograma"
    #             }
    #         },
    #         {"$unwind": "$cronograma"},
    #         {
    #             "$project": {
    #                 "monto_recibo": {"$toDouble": "$nmonto"},
    #                 "mes": "$detalles_cobro.mes",
    #                 "valor_detalle": {"$toDouble": "$detalles_cobro.valor"},
    #                 "estudiante_id": {"$toString": "$estudiante._id"},
    #                 "nombre_estudiante": "$estudiante.nombreEstudiante",
    #                 "nombre_grado": "$cronograma.grado",
    #                 "nombre_institucion": "$institucion.nombreInstitucion",
    #                 "nombre_concepto": "$cronograma.nombre",
    #                 "codigo": "$cronograma.codigo"
    #             }
    #         }
    #     ]
    #
    #     # Obtenemos los reportes
    #     cursor_resultados = db["recibo_cobro"].aggregate(pipeline)
    #     resultados = list(cursor_resultados)  # En estos resultados están las cuentas por cobrar de TODOS los meses
    #
    #     #hacemos un for, filtrando por mes y vamos guardando cada uno en la base de datos de redis
    #     for mes, numero_mes in MESES:
    #         processed_rows = [
    #             {
    #                 "monto_recibo": row["monto_recibo"],
    #                 "mes": row["mes"],
    #                 "valor_detalle": row["valor_detalle"],
    #                 "estudiante_id": row["estudiante_id"],
    #                 "nombre_estudiante": row["nombre_estudiante"],
    #                 "nombre_grado": row["nombre_grado"],
    #                 "nombre_institucion": row["nombre_institucion"],
    #                 "nombre_concepto": row["nombre_concepto"],
    #                 "codigo": row["codigo"]
    #             }
    #             for row in resultados if row["mes"] == mes
    #         ]
    #         key = f"cuentas_por_cobrar:{institucion}:{mes}"
    #         print(f"Key: {key}")
    #         if processed_rows:
    #             r.set(key, json.dumps(processed_rows), ex=60 * 60 * 24)