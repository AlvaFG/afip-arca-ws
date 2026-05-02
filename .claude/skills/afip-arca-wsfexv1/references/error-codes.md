# WSFEXv1 Error codes

| Código | Mensaje | Causa típica | Fix |
|---|---|---|---|
| 600 | Token inválido | TA expirado o malformado | Re-obtener TA con `service=wsfex` |
| 601 | Sign inválido | Mismatch en sign del TA | Re-obtener TA |
| 1500 | Pto_venta no autorizado para export | El punto de venta no está dado de alta para exportación | Crear PV de tipo "exportación" en AFIP |
| 1501 | Idioma_cbte inválido | Valor fuera de {1,2,3} | Revisar `references/idiomas.md` |
| 1502 | Moneda_Id inválida | No existe en `FEXGetPARAM_MON` | Llamar `FEXGetPARAM_MON` y elegir uno válido |
| 1503 | Moneda_ctz fuera de rango | Cotización absurda (e.g. 0 o negativa) | Usar cotización del día desde BCRA |
| 1505 | Incoterms inválido | No está en `FEXGetPARAM_Incoterms` | Usar código estándar (FOB, CIF, etc.) |
| 1506 | Tipo_expo inválido | Valor fuera de {1,2,4} | 1=Bienes, 2=Servicios, 4=Otros |
| 1510 | Dst_cmp = Argentina | Argentina (200) no es destino válido para export | Cambiar al país real del cliente |
| 1517 | Permiso_existente requerido pero no informado | Si Tipo_expo=1 (bienes), Permiso_existente debe ser S/N | Completar el campo |
| 1518 | Permiso inválido | Id_permiso no validado contra Aduana | Llamar `FEXCheck_Permiso` antes |
| 1601 | Cliente requerido | Nombre del cliente vacío | Completar |
| 1602 | Cuit_pais_cliente inválido | El CUIT del país no existe en padrón | Verificar; AFIP mantiene lista de "CUIT país" |
| 1603 | Items vacíos | Items[] tiene 0 elementos | Agregar al menos 1 ítem |
